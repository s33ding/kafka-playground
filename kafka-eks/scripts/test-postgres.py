#!/usr/bin/env python3
import psycopg2
import subprocess
import time
import signal
import sys

def start_port_forward():
    """Start kubectl port-forward for PostgreSQL"""
    print("🐘 Starting PostgreSQL port forward...")
    proc = subprocess.Popen(['kubectl', 'port-forward', 'svc/postgres-service', '5432:5432'])
    time.sleep(2)  # Wait for port forward to be ready
    return proc

def test_postgres_connection():
    """Test PostgreSQL connection and run queries"""
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="testdb",
            user="postgres",
            password="postgres"
        )
        
        cursor = conn.cursor()
        
        print("✅ Connected to PostgreSQL!")
        
        # Test queries
        print("\n👥 Users:")
        cursor.execute("SELECT * FROM users;")
        for row in cursor.fetchall():
            print(f"  ID: {row[0]}, Name: {row[1]}, Email: {row[2]}")
        
        print("\n📦 Orders:")
        cursor.execute("SELECT * FROM orders;")
        for row in cursor.fetchall():
            print(f"  ID: {row[0]}, User ID: {row[1]}, Product: {row[2]}, Amount: ${row[3]}")
        
        # Insert test data
        print("\n➕ Inserting new user...")
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id;", 
                      ("Jane Smith", "jane@example.com"))
        new_user_id = cursor.fetchone()[0]
        print(f"  New user ID: {new_user_id}")
        
        cursor.execute("INSERT INTO orders (user_id, product, amount) VALUES (%s, %s, %s);",
                      (new_user_id, "Phone", 599.99))
        
        conn.commit()
        print("✅ Data inserted successfully!")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    pf_proc = None
    
    def cleanup(signum, frame):
        if pf_proc:
            pf_proc.terminate()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, cleanup)
    
    try:
        pf_proc = start_port_forward()
        test_postgres_connection()
    finally:
        if pf_proc:
            pf_proc.terminate()

if __name__ == "__main__":
    main()
