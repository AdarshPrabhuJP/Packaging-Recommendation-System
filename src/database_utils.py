"""
Database utility functions for querying packaging materials.
Provides reusable functions for common database operations.
"""

import sys
from pathlib import Path

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).parent.parent))

from database.config import get_db_connection


def get_all_materials():
    """
    Fetch all materials from the database.
    
    Returns:
        list: List of tuples containing material data
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT id, material_type, cost_per_unit, durability_score, 
               co2_footprint, biodegradability_score, recyclable,
               product_weight, product_fragility, shipping_distance,
               recommended_use
        FROM materials
        ORDER BY material_type;
    """)
    
    results = cur.fetchall()
    cur.close()
    conn.close()
    
    return results


def get_material_by_id(material_id):
    """
    Fetch a specific material by ID.
    
    Args:
        material_id (int): Material ID
        
    Returns:
        tuple: Material data or None if not found
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT id, material_type, cost_per_unit, durability_score, 
               co2_footprint, biodegradability_score, recyclable,
               product_weight, product_fragility, shipping_distance,
               recommended_use
        FROM materials
        WHERE id = %s;
    """, (material_id,))
    
    result = cur.fetchone()
    cur.close()
    conn.close()
    
    return result


def get_materials_by_recyclability(recyclable=True):
    """
    Fetch materials filtered by recyclability.
    
    Args:
        recyclable (bool): True for recyclable materials, False for non-recyclable
        
    Returns:
        list: List of materials
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT id, material_type, cost_per_unit, durability_score, 
               co2_footprint, biodegradability_score, recyclable,
               product_weight, product_fragility, shipping_distance,
               recommended_use
        FROM materials
        WHERE recyclable = %s
        ORDER BY biodegradability_score DESC, co2_footprint ASC;
    """, (recyclable,))
    
    results = cur.fetchall()
    cur.close()
    conn.close()
    
    return results


def get_materials_by_cost_range(min_cost=0, max_cost=100):
    """
    Fetch materials within a cost range.
    
    Args:
        min_cost (float): Minimum cost per unit
        max_cost (float): Maximum cost per unit
        
    Returns:
        list: List of materials within cost range
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT id, material_type, cost_per_unit, durability_score, 
               co2_footprint, biodegradability_score, recyclable,
               product_weight, product_fragility, shipping_distance,
               recommended_use
        FROM materials
        WHERE cost_per_unit BETWEEN %s AND %s
        ORDER BY cost_per_unit ASC;
    """, (min_cost, max_cost))
    
    results = cur.fetchall()
    cur.close()
    conn.close()
    
    return results


def get_materials_by_sustainability(min_biodegradability=7, max_co2=1.5):
    """
    Fetch highly sustainable materials.
    
    Args:
        min_biodegradability (int): Minimum biodegradability score (0-10)
        max_co2 (float): Maximum CO2 footprint
        
    Returns:
        list: List of sustainable materials
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT id, material_type, cost_per_unit, durability_score, 
               co2_footprint, biodegradability_score, recyclable,
               product_weight, product_fragility, shipping_distance,
               recommended_use
        FROM materials
        WHERE biodegradability_score >= %s 
          AND co2_footprint <= %s
        ORDER BY biodegradability_score DESC, co2_footprint ASC;
    """, (min_biodegradability, max_co2))
    
    results = cur.fetchall()
    cur.close()
    conn.close()
    
    return results


def get_materials_by_use_case(use_case):
    """
    Fetch materials by recommended use case.
    
    Args:
        use_case (str): Recommended use (e.g., 'Electronics', 'Food')
        
    Returns:
        list: List of materials for the use case
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT id, material_type, cost_per_unit, durability_score, 
               co2_footprint, biodegradability_score, recyclable,
               product_weight, product_fragility, shipping_distance,
               recommended_use
        FROM materials
        WHERE recommended_use ILIKE %s
        ORDER BY biodegradability_score DESC;
    """, (f'%{use_case}%',))
    
    results = cur.fetchall()
    cur.close()
    conn.close()
    
    return results


def get_database_statistics():
    """
    Get summary statistics about the materials database.
    
    Returns:
        dict: Statistics including counts, averages, etc.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Total count
    cur.execute("SELECT COUNT(*) FROM materials;")
    total_count = cur.fetchone()[0]
    
    # Recyclable count
    cur.execute("SELECT COUNT(*) FROM materials WHERE recyclable = TRUE;")
    recyclable_count = cur.fetchone()[0]
    
    # Average metrics
    cur.execute("""
        SELECT 
            AVG(cost_per_unit) as avg_cost,
            AVG(co2_footprint) as avg_co2,
            AVG(biodegradability_score) as avg_biodegradability,
            AVG(durability_score) as avg_durability
        FROM materials;
    """)
    
    averages = cur.fetchone()
    
    cur.close()
    conn.close()
    
    return {
        'total_materials': total_count,
        'recyclable_materials': recyclable_count,
        'recyclable_percentage': (recyclable_count / total_count * 100) if total_count > 0 else 0,
        'avg_cost': float(averages[0]) if averages[0] else 0,
        'avg_co2': float(averages[1]) if averages[1] else 0,
        'avg_biodegradability': float(averages[2]) if averages[2] else 0,
        'avg_durability': float(averages[3]) if averages[3] else 0
    }


if __name__ == "__main__":
    # Test the functions
    print("=" * 60)
    print("DATABASE UTILITIES TEST")
    print("=" * 60)
    
    # Get statistics
    print("\n📊 Database Statistics:")
    stats = get_database_statistics()
    print(f"  Total materials: {stats['total_materials']}")
    print(f"  Recyclable: {stats['recyclable_materials']} ({stats['recyclable_percentage']:.1f}%)")
    print(f"  Avg cost: ${stats['avg_cost']:.2f}")
    print(f"  Avg CO₂: {stats['avg_co2']:.2f}")
    print(f"  Avg biodegradability: {stats['avg_biodegradability']:.1f}/10")
    print(f"  Avg durability: {stats['avg_durability']:.1f}/10")
    
    # Test recyclable materials
    print("\n♻️ Recyclable Materials:")
    recyclable = get_materials_by_recyclability(True)
    print(f"  Found {len(recyclable)} recyclable materials")
    
    # Test sustainable materials
    print("\n🌱 Highly Sustainable Materials (biodegradability ≥ 8, CO₂ ≤ 1.0):")
    sustainable = get_materials_by_sustainability(min_biodegradability=8, max_co2=1.0)
    for material in sustainable[:5]:  # Show top 5
        print(f"  - {material[1]}: Biodegradability={material[5]}, CO₂={material[4]}")
    
    print("\n✓ All tests completed successfully!")
