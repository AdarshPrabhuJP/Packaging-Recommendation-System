"""
Data Validation Module
Validates data quality and detects issues in the packaging materials database.
"""

import sys
from pathlib import Path
import json
from datetime import datetime

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from src.database_utils import get_all_materials
from database.config import get_db_connection


def check_missing_values():
    """
    Check for missing or null values in the database.
    
    Returns:
        dict: Missing value report
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Check materials table
    cur.execute("""
        SELECT 
            COUNT(*) as total_rows,
            COUNT(material_type) as material_type_count,
            COUNT(cost_per_unit) as cost_count,
            COUNT(durability_score) as durability_count,
            COUNT(co2_footprint) as co2_count,
            COUNT(biodegradability_score) as biodegradability_count,
            COUNT(recyclable) as recyclable_count,
            COUNT(product_weight) as weight_count,
            COUNT(product_fragility) as fragility_count,
            COUNT(shipping_distance) as shipping_count,
            COUNT(recommended_use) as use_count
        FROM materials;
    """)
    
    result = cur.fetchone()
    total_rows = result[0]
    
    missing_report = {
        'total_records': total_rows,
        'missing_values': {},
        'completeness_percentage': {}
    }
    
    columns = [
        'material_type', 'cost_per_unit', 'durability_score', 'co2_footprint',
        'biodegradability_score', 'recyclable', 'product_weight', 
        'product_fragility', 'shipping_distance', 'recommended_use'
    ]
    
    for i, col in enumerate(columns):
        count = result[i + 1]
        missing = total_rows - count
        missing_report['missing_values'][col] = missing
        missing_report['completeness_percentage'][col] = round((count / total_rows) * 100, 2)
    
    cur.close()
    conn.close()
    
    return missing_report


def detect_outliers():
    """
    Detect statistical outliers using IQR (Interquartile Range) method.
    
    Returns:
        dict: Outlier detection report
    """
    materials = get_all_materials()
    
    # Extract numerical features
    costs = [float(m[2]) for m in materials if m[2]]
    durabilities = [m[3] for m in materials if m[3]]
    co2_values = [float(m[4]) for m in materials if m[4]]
    biodegradabilities = [m[5] for m in materials if m[5]]
    weights = [m[7] for m in materials if m[7]]
    shipping_distances = [m[9] for m in materials if m[9]]
    
    def find_outliers_iqr(data, name):
        """Find outliers using IQR method"""
        if not data:
            return {'outliers': [], 'count': 0}
        
        sorted_data = sorted(data)
        n = len(sorted_data)
        q1 = sorted_data[n // 4]
        q3 = sorted_data[(3 * n) // 4]
        iqr = q3 - q1
        
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        outliers = [x for x in data if x < lower_bound or x > upper_bound]
        
        return {
            'q1': q1,
            'q3': q3,
            'iqr': iqr,
            'lower_bound': round(lower_bound, 2),
            'upper_bound': round(upper_bound, 2),
            'outliers': outliers,
            'count': len(outliers)
        }
    
    outlier_report = {
        'cost_per_unit': find_outliers_iqr(costs, 'cost'),
        'durability_score': find_outliers_iqr(durabilities, 'durability'),
        'co2_footprint': find_outliers_iqr(co2_values, 'co2'),
        'biodegradability_score': find_outliers_iqr(biodegradabilities, 'biodegradability'),
        'product_weight': find_outliers_iqr(weights, 'weight'),
        'shipping_distance': find_outliers_iqr(shipping_distances, 'shipping')
    }
    
    return outlier_report


def validate_ranges():
    """
    Validate that values are within expected ranges.
    
    Returns:
        dict: Range validation report
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    validation_report = {
        'valid': True,
        'violations': []
    }
    
    # Check score ranges (should be 0-10)
    cur.execute("""
        SELECT id, material_type, durability_score 
        FROM materials 
        WHERE durability_score < 0 OR durability_score > 10;
    """)
    durability_violations = cur.fetchall()
    if durability_violations:
        validation_report['valid'] = False
        validation_report['violations'].append({
            'field': 'durability_score',
            'issue': 'Out of range (0-10)',
            'count': len(durability_violations)
        })
    
    cur.execute("""
        SELECT id, material_type, biodegradability_score 
        FROM materials 
        WHERE biodegradability_score < 0 OR biodegradability_score > 10;
    """)
    biodegradability_violations = cur.fetchall()
    if biodegradability_violations:
        validation_report['valid'] = False
        validation_report['violations'].append({
            'field': 'biodegradability_score',
            'issue': 'Out of range (0-10)',
            'count': len(biodegradability_violations)
        })
    
    # Check for negative costs
    cur.execute("""
        SELECT id, material_type, cost_per_unit 
        FROM materials 
        WHERE cost_per_unit < 0;
    """)
    cost_violations = cur.fetchall()
    if cost_violations:
        validation_report['valid'] = False
        validation_report['violations'].append({
            'field': 'cost_per_unit',
            'issue': 'Negative value',
            'count': len(cost_violations)
        })
    
    # Check for negative CO2
    cur.execute("""
        SELECT id, material_type, co2_footprint 
        FROM materials 
        WHERE co2_footprint < 0;
    """)
    co2_violations = cur.fetchall()
    if co2_violations:
        validation_report['valid'] = False
        validation_report['violations'].append({
            'field': 'co2_footprint',
            'issue': 'Negative value',
            'count': len(co2_violations)
        })
    
    cur.close()
    conn.close()
    
    return validation_report


