# Packaging Recommendation System

An intelligent ML-based system for recommending optimal packaging materials based on product characteristics, cost, and environmental impact.

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)](https://www.postgresql.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3.2-orange.svg)](https://scikit-learn.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0.3-green.svg)](https://xgboost.readthedocs.io/)

---

## 🎯 Overview

This system uses machine learning to recommend the most suitable packaging materials by analyzing cost, durability, environmental impact, and product requirements. It employs Random Forest and XGBoost algorithms with an intelligent ranking system.

**Key Features:**
- 61 packaging materials database
- ML models with 96-98% accuracy
- Multi-criteria ranking system
- Real-time predictions

---

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.11+** installed
- **PostgreSQL 16+** installed and running
- **pip** package manager
- **Git** (for cloning)

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/springboardmentor123455-maker/Packaging-Recommendation-System.git
cd Packaging-Recommendation-System
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up PostgreSQL Database

**Create Database:**
```bash
createdb packaging_db
```

**Initialize Schema:**
```bash
psql -d packaging_db -f database/schema.sql
```

**Import Data:**
```bash
python database/import_data.py
```

### 4. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your database credentials
# DB_NAME=packaging_db
# DB_USER=your_username
# DB_PASSWORD=your_password
# DB_HOST=localhost
# DB_PORT=5432
```

### 5. Verify Installation

```bash
# Test database connection
python src/database_utils.py

# Should show: 61 materials, 85.2% recyclable
```

---

## 💻 Usage

### Train ML Models

**Random Forest Models:**
```bash
python src/ml_models.py
```

**XGBoost Models:**
```bash
python src/xgboost_models.py
```

### Get Material Rankings

```bash
python src/ranking_system.py
```

### Make Predictions

```bash
python src/inference.py
```

---

## 📊 Model Performance

| Model | Metric | Score |
|-------|--------|-------|
| Random Forest Cost | R² | 0.9655 |
| Random Forest Cost | MAE | ₹35.17 |
| Random Forest CO₂ | R² | 0.9865 |
| Random Forest CO₂ | MAE | 0.046 kg |

---

## 🗂️ Project Structure

```
Packaging-Recommendation-System/
├── Data/                    # Dataset files
├── database/                # Database setup
│   ├── config.py           # DB connection
│   ├── schema.sql          # DB schema
│   ├── init_db.py          # Initialize DB
│   └── import_data.py      # Import data
├── src/                    # Source code
│   ├── ml_models.py        # Random Forest
│   ├── xgboost_models.py   # XGBoost
│   ├── ranking_system.py   # Ranking
│   └── inference.py        # Predictions
├── models/                 # Trained models
├── visualizations/         # Charts
├── requirements.txt        # Dependencies
└── README.md              # This file
```

---

## 🔧 Troubleshooting

### Database Connection Error

```bash
# Check PostgreSQL is running
pg_isready

# Verify credentials in .env file
cat .env
```

### Import Error

```bash
# Ensure you're in project root
cd Packaging-Recommendation-System

# Reinstall dependencies
pip install -r requirements.txt
```

### Model Not Found

```bash
# Train models first
python src/ml_models.py
python src/xgboost_models.py
```

---

## 📖 Documentation

For detailed documentation, see [Project_Documentation.md](Project_Documentation.md)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📝 License

This project is licensed under the MIT License.

---

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Built with ❤️ using Python, PostgreSQL, and Machine Learning**