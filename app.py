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

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
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
