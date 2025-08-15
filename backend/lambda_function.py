#!/usr/bin/env python3
"""
AWS Lambda Function for Real-Time Cryptocurrency Data Processing
Processes data from Kinesis streams and stores in DynamoDB
Demonstrates serverless architecture and AWS service integration
"""

import json
import boto3
import logging
import os
from datetime import datetime
from typing import Dict, List, Any
import redis

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
s3_client = boto3.client('s3')

# Get environment variables
DYNAMODB_TABLE = os.environ.get('DYNAMODB_TABLE')
S3_BUCKET = os.environ.get('S3_BUCKET', 'crypto-data-lake-dev')
REDIS_ENDPOINT = os.environ.get('REDIS_ENDPOINT')

# Initialize Redis client if endpoint is provided
redis_client = None
if REDIS_ENDPOINT:
    try:
        redis_client = redis.Redis(
            host=REDIS_ENDPOINT,
            port=6379,
            decode_responses=True,
            socket_connect_timeout=5
        )
        logger.info(f"Connected to Redis at {REDIS_ENDPOINT}")
    except Exception as e:
        logger.warning(f"Failed to connect to Redis: {e}")
        redis_client = None

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda function handler for processing Kinesis records
    
    Args:
        event: Kinesis event containing records
        context: Lambda context
        
    Returns:
        Response dictionary
    """
    try:
        logger.info(f"Processing {len(event['Records'])} records from Kinesis")
        
        processed_records = 0
        failed_records = 0
        
        for record in event['Records']:
            try:
                # Parse Kinesis record
                kinesis_data = json.loads(record['kinesis']['data'])
                
                # Process the record
                success = process_crypto_record(kinesis_data)
                
                if success:
                    processed_records += 1
                else:
                    failed_records += 1
                    
            except Exception as e:
                logger.error(f"Error processing record: {e}")
                failed_records += 1
        
        logger.info(f"Processed {processed_records} records, {failed_records} failed")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'processed': processed_records,
                'failed': failed_records
            })
        }
        
    except Exception as e:
        logger.error(f"Lambda handler error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def process_crypto_record(record: Dict[str, Any]) -> bool:
    """
    Process a single cryptocurrency record
    
    Args:
        record: Cryptocurrency data record
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Store in DynamoDB
        if DYNAMODB_TABLE:
            store_in_dynamodb(record)
        
        # Cache in Redis
        if redis_client:
            cache_in_redis(record)
        
        # Store in S3 for data lake
        store_in_s3(record)
        
        return True
        
    except Exception as e:
        logger.error(f"Error processing record: {e}")
        return False

def store_in_dynamodb(record: Dict[str, Any]) -> None:
    """
    Store record in DynamoDB for real-time access
    
    Args:
        record: Cryptocurrency data record
    """
    try:
        table = dynamodb.Table(DYNAMODB_TABLE)
        
        # Create DynamoDB item
        item = {
            'symbol': record['symbol'],
            'timestamp': record['timestamp'],
            'price_usd': record['price_usd'],
            'market_cap': record['market_cap'],
            'volume_24h': record['volume_24h'],
            'price_change_24h': record['price_change_24h'],
            'last_updated': record['last_updated'],
            'source': record['source']
        }
        
        # Put item in DynamoDB
        table.put_item(Item=item)
        logger.debug(f"Stored {record['symbol']} data in DynamoDB")
        
    except Exception as e:
        logger.error(f"Error storing in DynamoDB: {e}")
        raise

def cache_in_redis(record: Dict[str, Any]) -> None:
    """
    Cache record in Redis for fast access
    
    Args:
        record: Cryptocurrency data record
    """
    try:
        # Create cache key
        cache_key = f"crypto:{record['symbol']}:latest"
        
        # Cache the record with 5-minute expiration
        redis_client.setex(
            cache_key,
            300,  # 5 minutes
            json.dumps(record)
        )
        
        # Also store in a sorted set for historical data
        historical_key = f"crypto:{record['symbol']}:history"
        score = float(record['last_updated'])
        redis_client.zadd(historical_key, {json.dumps(record): score})
        
        # Keep only last 1000 records
        redis_client.zremrangebyrank(historical_key, 0, -1001)
        
        logger.debug(f"Cached {record['symbol']} data in Redis")
        
    except Exception as e:
        logger.error(f"Error caching in Redis: {e}")
        # Don't raise exception for Redis failures

def store_in_s3(record: Dict[str, Any]) -> None:
    """
    Store record in S3 for data lake
    
    Args:
        record: Cryptocurrency data record
    """
    try:
        # Create S3 key with date partitioning
        date_str = datetime.fromtimestamp(record['last_updated']).strftime('%Y/%m/%d')
        time_str = datetime.fromtimestamp(record['last_updated']).strftime('%H')
        
        s3_key = f"raw/crypto/{date_str}/{time_str}/{record['symbol']}_{record['last_updated']}.json"
        
        # Upload to S3
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=s3_key,
            Body=json.dumps(record),
            ContentType='application/json'
        )
        
        logger.debug(f"Stored {record['symbol']} data in S3: {s3_key}")
        
    except Exception as e:
        logger.error(f"Error storing in S3: {e}")
        # Don't raise exception for S3 failures

def get_crypto_prices(symbols: List[str] = None) -> Dict[str, Any]:
    """
    Get latest cryptocurrency prices from cache/database
    
    Args:
        symbols: List of cryptocurrency symbols to fetch
        
    Returns:
        Dictionary with cryptocurrency prices
    """
    try:
        if not symbols:
            symbols = ['BTC', 'ETH', 'BNB', 'ADA', 'SOL', 'DOT', 'LINK', 'LTC']
        
        prices = {}
        
        if redis_client:
            # Try to get from Redis cache first
            for symbol in symbols:
                cache_key = f"crypto:{symbol}:latest"
                cached_data = redis_client.get(cache_key)
                
                if cached_data:
                    prices[symbol] = json.loads(cached_data)
        
        # If not in cache, get from DynamoDB
        if DYNAMODB_TABLE and len(prices) < len(symbols):
            table = dynamodb.Table(DYNAMODB_TABLE)
            
            for symbol in symbols:
                if symbol not in prices:
                    try:
                        response = table.query(
                            KeyConditionExpression='symbol = :symbol',
                            ScanIndexForward=False,
                            Limit=1,
                            ExpressionAttributeValues={':symbol': symbol}
                        )
                        
                        if response['Items']:
                            prices[symbol] = response['Items'][0]
                    except Exception as e:
                        logger.error(f"Error querying DynamoDB for {symbol}: {e}")
        
        return prices
        
    except Exception as e:
        logger.error(f"Error getting crypto prices: {e}")
        return {}

# API Gateway handler for REST API
def api_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    API Gateway handler for REST endpoints
    
    Args:
        event: API Gateway event
        context: Lambda context
        
    Returns:
        API Gateway response
    """
    try:
        http_method = event['httpMethod']
        path = event['path']
        
        if http_method == 'GET' and path == '/prices':
            # Get latest prices
            prices = get_crypto_prices()
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'prices': prices,
                    'timestamp': datetime.utcnow().isoformat()
                })
            }
        
        elif http_method == 'GET' and path.startswith('/prices/'):
            # Get specific cryptocurrency price
            symbol = path.split('/')[-1].upper()
            prices = get_crypto_prices([symbol])
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'symbol': symbol,
                    'data': prices.get(symbol, {}),
                    'timestamp': datetime.utcnow().isoformat()
                })
            }
        
        else:
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'Endpoint not found'})
            }
            
    except Exception as e:
        logger.error(f"API handler error: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'Internal server error'})
        } 