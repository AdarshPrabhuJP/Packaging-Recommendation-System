"""
Data import script for PostgreSQL database.
Imports data from CSV files into the materials and autoliv_materials tables.
"""

import os
import sys
from pathlib import Path
import pandas as pd

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).parent.parent))

from database.config import get_db_connection


def import_materials_data():
    """
    Import data from ecopack_dataset.csv into the materials table.
    """
    print("\n" + "=" * 60)
    print("Importing Materials Data (ecopack_dataset.csv)")
    print("=" * 60)
    
    # Path to CSV file
    csv_file = Path(__file__).parent.parent / 'Data' / 'ecopack_dataset.csv'
    
    if not csv_file.exists():
        print(f"✗ Error: CSV file not found at {csv_file}")
        return False
    
    try:
        # Read CSV
        print("\n[1/4] Reading CSV file...")
        df = pd.read_csv(csv_file)
        print(f"✓ Loaded {len(df)} rows from CSV")
        
        # Convert 'yes'/'no' to boolean
        print("\n[2/4] Processing data...")
        df['recyclable'] = df['recyclable'].str.lower().map({'yes': True, 'no': False})
        print("✓ Data processed successfully")
        
        # Connect to database
        print("\n[3/4] Connecting to database...")
        conn = get_db_connection()
        cur = conn.cursor()
        print("✓ Connected successfully")
        
        # Insert data
        print("\n[4/4] Inserting data into materials table...")
        insert_query = """
            INSERT INTO materials (
                material_type, cost_per_unit, durability_score, co2_footprint,
                biodegradability_score, recyclable, product_weight, product_fragility,
                shipping_distance, recommended_use
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        inserted_count = 0
        for _, row in df.iterrows():
            cur.execute(insert_query, (
                row['material_type'],
                row['cost_per_unit'],
                row['durability_score'],
                row['co2_footprint'],
                row['biodegradability_score'],
                row['recyclable'],
                row['product_weight'],
                row['product_fragility'],
                row['shipping_distance'],
                row['recommended_use']
            ))
            inserted_count += 1
        
        conn.commit()
        print(f"✓ Successfully inserted {inserted_count} rows into materials table")
        
        # Verify insertion
        cur.execute("SELECT COUNT(*) FROM materials;")
        total_count = cur.fetchone()[0]
        print(f"✓ Total rows in materials table: {total_count}")
        
        cur.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("✓ Materials data import completed successfully!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n✗ Error during materials data import: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False


def import_autoliv_data():
    """
    Import data from Detailed_Autoliv_Sustainable_Packaging_Dataset.csv 
    into the autoliv_materials table.
    """
    print("\n" + "=" * 60)
    print("Importing Autoliv Materials Data")
    print("=" * 60)
    
    # Path to CSV file
    csv_file = Path(__file__).parent.parent / 'Data' / 'Detailed_Autoliv_Sustainable_Packaging_Dataset.csv'
    
    if not csv_file.exists():
        print(f"✗ Error: CSV file not found at {csv_file}")
        return False
    
    try:
        # Read CSV
        print("\n[1/4] Reading CSV file...")
        df = pd.read_csv(csv_file)
        print(f"✓ Loaded {len(df)} rows from CSV")
        
        # Process data
        print("\n[2/4] Processing data...")
        print("✓ Data processed successfully")
        
        # Connect to database
        print("\n[3/4] Connecting to database...")
        conn = get_db_connection()
        cur = conn.cursor()
        print("✓ Connected successfully")
        
        # Insert data
        print("\n[4/4] Inserting data into autoliv_materials table...")
        insert_query = """
            INSERT INTO autoliv_materials (
                packaging_type, material_type, recyclability_pct, reusability_pct,
                carbon_footprint, waste_reduction_impact_pct, 
                supplier_sustainability_compliance_pct, cost_per_unit,
                annual_usage, total_material_weight, recycled_content_pct,
                end_of_life_disposal_pct, sustainability_target_progress_pct
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        inserted_count = 0
        for _, row in df.iterrows():
            cur.execute(insert_query, (
                row['Packaging Type'],
                row['Material Type'],
                row['Recyclability (%)'],
                row['Reusability (%)'],
                row['Carbon Footprint (kg CO2/unit)'],
                row['Waste Reduction Impact (%)'],
                row['Supplier Sustainability Compliance (%)'],
                row['Cost per Unit (USD)'],
                row['Annual Usage (units)'],
                row['Total Material Weight (tons)'],
                row['Recycled Content (%)'],
                row['End-of-Life Disposal (%)'],
                row['Sustainability Target Progress (%)']
            ))
            inserted_count += 1
        
        conn.commit()
        print(f"✓ Successfully inserted {inserted_count} rows into autoliv_materials table")
        
        # Verify insertion
        cur.execute("SELECT COUNT(*) FROM autoliv_materials;")
        total_count = cur.fetchone()[0]
        print(f"✓ Total rows in autoliv_materials table: {total_count}")
        
        cur.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("✓ Autoliv materials data import completed successfully!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n✗ Error during Autoliv data import: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False


def main():
    """
    Main function to import all data.
    """
    print("\n" + "=" * 60)
    print("DATA IMPORT SCRIPT")
    print("Packaging Recommendation System")
    print("=" * 60)
    
    # Import materials data
    materials_success = import_materials_data()
    
    # Import autoliv data
    autoliv_success = import_autoliv_data()
    
    # Summary
    print("\n" + "=" * 60)
    print("IMPORT SUMMARY")
    print("=" * 60)
    print(f"Materials data: {'✓ SUCCESS' if materials_success else '✗ FAILED'}")
    print(f"Autoliv data: {'✓ SUCCESS' if autoliv_success else '✗ FAILED'}")
    
    if materials_success and autoliv_success:
        print("\n✓ All data imported successfully!")
        print("=" * 60)
        return True
    else:
        print("\n✗ Some imports failed. Please check the errors above.")
        print("=" * 60)
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
