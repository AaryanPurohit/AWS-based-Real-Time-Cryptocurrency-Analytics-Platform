#!/usr/bin/env python3
"""
FastAPI Backend for AWS Crypto Analytics Platform
Provides REST API endpoints for cryptocurrency data and ML predictions
Demonstrates microservices architecture and AWS service integration
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import boto3
import json
import redis
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import requests
from pydantic import BaseModel
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AWS Crypto Analytics API",
    description="Real-time cryptocurrency analytics platform built on AWS services",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
s3_client = boto3.client('s3')
sagemaker_runtime = boto3.client('sagemaker-runtime')

# Configuration
DYNAMODB_TABLE = os.environ.get('DYNAMODB_TABLE', 'crypto-prices-dev')
S3_BUCKET = os.environ.get('S3_BUCKET', 'crypto-data-lake-dev')
REDIS_ENDPOINT = os.environ.get('REDIS_ENDPOINT')
SAGEMAKER_ENDPOINT = os.environ.get('SAGEMAKER_ENDPOINT')

# Initialize Redis client
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

# Pydantic models
class CryptoPrice(BaseModel):
    symbol: str
    price_usd: float
    market_cap: float
    volume_24h: float
    price_change_24h: float
    timestamp: str

class PredictionRequest(BaseModel):
    symbol: str
    historical_data: List[Dict[str, Any]]

class PredictionResponse(BaseModel):
    symbol: str
    predicted_price: float
    confidence: float
    timestamp: str

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "dynamodb": DYNAMODB_TABLE is not None,
            "redis": redis_client is not None,
            "sagemaker": SAGEMAKER_ENDPOINT is not None
        }
    }

# Get latest cryptocurrency prices
@app.get("/api/prices", response_model=Dict[str, Any])
async def get_latest_prices():
    """Get latest cryptocurrency prices from cache/database"""
    try:
        prices = await get_crypto_prices()
        
        return {
            "prices": prices,
            "timestamp": datetime.utcnow().isoformat(),
            "source": "aws-crypto-analytics"
        }
        
    except Exception as e:
        logger.error(f"Error getting latest prices: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Get specific cryptocurrency price
@app.get("/api/prices/{symbol}", response_model=Dict[str, Any])
async def get_crypto_price(symbol: str):
    """Get latest price for a specific cryptocurrency"""
    try:
        symbol = symbol.upper()
        prices = await get_crypto_prices([symbol])
        
        if symbol not in prices:
            raise HTTPException(status_code=404, detail=f"Cryptocurrency {symbol} not found")
        
        return {
            "symbol": symbol,
            "data": prices[symbol],
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting price for {symbol}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Get historical data
@app.get("/api/history/{symbol}")
async def get_historical_data(symbol: str, hours: int = 24):
    """Get historical price data for a cryptocurrency"""
    try:
        symbol = symbol.upper()
        
        # Try to get from Redis first
        if redis_client:
            historical_key = f"crypto:{symbol}:history"
            historical_data = redis_client.zrange(historical_key, -hours, -1)
            
            if historical_data:
                data = [json.loads(item) for item in historical_data]
                return {
                    "symbol": symbol,
                    "data": data,
                    "hours": hours,
                    "source": "redis_cache"
                }
        
        # Fallback to DynamoDB
        if DYNAMODB_TABLE:
            table = dynamodb.Table(DYNAMODB_TABLE)
            
            # Calculate time range
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(hours=hours)
            
            response = table.query(
                KeyConditionExpression='symbol = :symbol AND #ts BETWEEN :start AND :end',
                ExpressionAttributeNames={'#ts': 'timestamp'},
                ExpressionAttributeValues={
                    ':symbol': symbol,
                    ':start': start_time.isoformat(),
                    ':end': end_time.isoformat()
                },
                ScanIndexForward=False,
                Limit=1000
            )
            
            return {
                "symbol": symbol,
                "data": response.get('Items', []),
                "hours": hours,
                "source": "dynamodb"
            }
        
        raise HTTPException(status_code=404, detail=f"No historical data found for {symbol}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting historical data for {symbol}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# ML prediction endpoint
@app.post("/api/predict", response_model=PredictionResponse)
async def predict_price(request: PredictionRequest):
    """Get ML-powered price prediction for a cryptocurrency"""
    try:
        if not SAGEMAKER_ENDPOINT:
            raise HTTPException(status_code=503, detail="ML service not available")
        
        # Prepare data for ML model
        ml_input = prepare_ml_input(request.symbol, request.historical_data)
        
        # Call SageMaker endpoint
        response = sagemaker_runtime.invoke_endpoint(
            EndpointName=SAGEMAKER_ENDPOINT,
            ContentType='application/json',
            Body=json.dumps(ml_input)
        )
        
        # Parse prediction response
        prediction_result = json.loads(response['Body'].read().decode())
        
        return PredictionResponse(
            symbol=request.symbol,
            predicted_price=prediction_result.get('predicted_price', 0.0),
            confidence=prediction_result.get('confidence', 0.0),
            timestamp=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error making prediction for {request.symbol}: {e}")
        raise HTTPException(status_code=500, detail="Prediction service error")

# Market analytics endpoint
@app.get("/api/analytics/market")
async def get_market_analytics():
    """Get market-wide analytics and insights"""
    try:
        # Get all cryptocurrency prices
        prices = await get_crypto_prices()
        
        if not prices:
            raise HTTPException(status_code=404, detail="No market data available")
        
        # Calculate market analytics
        total_market_cap = sum(price.get('market_cap', 0) for price in prices.values())
        total_volume = sum(price.get('volume_24h', 0) for price in prices.values())
        
        # Find top gainers and losers
        sorted_by_change = sorted(
            prices.items(),
            key=lambda x: x[1].get('price_change_24h', 0),
            reverse=True
        )
        
        analytics = {
            "total_market_cap": total_market_cap,
            "total_volume_24h": total_volume,
            "crypto_count": len(prices),
            "top_gainers": sorted_by_change[:3],
            "top_losers": sorted_by_change[-3:],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return analytics
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting market analytics: {e}")
        raise HTTPException(status_code=500, detail="Analytics service error")

# Background task to refresh cache
@app.post("/api/cache/refresh")
async def refresh_cache(background_tasks: BackgroundTasks):
    """Refresh cache with latest data"""
    background_tasks.add_task(update_cache)
    return {"message": "Cache refresh initiated", "timestamp": datetime.utcnow().isoformat()}

# Helper functions
async def get_crypto_prices(symbols: List[str] = None) -> Dict[str, Any]:
    """Get cryptocurrency prices from cache/database"""
    if not symbols:
        symbols = ['BTC', 'ETH', 'BNB', 'ADA', 'SOL', 'DOT', 'LINK', 'LTC']
    
    prices = {}
    
    # Try Redis cache first
    if redis_client:
        for symbol in symbols:
            cache_key = f"crypto:{symbol}:latest"
            cached_data = redis_client.get(cache_key)
            
            if cached_data:
                prices[symbol] = json.loads(cached_data)
    
    # Fallback to DynamoDB
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

def prepare_ml_input(symbol: str, historical_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Prepare data for ML model input"""
    # Extract features from historical data
    features = []
    
    for data_point in historical_data[-100:]:  # Last 100 data points
        features.append({
            'price': data_point.get('price_usd', 0),
            'volume': data_point.get('volume_24h', 0),
            'market_cap': data_point.get('market_cap', 0),
            'price_change': data_point.get('price_change_24h', 0)
        })
    
    return {
        'symbol': symbol,
        'features': features,
        'timestamp': datetime.utcnow().isoformat()
    }

