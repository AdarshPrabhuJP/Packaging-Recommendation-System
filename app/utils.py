from flask import jsonify

def success_response(data, message="Success"):
    return jsonify({
        "status": "success",
        "message": message,
        **data
    })

def error_response(message, status_code=400):
    response = jsonify({
        "status": "error",
        "message": message
    })
    response.status_code = status_code
    return response

def validate_product_input(data):
    required_fields = ['product_weight', 'product_fragility', 'shipping_distance']
    
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    
    if not (0 < data['product_weight'] <= 10000):
        return False, "Product weight must be between 0 and 10000 grams"
    
    if not (1 <= data['product_fragility'] <= 5):
        return False, "Product fragility must be between 1 and 5"
    
    if not (0 < data['shipping_distance'] <= 10000):
        return False, "Shipping distance must be between 0 and 10000 km"
    
    return True, None

def calculate_environmental_score(co2, biodegradability, recyclable):
    co2_score = max(0, 100 - (co2 / 3.5 * 100))
    bio_score = biodegradability * 10
    recycle_score = 100 if recyclable else 0
    
    environmental_score = (
        0.5 * co2_score +
        0.3 * bio_score +
        0.2 * recycle_score
    )
    
    return round(environmental_score, 2)
