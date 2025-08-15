#!/usr/bin/env python3
"""
Test script to debug database connection and queries
"""

import sqlite3
from datetime import datetime

def test_database():
    """Test database connection and queries"""
    try:
        # Connect to database
        conn = sqlite3.connect('local_crypto.db')
        cursor = conn.cursor()
        
        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Tables: {tables}")
        
        # Check crypto_prices table
        cursor.execute("SELECT COUNT(*) FROM crypto_prices")
        count = cursor.fetchone()[0]
        print(f"Crypto prices count: {count}")
        
        # Get sample data
        cursor.execute("SELECT symbol, price_usd, market_cap FROM crypto_prices LIMIT 3")
        rows = cursor.fetchall()
        print(f"Sample data: {rows}")
        
        # Test the exact query from the API
        cursor.execute('SELECT * FROM crypto_prices')
        rows = cursor.fetchall()
        print(f"All data count: {len(rows)}")
        
        if rows:
            # Test the data structure
            row = rows[0]
            print(f"First row structure: {row}")
            print(f"Row length: {len(row)}")
            
            # Test creating the prices dict
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
            
            print(f"Prices dict created successfully with {len(prices)} entries")
            print(f"Sample price data: {list(prices.items())[0]}")
        
        conn.close()
        print("Database test completed successfully")
        
    except Exception as e:
        print(f"Error testing database: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_database() 