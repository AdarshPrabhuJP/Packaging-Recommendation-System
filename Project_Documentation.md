# Infosys Virtual Internship - Packaging Recommendation System
## Project Documentation

---

## 📋 Project Overview

**Project Name:** Packaging Recommendation System  
**Organization:** Infosys Virtual Internship  
**Timeline:** Week 1 - Week 8  
**Objective:** Build a system to recommend eco-friendly packaging materials based on various attributes

---

## 🎯 Project Modules

### Module 1: Data Collection and Management
- Gather eco-friendly material dataset with attributes:
  - Material type, strength, weight capacity
  - Biodegradability score
  - CO₂ emission score
  - Recyclability %
- Collect industry product categories: electronics, food, cosmetics, etc.
- Create PostgreSQL database structure for materials and product data
- Integrate CSV/Excel material data and validate schema

### Module 2: Data Cleaning and Feature Engineering
- Handle missing values and normalize numerical features
- Encode categorical material properties
- Feature engineering for:
  - CO₂ Impact Index
  - Cost Efficiency Index
  - Material Suitability Score
- Validate data quality using summary statistics

---

## 📅 Daily Progress Log

### **Day 1 - December 2, 2025**

#### ✅ Completed Tasks
- Created dataset for eco-friendly packaging materials
- Downloaded and started PostgreSQL installation
- Set up project structure

#### 📝 Notes
- Dataset includes attributes: material type, strength, weight capacity, biodegradability score, CO₂ emission score, recyclability %
- PostgreSQL will be used to store and manage materials and product data

#### 🔄 Next Steps
- Complete PostgreSQL installation and configuration
- Create database schema for materials and products
- Import dataset into PostgreSQL
- Validate data structure

#### ❓ Questions/Blockers
- None currently

---

### **Day 2 - December 3, 2025**

#### ✅ Completed Tasks
- Set up PostgreSQL database structure and configuration
- Created database schema with two tables:
  - `materials` table for general eco-friendly packaging materials
  - `autoliv_materials` table for Autoliv-specific sustainable packaging data
- Developed database initialization and data import scripts
- Added environment variable configuration for secure credential management
- Updated project structure with database folder

#### 📝 Notes
- Database uses PostgreSQL with proper constraints, indexes, and data validation
- Configuration uses environment variables (.env file) to keep credentials secure
- Schema includes comprehensive indexes for performance optimization
- Import scripts handle data type conversions (e.g., yes/no to boolean)
- Successfully imported all CSV data into PostgreSQL

#### ✅ Setup Completed
- Installed Python dependencies from requirements.txt
- Created PostgreSQL database (`packaging_recommendation_db`)
- Configured .env file with database credentials
- Ran database initialization script successfully
- Imported all CSV data into PostgreSQL tables (22 total records)
- Verified data integrity and table structure

#### ❓ Questions/Blockers
- None

---

### **Day 3 - December 4, 2025**

#### ✅ Completed Tasks
- Built feature engineering module with 3 calculated metrics:
  - CO₂ Impact Index (0-100 scale)
  - Cost Efficiency Index (0-100 scale)
  - Material Suitability Score (0-100 scale)
- Created database query utilities for filtering and searching materials
- Developed recommendation query functions:
  - Get eco-friendly materials by sustainability criteria
  - Get materials by budget constraints
  - Get materials by product category
  - Find sustainable alternatives
  - Compare materials side-by-side
- Built comprehensive testing/demo script

#### 📝 Notes
- Feature engineering formulas:
  - CO₂ Impact Index = 50% CO₂ footprint + 40% biodegradability + 10% recyclability
  - Cost Efficiency = 40% cost + 30% biodegradability + 20% durability + 10% recyclability
  - Suitability Score = 40% sustainability + 30% cost + 30% durability
- All materials now have calculated scores for easy comparison
- Recommendation system can filter by multiple criteria simultaneously
- Created 4 Python modules totaling ~1,070 lines of code
- Successfully tested all recommendation functions

#### ❓ Questions/Blockers
- None

---

### **Day 4 - December 5, 2025**

#### ✅ Completed Tasks
- Created data validation module with comprehensive quality checks
- Implemented data cleaning and normalization utilities
- Generated data quality report
- Completed Module 2 (Data Cleaning and Feature Engineering)

