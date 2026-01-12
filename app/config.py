import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    DB_NAME = os.getenv('DB_NAME', 'packaging_db')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    
    MODELS_DIR = 'models'
    
    XGBOOST_COST_MODEL = 'xgboost_cost_model.pkl'
    XGBOOST_CO2_MODEL = 'xgboost_co2_model.pkl'
    FEATURE_SCALER = 'feature_scaler.pkl'
