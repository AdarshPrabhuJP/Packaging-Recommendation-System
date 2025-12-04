"""
Database configuration module for PostgreSQL connection.
Handles database connection parameters and provides connection utilities.
"""

import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import pool

# Load environment variables from .env file
load_dotenv()


class DatabaseConfig:
    """Database configuration class to manage PostgreSQL connection settings."""
    
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.port = os.getenv('DB_PORT', '5432')
        self.database = os.getenv('DB_NAME', 'packaging_recommendation_db')
        self.user = os.getenv('DB_USER', 'postgres')
        self.password = os.getenv('DB_PASSWORD', '')
    
    def get_connection_params(self):
        """Return database connection parameters as a dictionary."""
        return {
            'host': self.host,
            'port': self.port,
            'database': self.database,
            'user': self.user,
            'password': self.password
        }
    
    def get_connection_string(self):
        """Return database connection string."""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


def get_db_connection():
    """
    Create and return a new database connection.
    
    Returns:
        psycopg2.connection: PostgreSQL database connection
    
    Raises:
        psycopg2.Error: If connection fails
    """
    config = DatabaseConfig()
    try:
        conn = psycopg2.connect(**config.get_connection_params())
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        raise


def test_connection():
    """Test database connection and print status."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT version();')
        db_version = cur.fetchone()
        print(f"✓ Database connection successful!")
        print(f"PostgreSQL version: {db_version[0]}")
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False


if __name__ == "__main__":
    # Test the connection when running this file directly
    test_connection()
