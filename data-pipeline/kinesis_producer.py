#!/usr/bin/env python3
"""
AWS Kinesis Producer for Real-Time Cryptocurrency Data
Fetches data from CoinGecko API and streams to Kinesis Data Streams
Demonstrates AWS SDK integration and real-time data processing
"""

import boto3
import json
import time
import requests
import logging
from datetime import datetime
from typing import Dict, List, Any
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CryptoKinesisProducer:
    """
    Real-time cryptocurrency data producer using AWS Kinesis
    Demonstrates microservices architecture and cloud-native development
    """
    
    def __init__(self, stream_name: str, region: str = 'us-east-1'):
        """
        Initialize the Kinesis producer
        
        Args:
            stream_name: Name of the Kinesis stream
            region: AWS region
        """
        self.stream_name = stream_name
        self.kinesis_client = boto3.client('kinesis', region_name=region)
        self.coingecko_base_url = "https://api.coingecko.com/api/v3"
        
        # Top cryptocurrencies to track
        self.crypto_ids = [
            'bitcoin', 'ethereum', 'binancecoin', 'cardano', 
            'solana', 'polkadot', 'chainlink', 'litecoin'
        ]
        
        logger.info(f"Initialized Kinesis producer for stream: {stream_name}")
    
    def fetch_crypto_data(self) -> List[Dict[str, Any]]:
        """
        Fetch real-time cryptocurrency data from CoinGecko API
        
        Returns:
            List of cryptocurrency data dictionaries
        """
        try:
            # Fetch current prices and market data
            url = f"{self.coingecko_base_url}/simple/price"
            params = {
                'ids': ','.join(self.crypto_ids),
                'vs_currencies': 'usd',
                'include_market_cap': 'true',
                'include_24hr_vol': 'true',
                'include_24hr_change': 'true',
                'include_last_updated_at': 'true'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            crypto_records = []
            
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
                crypto_records.append(record)
            
            logger.info(f"Fetched data for {len(crypto_records)} cryptocurrencies")
            return crypto_records
            
        except requests.RequestException as e:
            logger.error(f"Error fetching data from CoinGecko: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return []
    
    def send_to_kinesis(self, records: List[Dict[str, Any]]) -> bool:
        """
        Send records to Kinesis Data Stream
        
        Args:
            records: List of cryptocurrency data records
            
        Returns:
            True if successful, False otherwise
        """
        try:
            kinesis_records = []
            
            for record in records:
                # Create Kinesis record
                kinesis_record = {
                    'Data': json.dumps(record),
                    'PartitionKey': record['symbol']
                }
                kinesis_records.append(kinesis_record)
            
            # Send records to Kinesis
            response = self.kinesis_client.put_records(
                Records=kinesis_records,
                StreamName=self.stream_name
            )
            
            # Check for failed records
            failed_records = response.get('FailedRecordCount', 0)
            if failed_records > 0:
                logger.warning(f"Failed to send {failed_records} records to Kinesis")
                return False
            
            logger.info(f"Successfully sent {len(records)} records to Kinesis")
            return True
            
        except Exception as e:
            logger.error(f"Error sending data to Kinesis: {e}")
            return False
    
    def run(self, interval: int = 60):
        """
        Main loop to continuously fetch and stream data
        
        Args:
            interval: Time interval between data fetches in seconds
        """
        logger.info(f"Starting Kinesis producer. Fetching data every {interval} seconds...")
        
        while True:
            try:
                # Fetch cryptocurrency data
                crypto_data = self.fetch_crypto_data()
                
                if crypto_data:
                    # Send to Kinesis
                    success = self.send_to_kinesis(crypto_data)
                    
                    if success:
                        logger.info(f"Successfully processed {len(crypto_data)} records")
                    else:
                        logger.error("Failed to send data to Kinesis")
                else:
                    logger.warning("No data fetched from CoinGecko")
                
                # Wait for next interval
                time.sleep(interval)
                
            except KeyboardInterrupt:
                logger.info("Stopping Kinesis producer...")
                break
            except Exception as e:
                logger.error(f"Unexpected error in main loop: {e}")
                time.sleep(interval)

def main():
    """
    Main function to run the Kinesis producer
    """
    # Get configuration from environment variables
    stream_name = os.getenv('KINESIS_STREAM_NAME', 'crypto-price-stream-dev')
    region = os.getenv('AWS_REGION', 'us-east-1')
    interval = int(os.getenv('FETCH_INTERVAL', '60'))
    
    # Create and run producer
    producer = CryptoKinesisProducer(stream_name, region)
    producer.run(interval)

if __name__ == "__main__":
    main() 