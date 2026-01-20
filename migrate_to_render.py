import psycopg2
import sys

# Render database URL
DATABASE_URL = "postgresql://packaging_recommendation_user:tGj1ljyuVPivgfC3TwK38LCuPhibytHi@dpg-d5l2eohr0fns738tlpv0-a.singapore-postgres.render.com/packaging_recommendation"

# Local database connection
LOCAL_DB = {
    'dbname': 'packaging_recommendation_db',
    'user': 'postgres',
    'password': 'PostgreSQL',
    'host': 'localhost',
    'port': '5432'
}

print("Connecting to local database...")
try:
    local_conn = psycopg2.connect(**LOCAL_DB)
    local_cur = local_conn.cursor()
    
    print("Fetching data from local database...")
    local_cur.execute("SELECT * FROM materials ORDER BY id;")
    materials = local_cur.fetchall()
    print(f"✓ Found {len(materials)} materials")
    
    local_cur.close()
    local_conn.close()
    
except Exception as e:
    print(f"Error connecting to local database: {e}")
    sys.exit(1)

print("\nConnecting to Render database...")
try:
    render_conn = psycopg2.connect(DATABASE_URL)
    render_cur = render_conn.cursor()
    
    print("Creating materials table...")
    render_cur.execute("""
        CREATE TABLE IF NOT EXISTS materials (
            id SERIAL PRIMARY KEY,
            material_type VARCHAR(100) NOT NULL,
            cost_per_unit DECIMAL(10,2) NOT NULL,
            durability_score INTEGER NOT NULL,
            co2_footprint DECIMAL(10,3) NOT NULL,
            biodegradability_score INTEGER NOT NULL,
            recyclable BOOLEAN NOT NULL,
            product_weight INTEGER NOT NULL,
            product_fragility INTEGER NOT NULL,
            shipping_distance INTEGER NOT NULL,
            recommended_use TEXT
        );
    """)
    render_conn.commit()
    print("✓ Table created")
    
    print("\nInserting materials...")
    inserted = 0
    for material in materials:
        try:
            render_cur.execute("""
                INSERT INTO materials (
                    id, material_type, cost_per_unit, durability_score,
                    co2_footprint, biodegradability_score, recyclable,
                    product_weight, product_fragility, shipping_distance,
                    recommended_use
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
            """, (material[0], material[1], material[2], material[3], material[4], 
                  material[5], material[6], material[7], material[8], material[9], material[10]))
            inserted += 1
        except Exception as e:
            print(f"Error inserting material {material[0]}: {e}")
    
    render_conn.commit()
    print(f"✓ Inserted {inserted} materials")
    
    render_cur.execute("SELECT COUNT(*) FROM materials;")
    count = render_cur.fetchone()[0]
    print(f"\n✅ Verification: {count} materials in Render database")
    
    render_cur.close()
    render_conn.close()
    
    print("\n🎉 Database migration complete!")
    
except Exception as e:
    print(f"Error with Render database: {e}")
    sys.exit(1)
