# Data Quality Report

**Generated:** 2025-12-18 20:10:59

**Project:** Packaging Recommendation System

---

## 📊 Dataset Overview

- **Total Materials:** 61
- **Recyclable Materials:** 52 (85.2%)
- **Non-Recyclable Materials:** 9
- **Number of Features:** 11 (10 attributes + 1 ID)

---

## 🔍 Missing Value Analysis

✅ **No missing values found** - Dataset is 100% complete!


---

## 📈 Statistical Summary

### Numerical Features

| Feature | Min | Max | Mean | Std Dev |
|---------|-----|-----|------|---------|
| cost_per_unit | 5.00 | 1980.00 | 652.77 | 508.52 |
| durability_score | 5.00 | 10.00 | 7.05 | 1.18 |
| co2_footprint | 0.20 | 4.00 | 1.31 | 0.94 |
| biodegradability_score | 1.00 | 10.00 | 6.85 | 3.15 |
| product_weight | 50.00 | 2000.00 | 289.84 | 280.98 |
| product_fragility | 1.00 | 5.00 | 2.31 | 0.98 |
| shipping_distance | 50.00 | 1000.00 | 156.97 | 135.65 |

### Database Averages

- **Average Cost:** $652.77
- **Average CO₂ Footprint:** 1.31
- **Average Biodegradability:** 6.9/10
- **Average Durability:** 7.0/10

---

## 🎯 Outlier Detection

⚠️ **Found 11 outliers:**

| Feature | Outlier Count | Valid Range |
|---------|---------------|-------------|
| co2_footprint | 1 | [-1.35, 3.85] |
| product_weight | 5 | [-75.00, 525.00] |
| shipping_distance | 5 | [10.00, 250.00] |

---

## ✅ Range Validation

✅ **All values within expected ranges**

- Durability scores: 0-10 ✓
- Biodegradability scores: 0-10 ✓
- Cost values: Non-negative ✓
- CO₂ values: Non-negative ✓

---

## 🏷️ Categorical Variables

### Material Types (61 unique)

- Air Pillows (code: 0)
- Algae-Based Packaging (code: 1)
- Aluminium Foil Packaging (code: 2)
- Bamboo Fiber Box (code: 3)
- Banana Fiber Packaging (code: 4)
- Biodegradable Bubble Wrap (code: 5)
- Biodegradable Mailers (code: 6)
- Biodegradable Plastic (code: 7)
- Bioplastic Tray (code: 8)
- Bubble Wrap (code: 9)
- Bubble Wrap (Recyclable) (code: 10)
- Cardboard Box (code: 11)
- Cardboard Dividers (code: 12)
- Cassava Starch Film (code: 13)
- Cellulose Film (code: 14)
- Coconut Fiber Packaging (code: 15)
- Coffee Chaff Packaging (code: 16)
- Compostable Mailer (code: 17)
- Cornstarch Packaging (code: 18)
- Corrugated Cardboard (code: 19)
- Corrugated Plastic Sheets (code: 20)
- Edge Protectors (Cardboard) (code: 21)
- Expanded Polystyrene (EPS) (code: 22)
- Flax Fiber Packaging (code: 23)
- Foam Inserts (code: 24)
- Gummed Paper Tape (code: 25)
- HDPE Containers (code: 26)
- Hemp Packaging (code: 27)
- Honeycomb Paper (code: 28)
- Jute Packaging (code: 29)
- Kraft Paper Bags (code: 30)
- Kraft Paper Mailer (code: 31)
- Metal Tins (Aluminum) (code: 32)
- Molded Pulp (code: 33)
- Mushroom Packaging (code: 34)
- Mycelium Foam (code: 35)
- Newspaper Packaging (code: 36)
- PET Bottles (code: 37)
- PLA Containers (code: 38)
- PP Containers (code: 39)
- Paper Cushioning (code: 40)
- Paper Tape (code: 41)
- Pineapple Leaf Fiber (code: 42)
- Polyethylene Foam (code: 43)
- Recycled Cardboard Tubes (code: 44)
- Recycled Cotton Bags (code: 45)
- Recycled Glass Containers (code: 46)
- Recycled Paper Box (code: 47)
- Recycled Plastic (code: 48)
- Rice Husk Packaging (code: 49)
- Seaweed Packaging (code: 50)
- Shredded Paper Fill (code: 51)
- Starch-Based Peanuts (code: 52)
- Stretch Film (Recyclable) (code: 53)
- Sugarcane Bagasse (code: 54)
- Tea Waste Packaging (code: 55)
- Thermocol Sheets (code: 56)
- Wax-Coated Paper (code: 57)
- Wheat Straw Packaging (code: 58)
- Wood Wool (code: 59)
- Wooden Crate (code: 60)

### Recommended Uses (47 unique)

- Beverages (code: 0)
- Biodegradable Fill (code: 1)
- Clothing (code: 2)
- Compostable Packaging (code: 3)
- Corner Protection (code: 4)
- Cushioning (code: 5)
- Custom Protection (code: 6)
- E-commerce Shipping (code: 7)
- Eco Cushioning (code: 8)
- Eco Packaging (code: 9)
- Eco-Friendly Bags (code: 10)
- Eco-Friendly Packaging (code: 11)
- Electronics (code: 12)
- Electronics Packaging (code: 13)
- Food Containers (code: 14)
- Food Packaging (code: 15)
- Food Storage (code: 16)
- Food Wrapping (code: 17)
- Food and Pharma (code: 18)
- Food/Fragile Items (code: 19)
- Fragile Electronics (code: 20)
- Fragile Items (code: 21)
- General Packaging (code: 22)
- Heavy Items (code: 23)
- Industrial Goods (code: 24)
- Innovative Eco (code: 25)
- Light Items (code: 26)
- Lightweight Protection (code: 27)
- Liquids (code: 28)
- Organic Products (code: 29)
- Pallet Wrapping (code: 30)
- Premium Eco Packaging (code: 31)
- Premium Packaging (code: 32)
- Product Separation (code: 33)
- Protective Packaging (code: 34)
- Retail Packaging (code: 35)
- Reusable Bags (code: 36)
- Reusable Packaging (code: 37)
- Sealing (code: 38)
- Shipping Boxes (code: 39)
- Shipping Tubes (code: 40)
- Shock Absorption (code: 41)
- Soft Cushioning (code: 42)
- Soft Goods (code: 43)
- Sustainable Packaging (code: 44)
- Void Fill (code: 45)
- Water-Activated Sealing (code: 46)

---

## 🎯 Overall Data Quality Assessment

### ✅ **EXCELLENT**

The dataset is of high quality with:
- ✅ No missing values
- ✅ All values within valid ranges
- ✅ Proper data types
- ✅ Consistent formatting

**Recommendation:** Dataset is ready for analysis and modeling.

---


*Report generated by Data Quality Report Generator v1.0*