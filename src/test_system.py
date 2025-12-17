"""
Testing Script for Packaging Recommendation System
Demonstrates that all modules work correctly with test cases
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from src.database_utils import get_all_materials, get_database_statistics
from src.feature_engineering import calculate_co2_impact_index, calculate_cost_efficiency_index
from src.data_validation import check_missing_values, detect_outliers, validate_ranges
from src.data_cleaning import normalize_materials_data, encode_categorical_variables


def test_database_connection():
    """Test 1: Database Connection"""
    print("\n" + "="*60)
    print("TEST 1: DATABASE CONNECTION")
    print("="*60)
    
    try:
        materials = get_all_materials()
        print(f"✅ PASS: Successfully connected to database")
        print(f"   Retrieved {len(materials)} materials")
        return True
    except Exception as e:
        print(f"❌ FAIL: Database connection failed - {e}")
        return False


def test_data_completeness():
    """Test 2: Data Completeness (No Missing Values)"""
    print("\n" + "="*60)
    print("TEST 2: DATA COMPLETENESS")
    print("="*60)
    
    try:
        missing_report = check_missing_values()
        total_missing = sum(missing_report['missing_values'].values())
        
        if total_missing == 0:
            print(f"✅ PASS: No missing values found")
            print(f"   Dataset is 100% complete")
            return True
        else:
            print(f"❌ FAIL: Found {total_missing} missing values")
            return False
    except Exception as e:
        print(f"❌ FAIL: Test failed - {e}")
        return False


def test_data_validation():
    """Test 3: Data Range Validation"""
    print("\n" + "="*60)
    print("TEST 3: DATA RANGE VALIDATION")
    print("="*60)
    
    try:
        range_report = validate_ranges()
        
        if range_report['valid']:
            print(f"✅ PASS: All values within valid ranges")
            print(f"   - Durability scores: 0-10 ✓")
            print(f"   - Biodegradability scores: 0-10 ✓")
            print(f"   - Cost values: Non-negative ✓")
            print(f"   - CO₂ values: Non-negative ✓")
            return True
        else:
            print(f"❌ FAIL: Found {len(range_report['violations'])} violations")
            for violation in range_report['violations']:
                print(f"   - {violation['field']}: {violation['issue']}")
            return False
    except Exception as e:
        print(f"❌ FAIL: Test failed - {e}")
        return False


def test_feature_engineering():
    """Test 4: Feature Engineering Calculations"""
    print("\n" + "="*60)
    print("TEST 4: FEATURE ENGINEERING")
    print("="*60)
    
    try:
        # Test with sample material
        test_material = {
            'co2_footprint': 1.5,
            'biodegradability_score': 8,
            'recyclable': True,
            'cost_per_unit': 10.0,
            'durability_score': 7
        }
        
        co2_index = calculate_co2_impact_index(
            test_material['co2_footprint'],
            test_material['biodegradability_score'],
            test_material['recyclable']
        )
        
        cost_index = calculate_cost_efficiency_index(
            test_material['cost_per_unit'],
            test_material['biodegradability_score'],
            test_material['durability_score'],
            test_material['recyclable']
        )
        
        # Verify indices are in valid range (0-100)
        if 0 <= co2_index <= 100 and 0 <= cost_index <= 100:
            print(f"✅ PASS: Feature calculations working correctly")
            print(f"   Sample Material:")
            print(f"   - CO₂ Impact Index: {co2_index:.1f}/100")
            print(f"   - Cost Efficiency Index: {cost_index:.1f}/100")
            return True
        else:
            print(f"❌ FAIL: Indices out of range")
            return False
    except Exception as e:
        print(f"❌ FAIL: Test failed - {e}")
        return False


def test_normalization():
    """Test 5: Data Normalization"""
    print("\n" + "="*60)
    print("TEST 5: DATA NORMALIZATION")
    print("="*60)
    
    try:
        normalized_data = normalize_materials_data()
        
        # Check that normalized values are between 0 and 1
        sample = normalized_data[0]
        
        checks = [
            ('cost_normalized', sample['cost_normalized']),
            ('durability_normalized', sample['durability_normalized']),
            ('co2_normalized', sample['co2_normalized'])
        ]
        
        all_valid = all(0 <= value <= 1 for _, value in checks)
        
        if all_valid:
            print(f"✅ PASS: Normalization working correctly")
            print(f"   Sample normalized values:")
            for name, value in checks:
                print(f"   - {name}: {value:.3f} (0-1 range ✓)")
            return True
        else:
            print(f"❌ FAIL: Normalized values out of range")
            return False
    except Exception as e:
        print(f"❌ FAIL: Test failed - {e}")
        return False


def test_categorical_encoding():
    """Test 6: Categorical Variable Encoding"""
    print("\n" + "="*60)
    print("TEST 6: CATEGORICAL ENCODING")
    print("="*60)
    
    try:
        encodings = encode_categorical_variables()
        
        material_types = len(encodings['material_type'])
        recommended_uses = len(encodings['recommended_use'])
        
        if material_types > 0 and recommended_uses > 0:
            print(f"✅ PASS: Categorical encoding working correctly")
            print(f"   - Material types encoded: {material_types}")
            print(f"   - Recommended uses encoded: {recommended_uses}")
            return True
        else:
            print(f"❌ FAIL: Encoding failed")
            return False
    except Exception as e:
        print(f"❌ FAIL: Test failed - {e}")
        return False


def test_database_statistics():
    """Test 7: Database Statistics Calculation"""
    print("\n" + "="*60)
    print("TEST 7: DATABASE STATISTICS")
    print("="*60)
    
    try:
        stats = get_database_statistics()
        
        required_keys = ['total_materials', 'recyclable_materials', 'avg_cost', 'avg_co2']
        
        if all(key in stats for key in required_keys):
            print(f"✅ PASS: Statistics calculated correctly")
            print(f"   - Total materials: {stats['total_materials']}")
            print(f"   - Recyclable: {stats['recyclable_materials']} ({stats['recyclable_percentage']:.1f}%)")
            print(f"   - Average cost: ${stats['avg_cost']:.2f}")
            print(f"   - Average CO₂: {stats['avg_co2']:.2f}")
            return True
        else:
            print(f"❌ FAIL: Missing statistics")
            return False
    except Exception as e:
        print(f"❌ FAIL: Test failed - {e}")
        return False


def run_all_tests():
    """Run all test cases"""
    print("\n" + "="*60)
    print("PACKAGING RECOMMENDATION SYSTEM - TEST SUITE")
    print("="*60)
    print("Running comprehensive tests for Module 1 & 2...")
    
    tests = [
        ("Database Connection", test_database_connection),
        ("Data Completeness", test_data_completeness),
        ("Data Validation", test_data_validation),
        ("Feature Engineering", test_feature_engineering),
        ("Data Normalization", test_normalization),
        ("Categorical Encoding", test_categorical_encoding),
        ("Database Statistics", test_database_statistics)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ CRITICAL ERROR in {test_name}: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print("\n" + "="*60)
    print(f"RESULTS: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
    print("="*60)
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! System is working correctly.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review above.")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
