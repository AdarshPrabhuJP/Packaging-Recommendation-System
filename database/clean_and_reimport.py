"""
Clean database and re-import corrected packaging dataset.
Removes non-packaging items and adds relevant shipping materials.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from database.config import get_db_connection


def clean_and_reimport():
    """
    Remove non-packaging items and import corrected dataset.
    """
    print("\n" + "=" * 60)
    print("CLEANING DATABASE - REMOVING NON-PACKAGING ITEMS")
    print("=" * 60)
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # List of non-packaging items to remove
        non_packaging_items = [
            'Palm Leaf Plates',
            'Beeswax Wraps',
            'Silicone Food Bags'
        ]
        
        print("\n[1/2] Removing non-packaging items...")
        removed_count = 0
        for item in non_packaging_items:
            cur.execute("DELETE FROM materials WHERE material_type = %s", (item,))
            if cur.rowcount > 0:
                print(f"  ✓ Removed: {item}")
                removed_count += cur.rowcount
        
        conn.commit()
        print(f"\n✓ Removed {removed_count} non-packaging items")
        
        # Check current count
        cur.execute("SELECT COUNT(*) FROM materials")
        current_count = cur.fetchone()[0]
        print(f"✓ Current materials in database: {current_count}")
        
        cur.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("✅ DATABASE CLEANED SUCCESSFULLY!")
        print("=" * 60)
        
        # Now import new packaging materials
        print("\n" + "=" * 60)
        print("IMPORTING NEW PACKAGING MATERIALS")
        print("=" * 60)
        
        import pandas as pd
        
        csv_file = Path(__file__).parent.parent / 'Data' / 'expanded_ecopack_dataset.csv'
        df = pd.read_csv(csv_file)
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Get existing materials
        cur.execute("SELECT DISTINCT material_type FROM materials")
        existing = {row[0] for row in cur.fetchall()}
        
        # Filter new materials
        new_materials = df[~df['Material Type'].isin(existing)]
        
        print(f"\n✓ Found {len(new_materials)} new materials to add")
        
        # Insert new materials
        insert_query = """
            INSERT INTO materials (
                material_type, cost_per_unit, durability_score, co2_footprint,
                biodegradability_score, recyclable, product_weight, product_fragility,
                shipping_distance, recommended_use
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        inserted = 0
        for _, row in new_materials.iterrows():
            cur.execute(insert_query, (
                row['Material Type'],
                row['Cost per Unit (₹)'],
                row['Durability Score (0-10)'],
                row['CO2 Footprint (kg)'],
                row['Biodegradability Score (0-10)'],
                row['Recyclable'],
                row['Product Weight (g)'],
                row['Product Fragility (1-5)'],
                row['Shipping Distance (km)'],
                row['Recommended Use']
            ))
            inserted += 1
        
        conn.commit()
        print(f"✓ Added {inserted} new packaging materials")
        
        # Final statistics
        cur.execute("""
            SELECT 
                COUNT(*) as total,
                COUNT(*) FILTER (WHERE recyclable = TRUE) as recyclable,
                ROUND(AVG(cost_per_unit)::numeric, 2) as avg_cost
            FROM materials
        """)
        stats = cur.fetchone()
        
        print("\n" + "=" * 60)
        print("FINAL DATABASE STATISTICS")
        print("=" * 60)
        print(f"Total packaging materials: {stats[0]}")
        print(f"Recyclable: {stats[1]} ({(stats[1]/stats[0]*100):.1f}%)")
        print(f"Average cost: ₹{stats[2]}")
        
        cur.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("✅ ALL DONE! Database contains only packaging materials")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False


if __name__ == "__main__":
    success = clean_and_reimport()
    sys.exit(0 if success else 1)
