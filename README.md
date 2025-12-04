# Packaging Recommendation System

**Infosys Virtual Internship Project**  
AI-powered system to recommend eco-friendly packaging materials based on sustainability, cost, and performance criteria.

---

## 📋 Project Overview

This system helps businesses select the most suitable packaging materials by analyzing:
- **Environmental Impact** - CO₂ footprint, biodegradability, recyclability
- **Cost Efficiency** - Budget constraints and value optimization
- **Performance** - Durability, weight capacity, fragility handling
- **Use Cases** - Electronics, food, cosmetics, industrial goods

---

## 🎯 Features

### ✅ Implemented (Days 1-3)

- **PostgreSQL Database** - 22 packaging materials with comprehensive attributes
- **Feature Engineering** - 3 calculated metrics:
  - CO₂ Impact Index (0-100)
  - Cost Efficiency Index (0-100)
  - Material Suitability Score (0-100)
- **Smart Recommendations** - Filter by sustainability, budget, category
- **Alternative Finder** - Discover eco-friendly alternatives
- **Material Comparison** - Side-by-side analysis

---

## 🗂️ Project Structure

```
Packaging-Recommendation-System/
├── Data/                    # Dataset CSV files (22 materials)
├── database/               # PostgreSQL setup scripts
│   ├── config.py          # Database connection
│   ├── schema.sql         # Table definitions
│   ├── init_db.py         # Initialization script
│   └── import_data.py     # Data import script
├── src/                   # Source code
│   ├── database_utils.py  # Query utilities
│   ├── feature_engineering.py  # Metric calculations
│   ├── recommendation_queries.py  # Recommendation logic
│   └── test_recommendations.py  # Demo script
├── .env.example           # Environment template
├── requirements.txt       # Python dependencies
└── Project_Documentation.md  # Detailed documentation
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL 12+

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Packaging-Recommendation-System.git
   cd Packaging-Recommendation-System
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up PostgreSQL**
   ```sql
   CREATE DATABASE packaging_recommendation_db;
   ```

4. **Configure environment**
   ```bash
   copy .env.example .env
   # Edit .env with your PostgreSQL credentials
   ```

5. **Initialize database**
   ```bash
   python database/init_db.py
   python database/import_data.py
   ```

6. **Run demo**
   ```bash
   python src/test_recommendations.py
   ```

---

## 💡 Usage Examples

### Get Eco-Friendly Materials
```python
from src.recommendation_queries import get_eco_friendly_materials

materials = get_eco_friendly_materials(
    min_co2_index=70,
    min_biodegradability=8,
    recyclable_only=True
)
```

### Get Budget-Friendly Options
```python
from src.recommendation_queries import get_materials_by_budget

materials = get_materials_by_budget(max_cost=15, min_suitability_score=60)
```

### Get Materials for Electronics
```python
from src.recommendation_queries import get_materials_by_category

materials = get_materials_by_category('Electronics', top_n=5)
```

---

## 📊 Dataset

**Total Materials:** 22  
**Sources:** 2 CSV files
- `ecopack_dataset.csv` - 16 general eco-friendly materials
- `Detailed_Autoliv_Sustainable_Packaging_Dataset.csv` - 6 industrial materials

**Attributes:**
- Material type, cost, durability, weight capacity
- CO₂ footprint, biodegradability, recyclability
- Product fragility, shipping distance, recommended use

---

## 🛠️ Technology Stack

- **Database:** PostgreSQL
- **Backend:** Python 3.8+
- **Libraries:** psycopg2, pandas, python-dotenv
- **Version Control:** Git

---

## 📈 Feature Engineering

### CO₂ Impact Index
Formula: `50% CO₂ footprint + 40% biodegradability + 10% recyclability`

### Cost Efficiency Index
Formula: `40% cost + 30% biodegradability + 20% durability + 10% recyclability`

### Material Suitability Score
Formula: `40% sustainability + 30% cost + 30% durability`

---

## 📝 Documentation

- [Project Documentation](Project_Documentation.md) - Detailed day-by-day progress
- [Database Setup Guide](database/README.md) - PostgreSQL configuration

---

## 🤝 Contributing

This is an internship project. For questions or suggestions, please open an issue.

---

## 📄 License

See [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Adarsh Prabhu JP**  
Infosys Virtual Internship - Packaging Recommendation System

---

**Last Updated:** December 4, 2025