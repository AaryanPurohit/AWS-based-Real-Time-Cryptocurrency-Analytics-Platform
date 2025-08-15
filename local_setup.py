#!/usr/bin/env python3
"""
Local Development Setup for AWS Crypto Analytics Platform
This script sets up a local environment that simulates AWS services
Perfect for development and testing before AWS deployment
"""

import os
import json
import time
import requests
import sqlite3
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LocalDataStore:
    """Simulates DynamoDB with SQLite for local development"""
    
    def __init__(self, db_path: str = "local_crypto.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database with crypto tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create crypto prices table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS crypto_prices (
                symbol TEXT PRIMARY KEY,
                price_usd REAL,
                market_cap REAL,
                volume_24h REAL,
                price_change_24h REAL,
                timestamp TEXT,
                last_updated TEXT
            )
        ''')
        
        # Create historical data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS historical_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT,
                price_usd REAL,
                timestamp TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Local database initialized")
    
    def store_price(self, data: Dict[str, Any]):
        """Store cryptocurrency price data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO crypto_prices 
            (symbol, price_usd, market_cap, volume_24h, price_change_24h, timestamp, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['symbol'],
            data['price_usd'],
            data['market_cap'],
            data['volume_24h'],
            data['price_change_24h'],
            data['timestamp'],
            datetime.utcnow().isoformat()
        ))
        
        # Store historical data
        cursor.execute('''
            INSERT INTO historical_data (symbol, price_usd, timestamp)
            VALUES (?, ?, ?)
        ''', (data['symbol'], data['price_usd'], data['timestamp']))
        
        conn.commit()
        conn.close()
    
    def get_latest_prices(self) -> Dict[str, Any]:
        """Get latest prices for all cryptocurrencies"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM crypto_prices')
        rows = cursor.fetchall()
        
        prices = {}
        for row in rows:
            prices[row[0]] = {
                'price_usd': row[1],
                'market_cap': row[2],
                'volume_24h': row[3],
                'price_change_24h': row[4],
                'timestamp': row[5],
                'last_updated': row[6]
            }
        
        conn.close()
        return prices
    
    def get_historical_data(self, symbol: str, hours: int = 24) -> List[Dict[str, Any]]:
        """Get historical data for a cryptocurrency"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get data from last N hours
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        cutoff_str = cutoff_time.isoformat()
        
        cursor.execute('''
            SELECT price_usd, timestamp 
            FROM historical_data 
            WHERE symbol = ? AND timestamp > ?
            ORDER BY timestamp DESC
        ''', (symbol, cutoff_str))
        
        rows = cursor.fetchall()
        data = [{'price': row[0], 'timestamp': row[1]} for row in rows]
        
        conn.close()
        return data

class LocalCache:
    """Simulates Redis cache for local development"""
    
    def __init__(self):
        self.cache = {}
        self.expiry = {}
    
    def set(self, key: str, value: Any, expire: int = 300):
        """Set cache value with expiration"""
        self.cache[key] = value
        self.expiry[key] = time.time() + expire
    
    def get(self, key: str) -> Any:
        """Get cache value if not expired"""
        if key in self.cache and time.time() < self.expiry.get(key, 0):
            return self.cache[key]
        return None
    
    def delete(self, key: str):
        """Delete cache key"""
        if key in self.cache:
            del self.cache[key]
        if key in self.expiry:
            del self.expiry[key]

class LocalDataProducer:
    """Simulates Kinesis producer by fetching real data"""
    
    def __init__(self, data_store: LocalDataStore):
        self.data_store = data_store
        self.coingecko_base_url = "https://api.coingecko.com/api/v3"
        self.crypto_ids = [
            'bitcoin', 'ethereum', 'binancecoin', 'cardano', 
            'solana', 'polkadot', 'chainlink', 'litecoin'
        ]
    
    def fetch_and_store_data(self):
        """Fetch real cryptocurrency data and store locally"""
        try:
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
            
            for crypto_id, crypto_data in data.items():
                record = {
                    'symbol': crypto_id.upper(),
                    'price_usd': crypto_data.get('usd', 0),
                    'market_cap': crypto_data.get('usd_market_cap', 0),
                    'volume_24h': crypto_data.get('usd_24h_vol', 0),
                    'price_change_24h': crypto_data.get('usd_24h_change', 0),
                    'timestamp': datetime.utcnow().isoformat()
                }
                self.data_store.store_price(record)
            
            logger.info(f"Fetched and stored data for {len(data)} cryptocurrencies")
            
        except Exception as e:
            logger.error(f"Error fetching data: {e}")
    
    def run_continuous(self, interval: int = 60):
        """Run data producer continuously"""
        logger.info(f"Starting local data producer (interval: {interval}s)")
        
        while True:
            try:
                self.fetch_and_store_data()
                time.sleep(interval)
            except KeyboardInterrupt:
                logger.info("Stopping data producer")
                break
            except Exception as e:
                logger.error(f"Error in data producer: {e}")
                time.sleep(interval)

def create_local_env_file():
    """Create local environment file"""
    env_content = """# Local Development Environment
# These variables simulate AWS services locally

# Backend Configuration
BACKEND_HOST=localhost
BACKEND_PORT=8000

# Database Configuration (SQLite)
DATABASE_URL=sqlite:///local_crypto.db

# Cache Configuration (Local)
REDIS_ENDPOINT=localhost
REDIS_PORT=6379

# API Configuration
API_BASE_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000

# Development Mode
DEBUG=true
ENVIRONMENT=local
"""
    
    with open('.env.local', 'w') as f:
        f.write(env_content)
    
    logger.info("Created .env.local file")

def main():
    """Main function to set up local development environment"""
    logger.info("Setting up local development environment...")
    
    # Create environment file
    create_local_env_file()
    
    # Initialize local data store
    data_store = LocalDataStore()
    
    # Initialize local cache
    cache = LocalCache()
    
    # Initialize data producer
    producer = LocalDataProducer(data_store)
    
    # Start data producer in background thread
    producer_thread = threading.Thread(
        target=producer.run_continuous, 
        args=(60,),  # 60 second interval
        daemon=True
    )
    producer_thread.start()
    
    logger.info("Local development environment ready!")
    logger.info("Next steps:")
    logger.info("1. Start backend: python backend/app_local.py")
    logger.info("2. Start frontend: cd frontend && npm start")
    logger.info("3. Data will be automatically fetched every 60 seconds")
    
    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down local environment")

if __name__ == "__main__":
    main() 