# Packaging Recommendation System

An intelligent ML-based web application for recommending optimal packaging materials based on product characteristics, cost, and environmental impact.

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-black.svg)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)](https://www.postgresql.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3.2-orange.svg)](https://scikit-learn.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0.3-green.svg)](https://xgboost.readthedocs.io/)

---

## 🌐 Live Demo

**🚀 [View Live Application](https://packaging-recommendation-system-nyqr.onrender.com)**

---

## ✨ Features

### **Core Functionality**
- 🎯 **61 Packaging Materials Database** - Comprehensive material catalog
- 🤖 **ML-Powered Recommendations** - Random Forest & XGBoost models (96-98% accuracy)
- 📊 **BI Analytics Dashboard** - Real-time insights and visualizations
- 📄 **PDF Export** - Professional sustainability reports
- 📊 **Excel Export** - Multi-sheet data exports for analysis
- 🏷️ **Product Category Filters** - Food, Electronics, Gifts, Cosmetics, etc.
- 💰 **Cost Analysis** - Compare material costs with interactive charts
- 🌱 **Environmental Impact** - CO₂ footprint tracking and analysis

### **Web Interface**
- Clean, professional UI with green eco-theme
- Real-time material recommendations
- Interactive charts (Chart.js)
- Responsive design for all devices

### **API Endpoints**
- RESTful API for programmatic access
- JSON responses
- Health check endpoint
- Material database queries

---

## 🎯 Overview

This system uses machine learning to recommend the most suitable packaging materials by analyzing cost, durability, environmental impact, and product requirements. It employs Random Forest and XGBoost algorithms with an intelligent ranking system.

**Use Cases:**
- E-commerce packaging selection
- Sustainability reporting
- Cost optimization
- Environmental compliance

---

## 📋 Prerequisites

- **Python 3.11+**
- **PostgreSQL 16+**
- **pip** package manager
- **Git**

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/AdarshPrabhuJP/Packaging-Recommendation-System.git
cd Packaging-Recommendation-System
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Database

**Option A: Use Render PostgreSQL (Recommended for deployment)**
```bash
# Set DATABASE_URL environment variable
export DATABASE_URL="your_render_postgresql_url"
```

**Option B: Local PostgreSQL**
```bash
# Create database
createdb packaging_db

# Initialize schema
psql -d packaging_db -f database/schema.sql

# Import data
python database/import_data.py
```

### 4. Run the Application

```bash
python app.py
```

Visit: **http://localhost:5000**

---

## 💻 Usage

### **Web Interface**

1. **Get Recommendations**
   - Enter product weight (grams)
   - Set fragility level (1-5)
   - Specify shipping distance (km)
   - Choose priority (Balanced/Eco-Friendly/Budget)
   - Select product category
   - Click "Get Recommendations"

2. **View Analytics Dashboard**
   - Click "📊 Analytics Dashboard"
   - View key metrics (Total materials, CO₂ saved, Cost savings)
   - Explore interactive charts
   - Download PDF sustainability report
   - Export Excel data for analysis

### **API Usage**

```bash
# Get all materials
curl http://localhost:5000/api/materials

# Get recommendations
curl -X POST http://localhost:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "product_weight": 500,
    "product_fragility": 3,
    "shipping_distance": 100,
    "priority": "balanced",
    "category": "general"
  }'

# Health check
curl http://localhost:5000/api/health
```

---

## 📊 Model Performance

| Model | Metric | Score |
|-------|--------|-------|
| Random Forest Cost | R² | 0.9655 |
| Random Forest Cost | MAE | ₹35.17 |
| Random Forest CO₂ | R² | 0.9865 |
| Random Forest CO₂ | MAE | 0.046 kg |
| XGBoost Cost | R² | 0.9712 |
| XGBoost CO₂ | R² | 0.9891 |

---

## 🗂️ Project Structure

```
Packaging-Recommendation-System/
├── app/                        # Flask application
│   ├── __init__.py            # App factory
│   ├── routes.py              # API routes
│   ├── config.py              # Configuration
│   ├── analytics.py           # Analytics logic
│   ├── pdf_generator.py       # PDF export
│   └── excel_generator.py     # Excel export
├── templates/                  # HTML templates
│   ├── index.html             # Main page
│   └── dashboard.html         # Analytics dashboard
├── static/                     # Static assets
│   ├── css/                   # Stylesheets
│   ├── js/                    # JavaScript
│   └── images/                # Images
├── models/                     # Trained ML models
│   ├── random_forest_cost_model.pkl
│   ├── random_forest_co2_model.pkl
│   ├── xgboost_cost_model.pkl
│   └── xgboost_co2_model.pkl
├── database/                   # Database setup
│   ├── schema.sql             # DB schema
│   └── import_data.py         # Data import
├── src/                        # Source code
│   ├── ml_models.py           # Random Forest
│   ├── xgboost_models.py      # XGBoost
│   ├── ranking_system.py      # Ranking logic
│   └── inference.py           # Predictions
├── requirements.txt            # Dependencies
├── Procfile                    # Render deployment
├── runtime.txt                 # Python version
├── wsgi.py                     # WSGI entry point
└── README.md                   # This file
```

---

## 🚀 Deployment

### **Render (Recommended)**

1. **Create Web Service** on Render
2. **Connect GitHub repository**
3. **Add environment variable**:
   ```
   DATABASE_URL=your_postgresql_url
   ```
4. **Deploy** - Automatic from GitHub

See [DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md) for detailed instructions.

---

## 🔧 Configuration

### **Environment Variables**

```bash
# Database (choose one method)
DATABASE_URL=postgresql://user:pass@host/db  # Render/Production
# OR
DB_NAME=packaging_db                          # Local development
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Application
SECRET_KEY=your-secret-key
```

---

## 📖 Documentation

- **[PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)** - Complete technical documentation
- **[API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md)** - API reference
- **[USER_GUIDE.md](docs/USER_GUIDE.md)** - User manual
- **[DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md)** - Deployment instructions

---

## 🧪 Testing

```bash
# Test database connection
python src/database_utils.py

# Test ML models
python src/ml_models.py

# Test API
python -m pytest tests/
```

---

## 🔧 Troubleshooting

### **Database Connection Error**
```bash
# Check DATABASE_URL is set
echo $DATABASE_URL

# Verify PostgreSQL is running
pg_isready
```

### **Import Error**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### **Model Not Found**
```bash
# Train models
python src/ml_models.py
python src/xgboost_models.py
```

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📝 License

This project is licensed under the MIT License.

---

## 📧 Contact

- **GitHub**: [AdarshPrabhuJP](https://github.com/AdarshPrabhuJP)
- **Issues**: [Report a bug](https://github.com/AdarshPrabhuJP/Packaging-Recommendation-System/issues)

---

## 🙏 Acknowledgments

- **Infosys Springboard** - Project mentorship
- **PostgreSQL** - Database
- **Flask** - Web framework
- **scikit-learn & XGBoost** - Machine learning
- **Chart.js** - Data visualization
- **Render** - Cloud deployment

---

**Built with ❤️ using Python, Flask, PostgreSQL, and Machine Learning**

🌐 **[Live Demo](https://packaging-recommendation-system-nyqr.onrender.com)** | 📊 **[Analytics Dashboard](https://packaging-recommendation-system-nyqr.onrender.com/dashboard)**