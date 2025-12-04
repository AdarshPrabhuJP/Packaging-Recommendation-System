"""
Database initialization script.
Creates tables and schema in PostgreSQL database.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).parent.parent))

from database.config import get_db_connection


def init_database():
    """
    Initialize the database by executing the schema.sql file.
    Creates all tables, indexes, and constraints.
    """
    print("=" * 60)
    print("Database Initialization Script")
    print("=" * 60)
    
    # Get the path to schema.sql
    schema_file = Path(__file__).parent / 'schema.sql'
    
    if not schema_file.exists():
        print(f"✗ Error: schema.sql not found at {schema_file}")
        return False
    
    try:
        # Connect to database
        print("\n[1/3] Connecting to database...")
        conn = get_db_connection()
        cur = conn.cursor()
        print("✓ Connected successfully")
        
        # Read and execute schema
        print("\n[2/3] Reading schema.sql...")
        with open(schema_file, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        print("✓ Schema file loaded")
        
        print("\n[3/3] Executing schema (creating tables, indexes, constraints)...")
        cur.execute(schema_sql)
        conn.commit()
        print("✓ Schema executed successfully")
        
        # Verify tables were created
        print("\n" + "=" * 60)
        print("Verifying table creation...")
        print("=" * 60)
        
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """)
        
        tables = cur.fetchall()
        if tables:
            print("\n✓ Tables created successfully:")
            for table in tables:
                print(f"  - {table[0]}")
                
                # Get row count
                cur.execute(f"SELECT COUNT(*) FROM {table[0]};")
                count = cur.fetchone()[0]
                print(f"    (currently {count} rows)")
        else:
            print("\n⚠ Warning: No tables found")
        
        # Close connection
        cur.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("✓ Database initialization completed successfully!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n✗ Error during database initialization: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False


if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)
