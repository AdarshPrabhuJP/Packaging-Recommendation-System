"""
Feature Engineering Module
Calculates derived metrics for packaging materials:
- CO₂ Impact Index
- Cost Efficiency Index  
- Material Suitability Score
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from src.database_utils import get_all_materials


def calculate_co2_impact_index(co2_footprint, biodegradability_score, recyclable):
    """
    Calculate CO₂ Impact Index (0-100 scale, higher is better).
    
    Formula: Combines CO₂ footprint (inverted) with biodegradability and recyclability.
    - Lower CO₂ footprint = better
    - Higher biodegradability = better
    - Recyclable materials get a bonus
    
    Args:
        co2_footprint (float): CO₂ emissions
        biodegradability_score (int): Biodegradability score (0-10)
        recyclable (bool): Whether material is recyclable
        
    Returns:
        float: CO₂ Impact Index (0-100)
    """
    # Normalize CO₂ (assuming max CO₂ is 5.0, invert so lower is better)
    max_co2 = 5.0
    co2_normalized = max(0, (max_co2 - co2_footprint) / max_co2) * 100
    
    # Normalize biodegradability (0-10 scale to 0-100)
    biodegradability_normalized = (biodegradability_score / 10) * 100
    
    # Recyclable bonus
    recyclable_bonus = 10 if recyclable else 0
    
    # Weighted combination: 50% CO₂, 40% biodegradability, 10% recyclable bonus
    index = (co2_normalized * 0.5) + (biodegradability_normalized * 0.4) + recyclable_bonus
    
    return round(min(100, index), 2)


def calculate_cost_efficiency_index(cost_per_unit, biodegradability_score, durability_score, recyclable):
    """
    Calculate Cost Efficiency Index (0-100 scale, higher is better).
    
    Formula: Balance between cost and sustainability/durability.
    - Lower cost = better
    - Higher sustainability metrics = better
    
    Args:
        cost_per_unit (float): Cost per unit
        biodegradability_score (int): Biodegradability score (0-10)
        durability_score (int): Durability score (0-10)
        recyclable (bool): Whether material is recyclable
        
    Returns:
        float: Cost Efficiency Index (0-100)
    """
    # Normalize cost (assuming max cost is 50, invert so lower is better)
    max_cost = 50.0
    cost_normalized = max(0, (max_cost - cost_per_unit) / max_cost) * 100
    
    # Normalize sustainability metrics
    biodegradability_normalized = (biodegradability_score / 10) * 100
    durability_normalized = (durability_score / 10) * 100
    recyclable_bonus = 10 if recyclable else 0
    
    # Weighted combination: 40% cost, 30% biodegradability, 20% durability, 10% recyclable
    index = (cost_normalized * 0.4) + (biodegradability_normalized * 0.3) + \
            (durability_normalized * 0.2) + recyclable_bonus
    
    return round(min(100, index), 2)


def calculate_material_suitability_score(co2_footprint, biodegradability_score, 
                                         cost_per_unit, durability_score, recyclable):
    """
    Calculate overall Material Suitability Score (0-100 scale, higher is better).
    
    Formula: Comprehensive score combining all metrics.
    - Sustainability: 40% weight
    - Cost: 30% weight
    - Durability: 30% weight
    
    Args:
        co2_footprint (float): CO₂ emissions
        biodegradability_score (int): Biodegradability score (0-10)
        cost_per_unit (float): Cost per unit
        durability_score (int): Durability score (0-10)
        recyclable (bool): Whether material is recyclable
        
    Returns:
        float: Material Suitability Score (0-100)
    """
    # Sustainability component (40%)
    max_co2 = 5.0
    co2_normalized = max(0, (max_co2 - co2_footprint) / max_co2) * 100
    biodegradability_normalized = (biodegradability_score / 10) * 100
    recyclable_bonus = 20 if recyclable else 0
    sustainability = (co2_normalized * 0.5 + biodegradability_normalized * 0.5 + recyclable_bonus) / 1.2
    
    # Cost component (30%)
    max_cost = 50.0
    cost_normalized = max(0, (max_cost - cost_per_unit) / max_cost) * 100
    
    # Durability component (30%)
    durability_normalized = (durability_score / 10) * 100
    
    # Weighted combination
    score = (sustainability * 0.4) + (cost_normalized * 0.3) + (durability_normalized * 0.3)
    
    return round(min(100, score), 2)


def enrich_material_with_features(material):
    """
    Add calculated features to a material tuple.
    
    Args:
        material (tuple): Material data from database
        
    Returns:
        dict: Material data with calculated features
    """
    material_id, material_type, cost_per_unit, durability_score, \
    co2_footprint, biodegradability_score, recyclable, \
    product_weight, product_fragility, shipping_distance, recommended_use = material
    
    # Calculate features
    co2_index = calculate_co2_impact_index(co2_footprint, biodegradability_score, recyclable)
    cost_efficiency = calculate_cost_efficiency_index(cost_per_unit, biodegradability_score, 
                                                       durability_score, recyclable)
    suitability_score = calculate_material_suitability_score(co2_footprint, biodegradability_score,
                                                              cost_per_unit, durability_score, recyclable)
    
    return {
        'id': material_id,
        'material_type': material_type,
        'cost_per_unit': float(cost_per_unit) if cost_per_unit else 0,
        'durability_score': durability_score,
        'co2_footprint': float(co2_footprint) if co2_footprint else 0,
        'biodegradability_score': biodegradability_score,
        'recyclable': recyclable,
        'product_weight': product_weight,
        'product_fragility': product_fragility,
        'shipping_distance': shipping_distance,
        'recommended_use': recommended_use,
        # Calculated features
        'co2_impact_index': co2_index,
        'cost_efficiency_index': cost_efficiency,
        'material_suitability_score': suitability_score
    }


def get_all_materials_with_features():
    """
    Get all materials with calculated feature scores.
    
    Returns:
        list: List of material dictionaries with features
    """
    materials = get_all_materials()
    return [enrich_material_with_features(m) for m in materials]


if __name__ == "__main__":
    # Test the feature engineering
    print("=" * 60)
    print("FEATURE ENGINEERING TEST")
    print("=" * 60)
    
    # Get materials with features
    materials = get_all_materials_with_features()
    
    print(f"\n📊 Processed {len(materials)} materials with calculated features\n")
    
    # Show top 5 by suitability score
    sorted_materials = sorted(materials, key=lambda x: x['material_suitability_score'], reverse=True)
    
    print("🏆 Top 5 Materials by Suitability Score:")
    print("-" * 60)
    for i, material in enumerate(sorted_materials[:5], 1):
        print(f"\n{i}. {material['material_type']}")
        print(f"   Suitability Score: {material['material_suitability_score']}/100")
        print(f"   CO₂ Impact Index: {material['co2_impact_index']}/100")
        print(f"   Cost Efficiency: {material['cost_efficiency_index']}/100")
        print(f"   Cost: ${material['cost_per_unit']:.2f} | Durability: {material['durability_score']}/10")
        print(f"   CO₂: {material['co2_footprint']} | Biodegradability: {material['biodegradability_score']}/10")
        print(f"   Recyclable: {'Yes' if material['recyclable'] else 'No'}")
    
    print("\n✓ Feature engineering test completed successfully!")