async def update_cache():
    """Background task to update cache with latest data"""
    try:
        # Fetch fresh data from CoinGecko
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': 'bitcoin,ethereum,binancecoin,cardano,solana,polkadot,chainlink,litecoin',
            'vs_currencies': 'usd',
            'include_market_cap': 'true',
            'include_24hr_vol': 'true',
            'include_24hr_change': 'true',
            'include_last_updated_at': 'true'
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Update Redis cache
        if redis_client:
            for crypto_id, crypto_data in data.items():
                record = {
                    'symbol': crypto_id.upper(),
                    'price_usd': crypto_data.get('usd', 0),
                    'market_cap': crypto_data.get('usd_market_cap', 0),
                    'volume_24h': crypto_data.get('usd_24h_vol', 0),
                    'price_change_24h': crypto_data.get('usd_24h_change', 0),
                    'last_updated': crypto_data.get('last_updated_at', int(time.time())),
                    'timestamp': datetime.utcnow().isoformat(),
                    'source': 'coingecko'
                }
                
                cache_key = f"crypto:{record['symbol']}:latest"
                redis_client.setex(cache_key, 300, json.dumps(record))
        
        logger.info("Cache updated successfully")
        
    except Exception as e:
        logger.error(f"Error updating cache: {e}")

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting AWS Crypto Analytics API...")
    logger.info(f"DynamoDB Table: {DYNAMODB_TABLE}")
    logger.info(f"S3 Bucket: {S3_BUCKET}")
    logger.info(f"Redis Endpoint: {REDIS_ENDPOINT}")
    logger.info(f"SageMaker Endpoint: {SAGEMAKER_ENDPOINT}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 