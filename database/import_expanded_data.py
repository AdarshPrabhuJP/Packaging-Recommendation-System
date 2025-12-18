"""
Import expanded dataset (34 new materials) into existing database.
Adds to the current materials without deleting existing data.
"""

import sys
from pathlib import Path
import pandas as pd

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from database.config import get_db_connection


def import_expanded_data():
    """
    Import expanded dataset into materials table.
    Adds new materials to existing data.
    """
    print("\n" + "=" * 60)
    print("IMPORTING EXPANDED DATASET")
    print("=" * 60)
    
    # Path to new CSV file
    csv_file = Path(__file__).parent.parent / 'Data' / 'expanded_ecopack_dataset.csv'
    
    if not csv_file.exists():
        print(f"✗ Error: CSV file not found at {csv_file}")
        return False
    
    try:
        # Read CSV
        print("\n[1/5] Reading CSV file...")
        df = pd.read_csv(csv_file)
        print(f"✓ Loaded {len(df)} rows from CSV")
        
        # Connect to database
        print("\n[2/5] Connecting to database...")
        conn = get_db_connection()
        cur = conn.cursor()
        print("✓ Connected successfully")
        
        # Check current count
        print("\n[3/5] Checking current database...")
        cur.execute("SELECT COUNT(*) FROM materials;")
        before_count = cur.fetchone()[0]
        print(f"✓ Current materials in database: {before_count}")
        
        # Get existing material types to avoid duplicates
        cur.execute("SELECT DISTINCT material_type FROM materials;")
        existing_materials = {row[0] for row in cur.fetchall()}
        print(f"✓ Found {len(existing_materials)} unique material types")
        
        # Filter out duplicates
        print("\n[4/5] Processing data...")
        new_materials = df[~df['Material Type'].isin(existing_materials)]
        duplicate_count = len(df) - len(new_materials)
        
        if duplicate_count > 0:
            print(f"⚠ Skipping {duplicate_count} duplicate materials")
        print(f"✓ {len(new_materials)} new materials to import")
        
        # Insert new data
        print("\n[5/5] Inserting new materials...")
        insert_query = """
            INSERT INTO materials (
                material_type, cost_per_unit, durability_score, co2_footprint,
                biodegradability_score, recyclable, product_weight, product_fragility,
                shipping_distance, recommended_use
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        inserted_count = 0
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
            inserted_count += 1
        
        conn.commit()
        print(f"✓ Successfully inserted {inserted_count} new materials")
        
        # Verify final count
        cur.execute("SELECT COUNT(*) FROM materials;")
        after_count = cur.fetchone()[0]
        print(f"✓ Total materials in database: {after_count}")
        print(f"✓ Added: {after_count - before_count} materials")
        
        # Show statistics
        cur.execute("""
            SELECT 
                COUNT(*) as total,
                COUNT(*) FILTER (WHERE recyclable = TRUE) as recyclable,
                ROUND(AVG(cost_per_unit)::numeric, 2) as avg_cost,
                ROUND(AVG(co2_footprint)::numeric, 2) as avg_co2
            FROM materials;
        """)
        stats = cur.fetchone()
        
        print("\n" + "=" * 60)
        print("DATABASE STATISTICS")
        print("=" * 60)
        print(f"Total materials: {stats[0]}")
        print(f"Recyclable: {stats[1]} ({(stats[1]/stats[0]*100):.1f}%)")
        print(f"Average cost: ₹{stats[2]}")
        print(f"Average CO₂: {stats[3]} kg")
        
        cur.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("✅ IMPORT COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n✗ Error during import: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False


if __name__ == "__main__":
    success = import_expanded_data()
    sys.exit(0 if success else 1)