#### 📝 Notes
- Data quality assessment results:
  - 100% complete dataset (no missing values)
  - All values within valid ranges
  - 2 minor outliers detected (product_weight, shipping_distance)
  - 16 unique material types, 16 recommended use categories
- Normalization strategy:
  - Min-Max scaling for numerical features (0-1 range)
  - One-hot encoding for categorical variables
  - Preserved original values alongside normalized versions
- Generated comprehensive quality report (DATA_QUALITY_REPORT.md)
- Dataset ready for advanced analysis and modeling

#### ❓ Questions/Blockers
- None

---

### **Day 5 - December 18, 2025**

#### ✅ Completed Tasks
- Expanded dataset from 32 to 61 packaging materials
- Removed non-packaging items (palm leaf plates, beeswax wraps, silicone bags)
- Added 12 new relevant packaging materials
- Converted all costs from USD to Indian Rupees (₹)
- Cleaned and reimported database
- Regenerated all Module 1 & 2 outputs

#### 📝 Notes
- **Dataset Expansion:**
  - Total materials: 61 (was 32)
  - Recyclable: 52 (85.2%)
  - Cost range: ₹330 - ₹2,475
  - Focused on packaging/shipping materials only
  
- **New Materials Added:**
  - Expanded Polystyrene (EPS), Polyethylene Foam
  - Corrugated Plastic Sheets, Honeycomb Paper
  - Edge Protectors, Stretch Film
  - Biodegradable Bubble Wrap, Paper Tape
  - Gummed Paper Tape, Cardboard Dividers
  - Foam Inserts, Biodegradable Mailers

- **Updated Outputs:**
  - All 7 visualizations regenerated with new data
  - Data validation report updated (100% complete dataset)
  - Data cleaning & normalization updated (61 materials)
  - Data quality report updated (85.2% recyclable)
  - All tests passing (7/7 - 100% success rate)

- **Currency Conversion:**
  - Exchange rate: $1 = ₹82.50
  - All costs now in Indian Rupees for local context

#### ❓ Questions/Blockers
- None

---

## 🗂️ Project Structure

```
Packaging-Recommendation-System/
├── Data/                    # Dataset CSV files
│   ├── ecopack_dataset.csv
│   └── Detailed_Autoliv_Sustainable_Packaging_Dataset.csv
├── database/               # Database scripts and configuration
│   ├── config.py          # Database connection configuration
│   ├── schema.sql         # Database schema (tables, indexes)
│   ├── init_db.py         # Database initialization script
│   ├── import_data.py     # Data import script
│   └── README.md          # Database setup guide
├── src/                   # Source code
│   ├── database_utils.py  # Database query utilities
│   ├── feature_engineering.py  # Feature calculations (Day 3)
│   ├── recommendation_queries.py  # Recommendation functions (Day 3)
│   ├── test_recommendations.py  # Demo script (Day 3)
│   ├── data_validation.py  # Data validation (Day 4)
│   ├── data_cleaning.py  # Data cleaning & normalization (Day 4)
│   └── data_quality_report.py  # Quality report generator (Day 4)
├── DATA_QUALITY_REPORT.md  # Generated quality report (Day 4)
├── cleaned_dataset.json  # Normalized dataset (Day 4)
├── data_validation_report.json  # Validation results (Day 4)
├── .env.example           # Environment variables template
├── requirements.txt       # Python dependencies
├── README.md             # Project overview
└── Project_Documentation.md # This file
```

---

## 📊 Dataset Information

### Material Attributes
- **Material Type:** Categorical (e.g., cardboard, bioplastic, recycled paper)
- **Strength:** Numerical
- **Weight Capacity:** Numerical
- **Biodegradability Score:** Numerical (0-100)
- **CO₂ Emission Score:** Numerical
- **Recyclability %:** Numerical (0-100)

### Product Categories
- Electronics
- Food
- Cosmetics
- Others (to be defined)

---

## 🛠️ Technology Stack

- **Database:** PostgreSQL
- **Data Format:** CSV/Excel
- **Programming Language:** Python (assumed)
- **Tools:** pgAdmin/psql (for database management)

---

**Last Updated:** December 18, 2025