def generate_validation_report():
    """
    Generate comprehensive validation report.
    
    Returns:
        dict: Complete validation report
    """
    print("=" * 60)
    print("DATA VALIDATION REPORT")
    print("=" * 60)
    
    # Missing values
    print("\n📊 Checking for missing values...")
    missing_report = check_missing_values()
    
    # Outliers
    print("🔍 Detecting outliers...")
    outlier_report = detect_outliers()
    
    # Range validation
    print("✓ Validating data ranges...")
    range_report = validate_ranges()
    
    # Compile full report
    full_report = {
        'timestamp': datetime.now().isoformat(),
        'missing_values': missing_report,
        'outliers': outlier_report,
        'range_validation': range_report,
        'overall_status': 'PASS' if range_report['valid'] and 
                         sum(missing_report['missing_values'].values()) == 0 else 'ISSUES_FOUND'
    }
    
    return full_report


def print_validation_summary(report):
    """Print human-readable validation summary"""
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    
    # Missing values
    print("\n📊 Missing Values:")
    missing = report['missing_values']
    total_missing = sum(missing['missing_values'].values())
    if total_missing == 0:
        print("  ✓ No missing values found")
    else:
        print(f"  ⚠ Found {total_missing} missing values:")
        for col, count in missing['missing_values'].items():
            if count > 0:
                print(f"    - {col}: {count} missing ({100 - missing['completeness_percentage'][col]:.1f}%)")
    
    # Outliers
    print("\n🔍 Outliers:")
    outliers = report['outliers']
    total_outliers = sum(o['count'] for o in outliers.values())
    if total_outliers == 0:
        print("  ✓ No outliers detected")
    else:
        print(f"  ⚠ Found {total_outliers} outliers:")
        for field, data in outliers.items():
            if data['count'] > 0:
                print(f"    - {field}: {data['count']} outliers")
                print(f"      Range: [{data['lower_bound']}, {data['upper_bound']}]")
    
    # Range validation
    print("\n✓ Range Validation:")
    range_val = report['range_validation']
    if range_val['valid']:
        print("  ✓ All values within expected ranges")
    else:
        print(f"  ⚠ Found {len(range_val['violations'])} violations:")
        for violation in range_val['violations']:
            print(f"    - {violation['field']}: {violation['issue']} ({violation['count']} records)")
    
    # Overall status
    print("\n" + "=" * 60)
    status = report['overall_status']
    if status == 'PASS':
        print("✅ OVERALL STATUS: PASS - Data quality is good!")
    else:
        print("⚠️  OVERALL STATUS: ISSUES FOUND - Review above")
    print("=" * 60)


if __name__ == "__main__":
    # Run validation
    report = generate_validation_report()
    
    # Print summary
    print_validation_summary(report)
    
    # Save to file
    output_file = Path(__file__).parent.parent / 'data_validation_report.json'
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Full report saved to: {output_file}")
