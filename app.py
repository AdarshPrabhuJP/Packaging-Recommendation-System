from app import create_app
from flask import render_template

app = create_app()

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
