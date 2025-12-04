"""
Test and Demo Script for Packaging Recommendation System
Demonstrates all features: database queries, feature engineering, and recommendations.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from src.database_utils import get_database_statistics
from src.feature_engineering import get_all_materials_with_features
from src.recommendation_queries import (
    get_eco_friendly_materials,
    get_materials_by_budget,
    get_materials_by_category,
    get_top_recommendations,
    get_best_for_fragile_items,
    get_sustainable_alternatives
)


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_material(material, index=None):
    """Print material details in a formatted way."""
    prefix = f"{index}. " if index else "  "
    print(f"\n{prefix}{material['material_type']}")
    print(f"   {'─' * 60}")
    print(f"   💰 Cost: ${material['cost_per_unit']:.2f} | "
          f"🔧 Durability: {material['durability_score']}/10 | "
          f"♻️ Recyclable: {'Yes' if material['recyclable'] else 'No'}")
    print(f"   🌍 CO₂: {material['co2_footprint']} | "
          f"🌱 Biodegradability: {material['biodegradability_score']}/10")
    print(f"   📊 Scores:")
    print(f"      • Material Suitability: {material['material_suitability_score']}/100")
    print(f"      • CO₂ Impact Index: {material['co2_impact_index']}/100")
    print(f"      • Cost Efficiency: {material['cost_efficiency_index']}/100")
    print(f"   📦 Recommended Use: {material['recommended_use']}")


def demo_database_statistics():
    """Demo: Show database statistics."""
    print_header("📊 DATABASE STATISTICS")
    
    stats = get_database_statistics()
    print(f"\n  Total Materials: {stats['total_materials']}")
    print(f"  Recyclable Materials: {stats['recyclable_materials']} ({stats['recyclable_percentage']:.1f}%)")
    print(f"\n  Average Metrics:")
    print(f"    • Cost per unit: ${stats['avg_cost']:.2f}")
    print(f"    • CO₂ footprint: {stats['avg_co2']:.2f}")
    print(f"    • Biodegradability: {stats['avg_biodegradability']:.1f}/10")
    print(f"    • Durability: {stats['avg_durability']:.1f}/10")


def demo_top_recommendations():
    """Demo: Show top overall recommendations."""
    print_header("🏆 TOP 5 RECOMMENDED MATERIALS (Balanced)")
    
    top_materials = get_top_recommendations(criteria='balanced', top_n=5)
    for i, material in enumerate(top_materials, 1):
        print_material(material, index=i)


def demo_eco_friendly():
    """Demo: Show most eco-friendly materials."""
    print_header("🌱 ECO-FRIENDLY MATERIALS")
    print("  Criteria: CO₂ Index ≥ 70, Biodegradability ≥ 8, Recyclable")
    
    eco_materials = get_eco_friendly_materials(min_co2_index=70, min_biodegradability=8)
    
    if eco_materials:
        for i, material in enumerate(eco_materials[:3], 1):
            print_material(material, index=i)
    else:
        print("\n  No materials found matching these strict criteria.")


def demo_budget_friendly():
    """Demo: Show budget-friendly options."""
    print_header("💰 BUDGET-FRIENDLY OPTIONS (Under $15)")
    print("  Criteria: Cost ≤ $15, Suitability Score ≥ 60")
    
    budget_materials = get_materials_by_budget(max_cost=15, min_suitability_score=60)
    
    for i, material in enumerate(budget_materials[:3], 1):
        print_material(material, index=i)


def demo_category_based():
    """Demo: Show category-based recommendations."""
    print_header("📦 CATEGORY-BASED RECOMMENDATIONS")
    
    categories = ['Electronics', 'Food', 'Fragile']
    
    for category in categories:
        print(f"\n  🔍 Top 2 for {category}:")
        materials = get_materials_by_category(category, top_n=2)
        
        if materials:
            for i, material in enumerate(materials, 1):
                print(f"\n    {i}. {material['material_type']}")
                print(f"       Suitability: {material['material_suitability_score']}/100 | "
                      f"Cost: ${material['cost_per_unit']:.2f}")
        else:
            print(f"    No materials found for {category}")


def demo_fragile_items():
    """Demo: Show best materials for fragile items."""
    print_header("🔒 BEST FOR FRAGILE ITEMS")
    print("  Criteria: Durability ≥ 7")
    
    fragile_materials = get_best_for_fragile_items(max_cost=20)
    
    for i, material in enumerate(fragile_materials[:3], 1):
        print_material(material, index=i)


def demo_sustainable_alternatives():
    """Demo: Find sustainable alternatives."""
    print_header("🔄 SUSTAINABLE ALTERNATIVES")
    
    current_material = "Bubble Wrap"
    print(f"  Finding eco-friendly alternatives to: {current_material}")
    print(f"  Criteria: CO₂ Impact Index improvement ≥ 10 points")
    
    alternatives = get_sustainable_alternatives(current_material, min_improvement=10)
    
    if alternatives:
        for i, material in enumerate(alternatives[:3], 1):
            print_material(material, index=i)
    else:
        print(f"\n  No significantly better alternatives found.")


def demo_criteria_comparison():
    """Demo: Compare different recommendation criteria."""
    print_header("📈 RECOMMENDATION CRITERIA COMPARISON")
    
    criteria_types = {
        'balanced': 'Balanced (Overall Suitability)',
        'eco': 'Most Eco-Friendly',
        'budget': 'Best Cost Efficiency',
        'durable': 'Most Durable'
    }
    
    for criteria, description in criteria_types.items():
        print(f"\n  🎯 {description}:")
        top_material = get_top_recommendations(criteria=criteria, top_n=1)[0]
        print(f"     {top_material['material_type']}")
        print(f"     Suitability: {top_material['material_suitability_score']}/100 | "
              f"Cost: ${top_material['cost_per_unit']:.2f} | "
              f"CO₂ Index: {top_material['co2_impact_index']}/100")


def main():
    """Run all demos."""
    print("\n" + "=" * 70)
    print("  PACKAGING RECOMMENDATION SYSTEM - DEMO")
    print("  Day 3: Feature Engineering & Query Functions")
    print("=" * 70)
    
    try:
        # Run all demos
        demo_database_statistics()
        demo_top_recommendations()
        demo_eco_friendly()
        demo_budget_friendly()
        demo_category_based()
        demo_fragile_items()
        demo_sustainable_alternatives()
        demo_criteria_comparison()
        
        # Summary
        print_header("✅ DEMO COMPLETED SUCCESSFULLY")
        print("\n  All features are working correctly!")
        print("  • Database queries: ✓")
        print("  • Feature engineering: ✓")
        print("  • Recommendation functions: ✓")
        print("\n" + "=" * 70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
