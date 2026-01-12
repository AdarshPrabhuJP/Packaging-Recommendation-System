import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_health():
    print("\n" + "="*60)
    print("TEST 1: Health Check")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_get_materials():
    print("\n" + "="*60)
    print("TEST 2: Get All Materials")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/materials")
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Total Materials: {data.get('count')}")
    print(f"First Material: {data['materials'][0]['material_type']}")
    return response.status_code == 200

def test_get_material_by_id():
    print("\n" + "="*60)
    print("TEST 3: Get Material by ID")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/materials/1")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_predict_cost():
    print("\n" + "="*60)
    print("TEST 4: Predict Cost")
    print("="*60)
    
    payload = {
        "cost_per_unit": 500,
        "durability_score": 8,
        "co2_footprint": 1.2,
        "biodegradability_score": 7,
        "product_weight": 200,
        "product_fragility": 3,
        "shipping_distance": 500,
        "recyclable": True
    }
    
    response = requests.post(f"{BASE_URL}/predict/cost", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_predict_co2():
    print("\n" + "="*60)
    print("TEST 5: Predict CO₂")
    print("="*60)
    
    payload = {
        "cost_per_unit": 500,
        "durability_score": 8,
        "co2_footprint": 1.2,
        "biodegradability_score": 7,
        "product_weight": 200,
        "product_fragility": 3,
        "shipping_distance": 500,
        "recyclable": True
    }
    
    response = requests.post(f"{BASE_URL}/predict/co2", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_recommend():
    print("\n" + "="*60)
    print("TEST 6: Get Recommendations")
    print("="*60)
    
    payload = {
        "product_weight": 200,
        "product_fragility": 5,
        "shipping_distance": 500,
        "priority": "eco",
        "top_n": 3
    }
    
    response = requests.post(f"{BASE_URL}/recommend", json=payload)
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Recommendations Count: {data.get('count')}")
    if 'recommendations' in data and len(data['recommendations']) > 0:
        print(f"\nTop Recommendation:")
        top = data['recommendations'][0]
        print(f"  Material: {top['material']}")
        print(f"  Score: {top['score']:.3f}")
        print(f"  Predicted Cost: ₹{top['predicted_cost']:.2f}")
        print(f"  Predicted CO₂: {top['predicted_co2']:.3f} kg")
    return response.status_code == 200

def test_environmental_score():
    print("\n" + "="*60)
    print("TEST 7: Environmental Score")
    print("="*60)
    
    payload = {
        "material_id": 1
    }
    
    response = requests.post(f"{BASE_URL}/environmental-score", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def run_all_tests():
    print("\n" + "="*60)
    print("FLASK API ENDPOINT TESTS")
    print("="*60)
    print(f"Testing API at: {BASE_URL}")
    
    tests = [
        ("Health Check", test_health),
        ("Get All Materials", test_get_materials),
        ("Get Material by ID", test_get_material_by_id),
        ("Predict Cost", test_predict_cost),
        ("Predict CO₂", test_predict_co2),
        ("Get Recommendations", test_recommend),
        ("Environmental Score", test_environmental_score)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\nERROR in {name}: {str(e)}")
            results.append((name, False))
    
    print("\n" + "="*60)
    print("TEST RESULTS SUMMARY")
    print("="*60)
    
    for name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status} - {name}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    print(f"\nTotal: {passed}/{total} tests passed")
    print("="*60)

if __name__ == "__main__":
    run_all_tests()
