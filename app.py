from app import create_app
from flask import render_template
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Auto-initialize database on startup
def init_database():
    try:
        from database.init_db import create_tables
        from database.import_data import import_materials_data
        print("Initializing database...")
        create_tables()
        import_materials_data()
        print("✓ Database initialized successfully")
    except Exception as e:
        print(f"Database initialization: {e}")

# Create Flask application instance
app = create_app()

# Initialize database on startup
if os.getenv('DATABASE_URL'):
    init_database()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/init-db')
def init_db_endpoint():
    """Manual database initialization endpoint"""
    try:
        import psycopg2
        import pandas as pd
        import os
        
        # Connect to database
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        cur = conn.cursor()
        
        # Create table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS materials (
                id SERIAL PRIMARY KEY,
                material_type VARCHAR(100),
                cost_per_unit DECIMAL,
                durability_score INTEGER,
                co2_footprint DECIMAL,
                biodegradability_score INTEGER,
                recyclable BOOLEAN,
                product_weight INTEGER,
                product_fragility INTEGER,
                shipping_distance INTEGER,
                recommended_use TEXT
            )
        ''')
        
        # Check if data exists
        cur.execute('SELECT COUNT(*) FROM materials')
        count = cur.fetchone()[0]
        
        if count == 0:
            # Load and insert sample data
            materials = [
                ('Cardboard', 45.50, 7, 0.85, 8, True, 500, 3, 200, 'General packaging'),
                ('Bubble Wrap', 120.75, 6, 2.10, 2, False, 100, 5, 150, 'Fragile items'),
                ('Paper Bags', 25.30, 4, 0.45, 9, True, 200, 2, 100, 'Light items'),
                ('Plastic Containers', 85.20, 9, 3.20, 1, False, 800, 4, 300, 'Liquid products'),
                ('Biodegradable Foam', 150.00, 8, 1.20, 9, True, 300, 4, 250, 'Eco-friendly packaging')
            ]
            
            for mat in materials:
                cur.execute('''
                    INSERT INTO materials (material_type, cost_per_unit, durability_score, 
                    co2_footprint, biodegradability_score, recyclable, product_weight, 
                    product_fragility, shipping_distance, recommended_use) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', mat)
        
        conn.commit()
        cur.close()
        conn.close()
        
        return f'Database initialized! {count} materials found, added sample data if empty.'
    except Exception as e:
        return f'Error: {str(e)}'

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
    print("\n" + "="*60)
    print("PACKAGING RECOMMENDATION SYSTEM")
    print("="*60)
    print("\nWeb Interface: http://localhost:5000")
    print("\nAPI Endpoints:")
    print("  POST   /api/recommend")
    print("  POST   /api/predict/cost")
    print("  POST   /api/predict/co2")
    print("  GET    /api/materials")
    print("  GET    /api/materials/<id>")
    print("  POST   /api/environmental-score")
    print("  GET    /api/health")
    print("\n" + "="*60)
    print("Starting server...")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
