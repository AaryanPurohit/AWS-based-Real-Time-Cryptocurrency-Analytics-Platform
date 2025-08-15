#!/usr/bin/env python3
"""
Local FastAPI Backend for AWS Crypto Analytics Platform
Uses local SQLite database and cache instead of AWS services
Perfect for development and testing
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import logging
import os
import sqlite3
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import requests
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app with lifespan
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler"""
    logger.info("Local Crypto Analytics API starting up...")
    logger.info("Environment: Local Development")
    logger.info("Database: SQLite")
    logger.info("Cache: In-memory")
    yield
    logger.info("Local Crypto Analytics API shutting down...")

app = FastAPI(
    title="Local Crypto Analytics API",
    description="Local development version of the cryptocurrency analytics platform",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Local database configuration
DB_PATH = "../local_crypto.db"

# Simple in-memory cache
cache = {}

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

def get_db_connection():
    """Get SQLite database connection"""
    return sqlite3.connect(DB_PATH)

def get_latest_prices_from_db() -> Dict[str, Any]:
    """Get latest prices from local database"""
    conn = get_db_connection()
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

def get_historical_data_from_db(symbol: str, hours: int = 24) -> List[Dict[str, Any]]:
    """Get historical data from local database"""
    conn = get_db_connection()
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

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": "local",
        "database": "sqlite",
        "cache": "in-memory"
    }

# Test endpoint
@app.get("/test")
async def test_endpoint():
    """Test endpoint to debug the issue"""
    try:
        prices = get_latest_prices_from_db()
        return {"prices": prices, "count": len(prices)}
    except Exception as e:
        logger.error(f"Test endpoint error: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return {"error": str(e)}

# Get latest cryptocurrency prices
@app.get("/api/prices")
async def get_latest_prices():
    """Get latest prices for all cryptocurrencies"""
    try:
        # Check cache first
        cache_key = "latest_prices"
        cached_data = cache.get(cache_key)
        
        if cached_data and time.time() - cached_data.get('timestamp', 0) < 30:
            logger.info("Returning cached data")
            return {"prices": cached_data['data']}
        
        # Get from database
        logger.info("Fetching data from database")
        prices = get_latest_prices_from_db()
        logger.info(f"Retrieved {len(prices)} prices from database")
        
        # Cache the result
        cache[cache_key] = {
            'data': prices,
            'timestamp': time.time()
        }
        
        return {"prices": prices}
        
    except Exception as e:
        logger.error(f"Error getting latest prices: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Failed to fetch prices")

# Get specific cryptocurrency price
@app.get("/api/prices/{symbol}")
async def get_crypto_price(symbol: str):
    """Get price for a specific cryptocurrency"""
    try:
        prices = get_latest_prices_from_db()
        
        if symbol.upper() not in prices:
            raise HTTPException(status_code=404, detail="Cryptocurrency not found")
        
        return {
            "symbol": symbol.upper(),
            "data": prices[symbol.upper()]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting price for {symbol}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch price")

# Get historical data
@app.get("/api/history/{symbol}")
async def get_historical_data(symbol: str, hours: int = 24):
    """Get historical data for a cryptocurrency"""
    try:
        # Validate hours parameter
        if hours < 1 or hours > 168:  # Max 1 week
            hours = 24
        
        data = get_historical_data_from_db(symbol.upper(), hours)
        
        if not data:
            raise HTTPException(status_code=404, detail="No historical data found")
        
        return {
            "symbol": symbol.upper(),
            "hours": hours,
            "data": data,
            "count": len(data)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting historical data for {symbol}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch historical data")

# Simple ML prediction (simulated)
@app.post("/api/predict", response_model=PredictionResponse)
async def predict_price(request: PredictionRequest):
    """Predict cryptocurrency price (simulated)"""
    try:
        # Simple prediction based on recent trend
        if not request.historical_data:
            raise HTTPException(status_code=400, detail="Historical data required")
        
        # Calculate simple moving average
        recent_prices = [d['price'] for d in request.historical_data[:10]]
        if len(recent_prices) < 2:
            raise HTTPException(status_code=400, detail="Insufficient historical data")
        
        current_price = recent_prices[0]
        avg_price = sum(recent_prices) / len(recent_prices)
        
        # Simple trend-based prediction
        trend = (current_price - avg_price) / avg_price
        predicted_price = current_price * (1 + trend * 0.1)  # 10% of trend
        
        return PredictionResponse(
            symbol=request.symbol,
            predicted_price=round(predicted_price, 2),
            confidence=0.75,  # Simulated confidence
            timestamp=datetime.utcnow().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error making prediction: {e}")
        raise HTTPException(status_code=500, detail="Failed to make prediction")

# Market analytics
@app.get("/api/analytics/market")
async def get_market_analytics():
    """Get market analytics"""
    try:
        prices = get_latest_prices_from_db()
        
        if not prices:
            return {
                "total_market_cap": 0,
                "total_volume_24h": 0,
                "top_gainers": [],
                "top_losers": [],
                "crypto_count": 0
            }
        
        # Calculate analytics
        total_market_cap = sum(p['market_cap'] for p in prices.values())
        total_volume = sum(p['volume_24h'] for p in prices.values())
        
        # Sort by 24h change
        sorted_cryptos = sorted(
            prices.items(),
            key=lambda x: x[1]['price_change_24h'],
            reverse=True
        )
        
        top_gainers = sorted_cryptos[:3]
        top_losers = sorted_cryptos[-3:]
        
        return {
            "total_market_cap": total_market_cap,
            "total_volume_24h": total_volume,
            "top_gainers": [
                {
                    "symbol": symbol,
                    "change_24h": data['price_change_24h'],
                    "price": data['price_usd']
                }
                for symbol, data in top_gainers
            ],
            "top_losers": [
                {
                    "symbol": symbol,
                    "change_24h": data['price_change_24h'],
                    "price": data['price_usd']
                }
                for symbol, data in top_losers
            ],
            "crypto_count": len(prices)
        }
        
    except Exception as e:
        logger.error(f"Error getting market analytics: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch market analytics")

# Cache refresh endpoint
@app.post("/api/cache/refresh")
async def refresh_cache(background_tasks: BackgroundTasks):
    """Refresh cache"""
    try:
        # Clear cache
        cache.clear()
        
        # Fetch fresh data
        background_tasks.add_task(update_cache)
        
        return {"message": "Cache refresh initiated"}
        
    except Exception as e:
        logger.error(f"Error refreshing cache: {e}")
        raise HTTPException(status_code=500, detail="Failed to refresh cache")

async def update_cache():
    """Update cache with fresh data"""
    try:
        prices = get_latest_prices_from_db()
        cache["latest_prices"] = {
            'data': prices,
            'timestamp': time.time()
        }
        logger.info("Cache updated")
    except Exception as e:
        logger.error(f"Error updating cache: {e}")

# Startup event handlers are now handled by lifespan

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 