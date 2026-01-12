import requests
import json

BASE_URL = "http://localhost:5000/api"

print("="*60)
print("TESTING RECOMMENDATION VARIATIONS")
print("="*60)

# Test 1: Light, low fragility, eco priority
print("\n" + "-"*60)
print("TEST 1: Light product, low fragility, eco priority")
print("-"*60)
response1 = requests.post(f"{BASE_URL}/recommend", json={
    "product_weight": 100,
    "product_fragility": 2,
    "shipping_distance": 200,
    "priority": "eco",
    "top_n": 3
})
data1 = response1.json()
print("Top 3 recommendations:")
for rec in data1['recommendations']:
    print(f"  {rec['rank']}. {rec['material']} - Score: {rec['score']:.3f}")

# Test 2: Heavy, high fragility, budget priority
print("\n" + "-"*60)
print("TEST 2: Heavy product, high fragility, budget priority")
print("-"*60)
response2 = requests.post(f"{BASE_URL}/recommend", json={
    "product_weight": 5000,
    "product_fragility": 5,
    "shipping_distance": 1000,
    "priority": "low",
    "top_n": 3
})
data2 = response2.json()
print("Top 3 recommendations:")
for rec in data2['recommendations']:
    print(f"  {rec['rank']}. {rec['material']} - Score: {rec['score']:.3f}")

# Test 3: Medium, balanced
print("\n" + "-"*60)
print("TEST 3: Medium product, balanced priority")
print("-"*60)
response3 = requests.post(f"{BASE_URL}/recommend", json={
    "product_weight": 500,
    "product_fragility": 3,
    "shipping_distance": 500,
    "priority": "balanced",
    "top_n": 3
})
data3 = response3.json()
print("Top 3 recommendations:")
for rec in data3['recommendations']:
    print(f"  {rec['rank']}. {rec['material']} - Score: {rec['score']:.3f}")

# Compare results
print("\n" + "="*60)
print("COMPARISON")
print("="*60)
print(f"Test 1 Top Material: {data1['recommendations'][0]['material']}")
print(f"Test 2 Top Material: {data2['recommendations'][0]['material']}")
print(f"Test 3 Top Material: {data3['recommendations'][0]['material']}")

if (data1['recommendations'][0]['material'] != data2['recommendations'][0]['material'] or
    data2['recommendations'][0]['material'] != data3['recommendations'][0]['material']):
    print("\n✓ SUCCESS: Recommendations vary based on inputs!")
else:
    print("\n✗ ISSUE: All recommendations are the same")
