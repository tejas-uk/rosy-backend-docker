#!/usr/bin/env python3
"""
Check Database Schema
This script will show the current database schema.
"""

import os
from dotenv import load_dotenv
import psycopg

# Load environment variables
load_dotenv()

def check_schema():
    """Check the current database schema."""
    
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        print("❌ DATABASE_URL not found in environment variables")
        return False
    
    print(f"🔗 Connecting to database: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else DATABASE_URL}")
    
    try:
        # Connect to database
        with psycopg.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                print("📋 Checking user table schema...")
                
                # Check user table columns
                cur.execute("""
                    SELECT column_name, data_type, is_nullable, column_default
                    FROM information_schema.columns 
                    WHERE table_name = 'user'
                    ORDER BY ordinal_position;
                """)
                
                columns = cur.fetchall()
                print("\nUser table columns:")
                for col in columns:
                    print(f"  - {col[0]}: {col[1]} (nullable: {col[2]}, default: {col[3]})")
                
                print("\n📋 Checking chat table schema...")
                
                # Check chat table columns
                cur.execute("""
                    SELECT column_name, data_type, is_nullable, column_default
                    FROM information_schema.columns 
                    WHERE table_name = 'chat'
                    ORDER BY ordinal_position;
                """)
                
                columns = cur.fetchall()
                print("\nChat table columns:")
                for col in columns:
                    print(f"  - {col[0]}: {col[1]} (nullable: {col[2]}, default: {col[3]})")
        
        return True
        
    except Exception as e:
        print(f"❌ Schema check failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Checking database schema...")
    success = check_schema()
    
    if not success:
        exit(1) 