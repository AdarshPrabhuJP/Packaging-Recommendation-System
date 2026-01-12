from flask import Blueprint, request
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from app.models import MLModels
from app.utils import success_response, error_response, validate_product_input, calculate_environmental_score
from src.database_utils import get_all_materials, get_material_by_id
from src.ranking_system import MaterialRanker

api_bp = Blueprint('api', __name__)

ml_models = None
material_ranker = None

def init_models():
    global ml_models, material_ranker
    if ml_models is None:
        ml_models = MLModels()
    if material_ranker is None:
        material_ranker = MaterialRanker()

@api_bp.route('/recommend', methods=['POST'])
def recommend_materials():
    init_models()
    
    try:
        data = request.get_json()
        
        is_valid, error_msg = validate_product_input(data)
        if not is_valid:
            return error_response(error_msg, 400)
        
        priority = data.get('priority', 'balanced')
        top_n = data.get('top_n', 5)
        
        requirements = {
            'eco_priority': priority,
            'product_weight': data['product_weight'],
            'product_fragility': data['product_fragility'],
            'shipping_distance': data['shipping_distance']
        }
        
        rankings = material_ranker.rank_materials(requirements, top_n)
        
        return success_response({
            "recommendations": rankings,
            "count": len(rankings)
        })
    
    except Exception as e:
        return error_response(str(e), 500)

@api_bp.route('/predict/cost', methods=['POST'])
def predict_cost():
    init_models()
    
    try:
        data = request.get_json()
        
        features = ml_models.prepare_features(data)
        predicted_cost = ml_models.predict_cost(features)
        
        return success_response({
            "predicted_cost": round(predicted_cost, 2),
            "currency": "INR"
        })
    
    except Exception as e:
        return error_response(str(e), 500)

@api_bp.route('/predict/co2', methods=['POST'])
def predict_co2():
    init_models()
    
    try:
        data = request.get_json()
        
        features = ml_models.prepare_features(data)
        predicted_co2 = ml_models.predict_co2(features)
        
        return success_response({
            "predicted_co2": round(predicted_co2, 3),
            "unit": "kg"
        })
    
    except Exception as e:
        return error_response(str(e), 500)

@api_bp.route('/materials', methods=['GET'])
def get_materials():
    try:
        materials = get_all_materials()
        
        materials_list = []
        for m in materials:
            materials_list.append({
                "id": m[0],
                "material_type": m[1],
                "cost_per_unit": float(m[2]),
                "durability_score": m[3],
                "co2_footprint": float(m[4]),
                "biodegradability_score": m[5],
                "recyclable": m[6],
                "product_weight": m[7],
                "product_fragility": m[8],
                "shipping_distance": m[9],
                "recommended_use": m[10]
            })
        
        return success_response({
            "materials": materials_list,
            "count": len(materials_list)
        })
    
    except Exception as e:
        return error_response(str(e), 500)

@api_bp.route('/materials/<int:material_id>', methods=['GET'])
def get_material(material_id):
    try:
        material = get_material_by_id(material_id)
        
        if not material:
            return error_response("Material not found", 404)
        
        material_dict = {
            "id": material[0],
            "material_type": material[1],
            "cost_per_unit": float(material[2]),
            "durability_score": material[3],
            "co2_footprint": float(material[4]),
            "biodegradability_score": material[5],
            "recyclable": material[6],
            "product_weight": material[7],
            "product_fragility": material[8],
            "shipping_distance": material[9],
            "recommended_use": material[10]
        }
        
        return success_response({"material": material_dict})
    
    except Exception as e:
        return error_response(str(e), 500)

@api_bp.route('/environmental-score', methods=['POST'])
def environmental_score():
    try:
        data = request.get_json()
        
        material_id = data.get('material_id')
        if material_id:
            material = get_material_by_id(material_id)
            if not material:
                return error_response("Material not found", 404)
            
            co2 = float(material[4])
            biodegradability = material[5]
            recyclable = material[6]
            material_name = material[1]
        else:
            co2 = data.get('co2_footprint', 0)
            biodegradability = data.get('biodegradability_score', 5)
            recyclable = data.get('recyclable', False)
            material_name = data.get('material_type', 'Unknown')
        
        env_score = calculate_environmental_score(co2, biodegradability, recyclable)
        
        co2_score = max(0, 100 - (co2 / 3.5 * 100))
        bio_score = biodegradability * 10
        recycle_score = 100 if recyclable else 0
        
        return success_response({
            "material": material_name,
            "environmental_score": env_score,
            "breakdown": {
                "co2_score": round(co2_score, 2),
                "biodegradability_score": round(bio_score, 2),
                "recyclability_score": recycle_score
            }
        })
    
    except Exception as e:
        return error_response(str(e), 500)

@api_bp.route('/health', methods=['GET'])
def health_check():
    return success_response({"status": "healthy"}, "API is running")
