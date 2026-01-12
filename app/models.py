import sys
from pathlib import Path
import joblib
import numpy as np

sys.path.append(str(Path(__file__).parent.parent))
from app.config import Config

class MLModels:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MLModels, cls).__new__(cls)
            cls._instance._load_models()
        return cls._instance
    
    def _load_models(self):
        models_dir = Path(__file__).parent.parent / Config.MODELS_DIR
        
        self.cost_model = joblib.load(models_dir / Config.XGBOOST_COST_MODEL)
        self.co2_model = joblib.load(models_dir / Config.XGBOOST_CO2_MODEL)
        self.scaler = joblib.load(models_dir / Config.FEATURE_SCALER)
        
        print("✓ ML models loaded successfully")
    
    def predict_cost(self, features):
        features_scaled = self.scaler.transform(features)
        prediction = self.cost_model.predict(features_scaled)
        return float(prediction[0])
    
    def predict_co2(self, features):
        features_scaled = self.scaler.transform(features)
        prediction = self.co2_model.predict(features_scaled)
        return float(prediction[0])
    
    def prepare_features(self, data):
        features = [
            data.get('cost_per_unit', 0),
            data.get('durability_score', 5),
            data.get('co2_footprint', 0),
            data.get('biodegradability_score', 5),
            data.get('product_weight', 100),
            data.get('product_fragility', 3),
            data.get('shipping_distance', 100),
            int(data.get('recyclable', False))
        ]
        return np.array(features).reshape(1, -1)
