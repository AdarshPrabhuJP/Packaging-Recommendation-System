"""
Recommendation Query Functions
Provides high-level functions to query and recommend packaging materials
based on various criteria.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from src.feature_engineering import get_all_materials_with_features


def get_eco_friendly_materials(min_co2_index=70, min_biodegradability=7, recyclable_only=True):
    """
    Get eco-friendly materials based on sustainability criteria.
    
    Args:
        min_co2_index (float): Minimum CO₂ Impact Index (0-100)
        min_biodegradability (int): Minimum biodegradability score (0-10)
        recyclable_only (bool): Filter for recyclable materials only
        
    Returns:
        list: Filtered and sorted list of materials
    """
    materials = get_all_materials_with_features()
    
    filtered = [
        m for m in materials
        if m['co2_impact_index'] >= min_co2_index
        and m['biodegradability_score'] >= min_biodegradability
        and (not recyclable_only or m['recyclable'])
    ]
    
    # Sort by CO₂ Impact Index (descending)
    return sorted(filtered, key=lambda x: x['co2_impact_index'], reverse=True)


def get_materials_by_budget(max_cost, min_suitability_score=50):
    """
    Get materials within budget that meet minimum suitability requirements.
    
    Args:
        max_cost (float): Maximum cost per unit
        min_suitability_score (float): Minimum material suitability score (0-100)
        
    Returns:
        list: Filtered and sorted list of materials
    """
    materials = get_all_materials_with_features()
    
    filtered = [
        m for m in materials
        if m['cost_per_unit'] <= max_cost
        and m['material_suitability_score'] >= min_suitability_score
    ]
    
    # Sort by suitability score (descending), then cost (ascending)
    return sorted(filtered, key=lambda x: (-x['material_suitability_score'], x['cost_per_unit']))


def get_materials_by_category(category, top_n=5):
    """
    Get top recommended materials for a specific product category.
    
    Args:
        category (str): Product category (e.g., 'Electronics', 'Food', 'Clothing')
        top_n (int): Number of top recommendations to return
        
    Returns:
        list: Top N materials for the category
    """
    materials = get_all_materials_with_features()
    
    # Filter by category (case-insensitive partial match)
    filtered = [
        m for m in materials
        if category.lower() in m['recommended_use'].lower()
    ]
    
    # Sort by suitability score
    sorted_materials = sorted(filtered, key=lambda x: x['material_suitability_score'], reverse=True)
    
    return sorted_materials[:top_n]


def get_top_recommendations(criteria='balanced', top_n=10):
    """
    Get top material recommendations based on different criteria.
    
    Args:
        criteria (str): Recommendation criteria
            - 'balanced': Best overall suitability score
            - 'eco': Most eco-friendly (highest CO₂ Impact Index)
            - 'budget': Best cost efficiency
            - 'durable': Highest durability
        top_n (int): Number of recommendations to return
        
    Returns:
        list: Top N recommended materials
    """
    materials = get_all_materials_with_features()
    
    if criteria == 'balanced':
        sorted_materials = sorted(materials, key=lambda x: x['material_suitability_score'], reverse=True)
    elif criteria == 'eco':
        sorted_materials = sorted(materials, key=lambda x: x['co2_impact_index'], reverse=True)
    elif criteria == 'budget':
        sorted_materials = sorted(materials, key=lambda x: x['cost_efficiency_index'], reverse=True)
    elif criteria == 'durable':
        sorted_materials = sorted(materials, key=lambda x: x['durability_score'], reverse=True)
    else:
        sorted_materials = sorted(materials, key=lambda x: x['material_suitability_score'], reverse=True)
    
    return sorted_materials[:top_n]


def compare_materials(material_ids):
    """
    Compare multiple materials side by side.
    
    Args:
        material_ids (list): List of material IDs to compare
        
    Returns:
        list: List of materials with all features
    """
    materials = get_all_materials_with_features()
    
    return [m for m in materials if m['id'] in material_ids]


def get_best_for_fragile_items(max_cost=None):
    """
    Get best materials for fragile items (high durability, low fragility handling).
    
    Args:
        max_cost (float): Optional maximum cost constraint
        
    Returns:
        list: Recommended materials for fragile items
    """
    materials = get_all_materials_with_features()
    
    # Filter for high durability
    filtered = [m for m in materials if m['durability_score'] >= 7]
    
    # Apply cost filter if specified
    if max_cost:
        filtered = [m for m in filtered if m['cost_per_unit'] <= max_cost]
    
    # Sort by durability (descending) and suitability score
    return sorted(filtered, key=lambda x: (-x['durability_score'], -x['material_suitability_score']))


def get_sustainable_alternatives(current_material_type, min_improvement=10):
    """
    Find more sustainable alternatives to a current material.
    
    Args:
        current_material_type (str): Current material type name
        min_improvement (float): Minimum improvement in CO₂ Impact Index required
        
    Returns:
        list: List of better alternatives
    """
    materials = get_all_materials_with_features()
    
    # Find current material
    current = next((m for m in materials if m['material_type'].lower() == current_material_type.lower()), None)
    
    if not current:
        return []
    
    # Find alternatives with better CO₂ Impact Index
    alternatives = [
        m for m in materials
        if m['id'] != current['id']
        and m['co2_impact_index'] >= current['co2_impact_index'] + min_improvement
    ]
    
    # Sort by CO₂ Impact Index improvement
    return sorted(alternatives, key=lambda x: x['co2_impact_index'], reverse=True)


if __name__ == "__main__":
    # Test recommendation functions
    print("=" * 60)
    print("RECOMMENDATION QUERIES TEST")
    print("=" * 60)
    
    # Test 1: Eco-friendly materials
    print("\n🌱 Top 3 Eco-Friendly Materials:")
    eco_materials = get_eco_friendly_materials(min_co2_index=70, min_biodegradability=8)
    for i, m in enumerate(eco_materials[:3], 1):
        print(f"{i}. {m['material_type']} - CO₂ Index: {m['co2_impact_index']}, Biodegradability: {m['biodegradability_score']}")
    
    # Test 2: Budget materials
    print("\n💰 Top 3 Materials Under $15:")
    budget_materials = get_materials_by_budget(max_cost=15, min_suitability_score=60)
    for i, m in enumerate(budget_materials[:3], 1):
        print(f"{i}. {m['material_type']} - Cost: ${m['cost_per_unit']}, Suitability: {m['material_suitability_score']}")
    
    # Test 3: Category-based
    print("\n📦 Top 3 Materials for Electronics:")
    electronics = get_materials_by_category('Electronics', top_n=3)
    for i, m in enumerate(electronics, 1):
        print(f"{i}. {m['material_type']} - Suitability: {m['material_suitability_score']}")
    
    # Test 4: Top balanced recommendations
    print("\n🏆 Top 5 Balanced Recommendations:")
    top_balanced = get_top_recommendations(criteria='balanced', top_n=5)
    for i, m in enumerate(top_balanced, 1):
        print(f"{i}. {m['material_type']} - Score: {m['material_suitability_score']}")
    
    print("\n✓ All recommendation tests completed successfully!")
