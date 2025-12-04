-- PostgreSQL Database Schema for Packaging Recommendation System
-- Created: December 3, 2025

-- Drop tables if they exist (for clean re-initialization)
DROP TABLE IF EXISTS materials CASCADE;
DROP TABLE IF EXISTS autoliv_materials CASCADE;

-- ============================================
-- Table: materials
-- Description: General eco-friendly packaging materials from ecopack_dataset.csv
-- ============================================
CREATE TABLE materials (
    id SERIAL PRIMARY KEY,
    material_type VARCHAR(100) NOT NULL,
    cost_per_unit DECIMAL(10, 2),
    durability_score INTEGER CHECK (durability_score >= 0 AND durability_score <= 10),
    co2_footprint DECIMAL(10, 2),
    biodegradability_score INTEGER CHECK (biodegradability_score >= 0 AND biodegradability_score <= 10),
    recyclable BOOLEAN,
    product_weight INTEGER,
    product_fragility INTEGER CHECK (product_fragility >= 0 AND product_fragility <= 10),
    shipping_distance INTEGER,
    recommended_use VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- Table: autoliv_materials
-- Description: Autoliv-specific sustainable packaging data
-- ============================================
CREATE TABLE autoliv_materials (
    id SERIAL PRIMARY KEY,
    packaging_type VARCHAR(100) NOT NULL,
    material_type VARCHAR(100) NOT NULL,
    recyclability_pct DECIMAL(5, 2) CHECK (recyclability_pct >= 0 AND recyclability_pct <= 100),
    reusability_pct DECIMAL(5, 2) CHECK (reusability_pct >= 0 AND reusability_pct <= 100),
    carbon_footprint DECIMAL(10, 2),
    waste_reduction_impact_pct DECIMAL(5, 2) CHECK (waste_reduction_impact_pct >= 0 AND waste_reduction_impact_pct <= 100),
    supplier_sustainability_compliance_pct DECIMAL(5, 2) CHECK (supplier_sustainability_compliance_pct >= 0 AND supplier_sustainability_compliance_pct <= 100),
    cost_per_unit DECIMAL(10, 2),
    annual_usage INTEGER,
    total_material_weight DECIMAL(10, 2),
    recycled_content_pct DECIMAL(5, 2) CHECK (recycled_content_pct >= 0 AND recycled_content_pct <= 100),
    end_of_life_disposal_pct DECIMAL(5, 2) CHECK (end_of_life_disposal_pct >= 0 AND end_of_life_disposal_pct <= 100),
    sustainability_target_progress_pct DECIMAL(5, 2) CHECK (sustainability_target_progress_pct >= 0 AND sustainability_target_progress_pct <= 100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- Indexes for Performance Optimization
-- ============================================

-- Index on material_type for both tables (frequently queried)
CREATE INDEX idx_materials_type ON materials(material_type);
CREATE INDEX idx_autoliv_materials_type ON autoliv_materials(material_type);

-- Index on recyclable for filtering eco-friendly options
CREATE INDEX idx_materials_recyclable ON materials(recyclable);

-- Index on cost for budget-based queries
CREATE INDEX idx_materials_cost ON materials(cost_per_unit);
CREATE INDEX idx_autoliv_cost ON autoliv_materials(cost_per_unit);

-- Index on biodegradability and recyclability for sustainability queries
CREATE INDEX idx_materials_biodegradability ON materials(biodegradability_score);
CREATE INDEX idx_autoliv_recyclability ON autoliv_materials(recyclability_pct);

-- ============================================
-- Comments for Documentation
-- ============================================

COMMENT ON TABLE materials IS 'General eco-friendly packaging materials with sustainability metrics';
COMMENT ON TABLE autoliv_materials IS 'Autoliv-specific sustainable packaging data with detailed compliance metrics';

COMMENT ON COLUMN materials.durability_score IS 'Material durability rating from 0-10';
COMMENT ON COLUMN materials.biodegradability_score IS 'Biodegradability rating from 0-10';
COMMENT ON COLUMN materials.product_fragility IS 'Product fragility level from 0-10';

COMMENT ON COLUMN autoliv_materials.recyclability_pct IS 'Percentage of material that is recyclable (0-100)';
COMMENT ON COLUMN autoliv_materials.carbon_footprint IS 'Carbon footprint in kg CO2 per unit';
COMMENT ON COLUMN autoliv_materials.sustainability_target_progress_pct IS 'Progress towards sustainability targets (0-100)';
