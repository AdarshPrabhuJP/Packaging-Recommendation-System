import psycopg2
from psycopg2 import sql

# Render database URL
RENDER_DB = "postgresql://packaging_recommendation_user:tGj1ljyuVPivgfC3TwK38LCuPhibytHi@dpg-d5l2eohr0fns738tlpv0-a.oregon-postgres.render.com/packaging_recommendation"

# Local database - try without password first
try:
    LOCAL_DB = {
        'dbname': 'packaging_db',
        'user': 'postgres',
        'host': 'localhost',
        'port': '5432'
    }
except:
    # If that fails, try with empty password
    LOCAL_DB = {
        'dbname': 'packaging_db',
        'user': 'postgres',
        'password': '',
        'host': 'localhost',
        'port': '5432'
    }

print("🔄 Starting direct database import to Render...")

# Step 1: Connect to local database
print("\n1️⃣ Connecting to local database...")
local_conn = psycopg2.connect(**LOCAL_DB)
local_cur = local_conn.cursor()

# Step 2: Fetch all materials
print("2️⃣ Fetching materials from local database...")
local_cur.execute("SELECT * FROM materials ORDER BY material_id")
materials = local_cur.fetchall()
print(f"   ✓ Found {len(materials)} materials")

# Step 3: Connect to Render database
print("\n3️⃣ Connecting to Render database...")
render_conn = psycopg2.connect(RENDER_DB)
render_cur = render_conn.cursor()
print("   ✓ Connected to Render PostgreSQL")

# Step 4: Drop existing table if exists
print("\n4️⃣ Preparing database...")
render_cur.execute("DROP TABLE IF EXISTS materials CASCADE")
print("   ✓ Cleared existing data")

# Step 5: Create table
print("\n5️⃣ Creating materials table...")
render_cur.execute("""
    CREATE TABLE materials (
        material_id SERIAL PRIMARY KEY,
        material_name VARCHAR(100) NOT NULL,
        cost_per_unit DECIMAL(10, 2),
        co2_footprint DECIMAL(10, 3),
        durability INTEGER,
        recyclable BOOLEAN,
        biodegradable BOOLEAN,
        weight_capacity INTEGER,
        temperature_resistance INTEGER,
        moisture_resistance INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
print("   ✓ Table created")

# Step 6: Insert materials
print("\n6️⃣ Inserting materials...")
for i, material in enumerate(materials, 1):
    render_cur.execute("""
        INSERT INTO materials (
            material_name, cost_per_unit, co2_footprint, durability,
            recyclable, biodegradable, weight_capacity,
            temperature_resistance, moisture_resistance
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, material[1:10])  # Skip material_id and created_at
    
    if i % 10 == 0:
        print(f"   ✓ Inserted {i}/{len(materials)} materials...")

print(f"   ✓ All {len(materials)} materials inserted!")

# Step 7: Verify
print("\n7️⃣ Verifying import...")
render_cur.execute("SELECT COUNT(*) FROM materials")
count = render_cur.fetchone()[0]
print(f"   ✓ Verified: {count} materials in Render database")

# Commit and close
render_conn.commit()
local_cur.close()
local_conn.close()
render_cur.close()
render_conn.close()

print("\n🎉 Database import complete!")
print(f"✅ Successfully imported {count} materials to Render PostgreSQL")
print("\n🌐 Your website should now show all materials!")
print("   Visit: https://packaging-recommendation-system-nyqr.onrender.com")
