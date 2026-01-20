import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # Parse DATABASE_URL if available (for Render deployment)
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        url = urlparse(database_url)
        DB_NAME = url.path[1:]  # Remove leading slash
        DB_USER = url.username
        DB_PASSWORD = url.password
        DB_HOST = url.hostname
        DB_PORT = str(url.port) if url.port else '5432'
    else:
        # Fallback to individual environment variables (for local development)
        DB_NAME = os.getenv('DB_NAME', 'packaging_db')
        DB_USER = os.getenv('DB_USER', 'postgres')
        DB_PASSWORD = os.getenv('DB_PASSWORD', '')
        DB_HOST = os.getenv('DB_HOST', 'localhost')
        DB_PORT = os.getenv('DB_PORT', '5432')
    
    MODELS_DIR = 'models'
    
    XGBOOST_COST_MODEL = 'xgboost_cost_model.pkl'
    XGBOOST_CO2_MODEL = 'xgboost_co2_model.pkl'
    FEATURE_SCALER = 'feature_scaler.pkl'
