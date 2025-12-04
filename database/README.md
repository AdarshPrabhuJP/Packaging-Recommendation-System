# Database Setup Guide

This folder contains all the database-related scripts and configuration for the Packaging Recommendation System.

## 📁 Files Overview

- **`config.py`** - Database connection configuration and utilities
- **`schema.sql`** - PostgreSQL schema (tables, indexes, constraints)
- **`init_db.py`** - Script to initialize database and create tables
- **`import_data.py`** - Script to import CSV data into PostgreSQL

## 🚀 Quick Start

### Prerequisites

1. **PostgreSQL installed and running** (version 12 or higher recommended)
2. **Python 3.8+** installed
3. **Python dependencies** installed (see below)

### Step 1: Install Python Dependencies

```bash
cd "c:\Users\adars\OneDrive\Desktop\Infosys Virtual Internship\Packaging-Recommendation-System"
pip install -r requirements.txt
```

### Step 2: Create PostgreSQL Database

Open pgAdmin or use psql command line:

```sql
CREATE DATABASE packaging_recommendation_db;
```

### Step 3: Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` and fill in your PostgreSQL credentials:
   ```
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=packaging_recommendation_db
   DB_USER=postgres
   DB_PASSWORD=your_actual_password
   ```

### Step 4: Initialize Database Schema

Run the initialization script to create tables:

```bash
python database/init_db.py
```

Expected output:
```
✓ Connected successfully
✓ Schema file loaded
✓ Schema executed successfully
✓ Tables created successfully:
  - autoliv_materials
  - materials
```

### Step 5: Import Data

Run the import script to load CSV data:

```bash
python database/import_data.py
```

Expected output:
```
✓ Successfully inserted 16 rows into materials table
✓ Successfully inserted 6 rows into autoliv_materials table
✓ All data imported successfully!
```

### Step 6: Verify Installation

Test the database connection:

```bash
python database/config.py
```

## 📊 Database Schema

### `materials` Table

Stores general eco-friendly packaging materials from `ecopack_dataset.csv`.

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| material_type | VARCHAR(100) | Type of material |
| cost_per_unit | DECIMAL(10,2) | Cost per unit |
| durability_score | INTEGER | Durability rating (0-10) |
| co2_footprint | DECIMAL(10,2) | CO2 emissions |
| biodegradability_score | INTEGER | Biodegradability rating (0-10) |
| recyclable | BOOLEAN | Whether material is recyclable |
| product_weight | INTEGER | Product weight |
| product_fragility | INTEGER | Fragility level (0-10) |
| shipping_distance | INTEGER | Shipping distance |
| recommended_use | VARCHAR(200) | Recommended use case |

### `autoliv_materials` Table

Stores Autoliv-specific sustainable packaging data.

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| packaging_type | VARCHAR(100) | Type of packaging |
| material_type | VARCHAR(100) | Material type |
| recyclability_pct | DECIMAL(5,2) | Recyclability percentage |
| reusability_pct | DECIMAL(5,2) | Reusability percentage |
| carbon_footprint | DECIMAL(10,2) | Carbon footprint (kg CO2/unit) |
| waste_reduction_impact_pct | DECIMAL(5,2) | Waste reduction impact |
| supplier_sustainability_compliance_pct | DECIMAL(5,2) | Supplier compliance |
| cost_per_unit | DECIMAL(10,2) | Cost per unit (USD) |
| annual_usage | INTEGER | Annual usage (units) |
| total_material_weight | DECIMAL(10,2) | Total weight (tons) |
| recycled_content_pct | DECIMAL(5,2) | Recycled content percentage |
| end_of_life_disposal_pct | DECIMAL(5,2) | End-of-life disposal percentage |
| sustainability_target_progress_pct | DECIMAL(5,2) | Sustainability target progress |

## 🔍 Useful SQL Queries

### View all materials
```sql
SELECT * FROM materials;
```

### Find most eco-friendly materials (high biodegradability, low CO2)
```sql
SELECT material_type, biodegradability_score, co2_footprint, recyclable
FROM materials
WHERE biodegradability_score >= 8 AND co2_footprint < 1.0
ORDER BY biodegradability_score DESC, co2_footprint ASC;
```

### View Autoliv materials with high recyclability
```sql
SELECT packaging_type, material_type, recyclability_pct, carbon_footprint
FROM autoliv_materials
WHERE recyclability_pct >= 90
ORDER BY recyclability_pct DESC;
```

## 🛠️ Troubleshooting

### Connection Error
- Verify PostgreSQL is running
- Check credentials in `.env` file
- Ensure database exists

### Import Error
- Run `init_db.py` first to create tables
- Verify CSV files exist in `Data/` folder
- Check for data type mismatches

### Permission Error
- Ensure PostgreSQL user has CREATE and INSERT permissions
- Check database ownership

## 📝 Notes

- The `.env` file is gitignored to protect credentials
- Tables include timestamps (`created_at`, `updated_at`)
- Indexes are created for performance optimization
- All percentage fields are constrained to 0-100 range
