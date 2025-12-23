# Packaging Recommendation System

An intelligent ML-based system for recommending optimal packaging materials based on product characteristics, cost, and environmental impact.

---

## Overview

This system uses machine learning to recommend the most suitable packaging materials for products by analyzing multiple factors including cost, durability, environmental impact, and product requirements. The system employs Random Forest and XGBoost algorithms to predict costs and CO₂ emissions, combined with an intelligent ranking system to provide personalized recommendations.

---

## Features

- **61 Packaging Materials Database** - Comprehensive PostgreSQL database with diverse packaging options
- **ML-Based Predictions** - Random Forest and XGBoost models for cost and CO₂ prediction
- **Intelligent Ranking System** - Multi-criteria ranking with customizable priorities
- **Feature Engineering** - Normalized features with StandardScaler for optimal performance
- **Data Visualization** - 7 analytical charts for dataset insights
- **High Accuracy** - Cost prediction R² = 0.9655, CO₂ prediction R² = 0.9865

---

## Technology Stack

**Backend:**
- Python 3.11
- PostgreSQL 16

**Machine Learning:**
- scikit-learn (Random Forest)
- XGBoost (Gradient Boosting)
- pandas, numpy (Data processing)

**Visualization:**
- matplotlib, seaborn

**Model Persistence:**
- joblib

---

## Project Structure

```
Packaging-Recommendation-System/
├── Data/                          # Dataset files
│   ├── ecopack_dataset.csv
│   └── expanded_ecopack_dataset.csv
├── database/                      # Database configuration
│   ├── config.py
│   ├── schema.sql
│   ├── init_db.py
│   └── import_data.py
├── src/                           # Source code
│   ├── database_utils.py          # Database utilities
│   ├── feature_engineering.py     # Feature calculations
│   ├── data_validation.py         # Data validation
│   ├── data_cleaning.py           # Data cleaning
│   ├── visualizations.py          # Chart generation
│   ├── ml_models.py               # Random Forest models
│   ├── xgboost_models.py          # XGBoost models
│   ├── ranking_system.py          # Material ranking
│   └── inference.py               # Prediction interface
├── models/                        # Trained ML models
│   ├── classifier_model.pkl
│   ├── cost_model.pkl
│   ├── co2_model.pkl
│   ├── xgboost_cost_model.pkl
│   ├── xgboost_co2_model.pkl
│   └── feature_scaler.pkl
├── visualizations/                # Generated charts
├── requirements.txt
└── README.md
```

---

## Dataset

**Size:** 61 packaging materials

**Features:**
- Material type
- Cost per unit (₹)
- Durability score (0-10)
- CO₂ footprint (kg)
- Biodegradability score (0-10)
- Product weight (g)
- Product fragility (1-5)
- Shipping distance (km)
- Recyclable (boolean)

**Statistics:**
- Cost range: ₹330 - ₹2,475
- Recyclable materials: 85.2%
- Average CO₂: 1.31 kg

---

## Machine Learning Models

### Random Forest Models

**Cost Prediction:**
- Algorithm: Random Forest Regressor
- R² Score: 0.9655
- RMSE: ₹99.55
- MAE: ₹35.17

**CO₂ Prediction:**
- Algorithm: Random Forest Regressor
- R² Score: 0.9865
- RMSE: 0.085 kg
- MAE: 0.046 kg

### XGBoost Models

**Features:**
- Gradient boosting algorithm
- StandardScaler normalization
- 8 input features
- 80/20 train-test split

**Performance:**
- Similar or better than Random Forest
- Production-ready quality

---

## Ranking System

The intelligent ranking system combines ML predictions with multi-criteria scoring:

**Scoring Components:**
- Predicted cost (from XGBoost)
- Predicted CO₂ (from XGBoost)
- Durability score
- Biodegradability score
- Recyclability bonus

**Priority Modes:**

1. **Eco-Priority** (Environmental Focus)
   - Cost: 20%
   - CO₂: 40%
   - Durability: 20%
   - Biodegradability: 20%

2. **Budget-Priority** (Cost Focus)
   - Cost: 50%
   - CO₂: 10%
   - Durability: 30%
   - Biodegradability: 10%

3. **Balanced** (Equal Weight)
   - Cost: 30%
   - CO₂: 30%
   - Durability: 20%
   - Biodegradability: 20%

---

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/springboardmentor123455-maker/Packaging-Recommendation-System.git
cd Packaging-Recommendation-System
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up PostgreSQL database**
```bash
# Create database
createdb packaging_db

# Initialize schema
psql -d packaging_db -f database/schema.sql

# Import data
python database/import_data.py
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

---

## Usage

### Train Models

```bash
# Train Random Forest models
python src/ml_models.py

# Train XGBoost models
python src/xgboost_models.py
```

### Get Recommendations

```python
from src.ranking_system import MaterialRanker

ranker = MaterialRanker()

# Get eco-friendly recommendations
rankings = ranker.rank_materials(
    requirements={'eco_priority': 'high'},
    top_n=5
)

ranker.display_rankings(rankings)
```

### Make Predictions

```python
from src.inference import PackagingRecommender

recommender = PackagingRecommender()

result = recommender.predict(
    product_weight=200,
    product_fragility=5,
    shipping_distance=500
)

print(f"Recommended: {result['recommended_material']}")
print(f"Cost: ₹{result['predicted_cost']:.2f}")
print(f"CO₂: {result['predicted_co2']:.2f} kg")
```

---

## Model Performance

| Model | Metric | Value |
|-------|--------|-------|
| RF Cost | R² Score | 0.9655 |
| RF Cost | MAE | ₹35.17 |
| RF CO₂ | R² Score | 0.9865 |
| RF CO₂ | MAE | 0.046 kg |
| XGBoost Cost | R² Score | ~0.96-0.99 |
| XGBoost CO₂ | R² Score | ~0.98-0.99 |

---

## Data Pipeline

1. **Data Loading** - Fetch from PostgreSQL
2. **Feature Selection** - 8 relevant features
3. **Feature Engineering** - Type conversion, normalization
4. **Train-Test Split** - 80/20 split
5. **Feature Scaling** - StandardScaler normalization
6. **Model Training** - Random Forest & XGBoost
7. **Model Evaluation** - R², RMSE, MAE metrics

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## License

This project is licensed under the MIT License.

---

## Contact

For questions or feedback, please open an issue on GitHub.

---

**Last Updated:** December 2025
