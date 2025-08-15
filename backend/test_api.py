#!/usr/bin/env python3
"""
Simple test script to debug the API
"""

import sqlite3
import os

def test_db_connection():
    """Test database connection"""
    db_path = "../local_crypto.db"
    print(f"Database path: {db_path}")
    print(f"Database exists: {os.path.exists(db_path)}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM crypto_prices")
        count = cursor.fetchone()[0]
        print(f"Database has {count} records")
        
        cursor.execute("SELECT symbol, price_usd FROM crypto_prices LIMIT 3")
        rows = cursor.fetchall()
        print(f"Sample data: {rows}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"Database error: {e}")
        return False

def test_get_latest_prices():
    """Test the get_latest_prices_from_db function"""
    try:
        from app_local import get_latest_prices_from_db
        prices = get_latest_prices_from_db()
        print(f"API function returned {len(prices)} prices")
        if prices:
            print(f"Sample price: {list(prices.items())[0]}")
        return True
    except Exception as e:
        print(f"API function error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing database connection...")
    test_db_connection()
    
    print("\nTesting API function...")
    test_get_latest_prices() 