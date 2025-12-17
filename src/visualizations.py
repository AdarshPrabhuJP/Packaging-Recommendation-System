"""
Data Visualization Module
Creates charts and graphs for the Packaging Recommendation System
"""

import sys
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from src.database_utils import get_all_materials, get_database_statistics
from src.feature_engineering import (calculate_co2_impact_index, 
                                      calculate_cost_efficiency_index,
                                      calculate_material_suitability_score)

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10


def create_materials_dataframe():
    """Convert materials data to pandas DataFrame"""
    materials = get_all_materials()
    
    df = pd.DataFrame(materials, columns=[
        'id', 'material_type', 'cost_per_unit', 'durability_score',
        'co2_footprint', 'biodegradability_score', 'recyclable',
        'product_weight', 'product_fragility', 'shipping_distance',
        'recommended_use'
    ])
    
    # Convert to appropriate types
    df['cost_per_unit'] = df['cost_per_unit'].astype(float)
    df['co2_footprint'] = df['co2_footprint'].astype(float)
    df['recyclable'] = df['recyclable'].astype(bool)
    
    return df


def plot_cost_distribution():
    """Plot 1: Cost Distribution"""
    df = create_materials_dataframe()
    
    plt.figure(figsize=(10, 6))
    plt.hist(df['cost_per_unit'], bins=15, color='skyblue', edgecolor='black', alpha=0.7)
    plt.xlabel('Cost per Unit ($)', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.title('Distribution of Packaging Material Costs', fontsize=14, fontweight='bold')
    plt.axvline(df['cost_per_unit'].mean(), color='red', linestyle='--', 
                linewidth=2, label=f'Mean: ${df["cost_per_unit"].mean():.2f}')
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    
    output_path = Path(__file__).parent.parent / 'visualizations' / 'cost_distribution.png'
    output_path.parent.mkdir(exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()


def plot_sustainability_metrics():
    """Plot 2: Sustainability Metrics Comparison"""
    df = create_materials_dataframe()
    
    # Get top 10 materials by biodegradability
    top_materials = df.nlargest(10, 'biodegradability_score')
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x = np.arange(len(top_materials))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, top_materials['biodegradability_score'], 
                   width, label='Biodegradability', color='green', alpha=0.7)
    bars2 = ax.bar(x + width/2, top_materials['durability_score'], 
                   width, label='Durability', color='blue', alpha=0.7)
    
    ax.set_xlabel('Material Type', fontsize=12)
    ax.set_ylabel('Score (0-10)', fontsize=12)
    ax.set_title('Top 10 Materials: Biodegradability vs Durability', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(top_materials['material_type'], rotation=45, ha='right')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    output_path = Path(__file__).parent.parent / 'visualizations' / 'sustainability_comparison.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()


def plot_recyclability_pie():
    """Plot 3: Recyclability Distribution"""
    df = create_materials_dataframe()
    
    recyclable_counts = df['recyclable'].value_counts()
    
    plt.figure(figsize=(8, 8))
    colors = ['#66b3ff', '#ff9999']
    explode = (0.05, 0)
    
    plt.pie(recyclable_counts, labels=['Recyclable', 'Non-Recyclable'], 
            autopct='%1.1f%%', startangle=90, colors=colors, explode=explode,
            textprops={'fontsize': 12, 'fontweight': 'bold'})
    plt.title('Recyclability Distribution of Packaging Materials', 
              fontsize=14, fontweight='bold', pad=20)
    
    output_path = Path(__file__).parent.parent / 'visualizations' / 'recyclability_pie.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()


def plot_co2_vs_cost():
    """Plot 4: CO2 Footprint vs Cost Scatter Plot"""
    df = create_materials_dataframe()
    
    plt.figure(figsize=(10, 6))
    
    # Color by recyclability
    colors = df['recyclable'].map({True: 'green', False: 'red'})
    
    plt.scatter(df['co2_footprint'], df['cost_per_unit'], 
                c=colors, s=100, alpha=0.6, edgecolors='black')
    
    plt.xlabel('CO₂ Footprint', fontsize=12)
    plt.ylabel('Cost per Unit ($)', fontsize=12)
    plt.title('CO₂ Footprint vs Cost (Green=Recyclable, Red=Non-Recyclable)', 
              fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='green', label='Recyclable'),
                      Patch(facecolor='red', label='Non-Recyclable')]
    plt.legend(handles=legend_elements)
    
    output_path = Path(__file__).parent.parent / 'visualizations' / 'co2_vs_cost.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()


def plot_feature_indices():
    """Plot 5: Calculated Feature Indices"""
    materials = get_all_materials()
    
    # Calculate features for each material
    enriched = []
    for m in materials:
        co2_index = calculate_co2_impact_index(float(m[4]), m[5], m[6])
        cost_index = calculate_cost_efficiency_index(float(m[2]), m[5], m[3], m[6])
        suitability = calculate_material_suitability_score(co2_index, cost_index, m[3])
        
        enriched.append({
            'material_type': m[1],
            'co2_impact_index': co2_index,
            'cost_efficiency_index': cost_index,
            'suitability_score': suitability
        })
    
    # Get top 10 by suitability score
    top_10 = sorted(enriched, key=lambda x: x['suitability_score'], reverse=True)[:10]
    
    material_names = [m['material_type'] for m in top_10]
    co2_indices = [m['co2_impact_index'] for m in top_10]
    cost_indices = [m['cost_efficiency_index'] for m in top_10]
    suitability_scores = [m['suitability_score'] for m in top_10]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x = np.arange(len(material_names))
    width = 0.25
    
    bars1 = ax.bar(x - width, co2_indices, width, label='CO₂ Impact Index', color='green', alpha=0.7)
    bars2 = ax.bar(x, cost_indices, width, label='Cost Efficiency Index', color='blue', alpha=0.7)
    bars3 = ax.bar(x + width, suitability_scores, width, label='Suitability Score', color='orange', alpha=0.7)
    
    ax.set_xlabel('Material Type', fontsize=12)
    ax.set_ylabel('Index Score (0-100)', fontsize=12)
    ax.set_title('Top 10 Materials: Calculated Feature Indices', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(material_names, rotation=45, ha='right')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    output_path = Path(__file__).parent.parent / 'visualizations' / 'feature_indices.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()


def plot_correlation_heatmap():
    """Plot 6: Correlation Heatmap of Numerical Features"""
    df = create_materials_dataframe()
    
    # Select numerical columns
    numerical_cols = ['cost_per_unit', 'durability_score', 'co2_footprint', 
                     'biodegradability_score', 'product_weight', 'shipping_distance']
    
    correlation_matrix = df[numerical_cols].corr()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
                square=True, linewidths=1, cbar_kws={"shrink": 0.8},
                fmt='.2f', vmin=-1, vmax=1)
    plt.title('Correlation Heatmap of Material Features', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    
    output_path = Path(__file__).parent.parent / 'visualizations' / 'correlation_heatmap.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()


def plot_category_distribution():
    """Plot 7: Material Category Distribution"""
    df = create_materials_dataframe()
    
    # Count materials by category
    category_counts = df['material_type'].value_counts().head(10)
    
    plt.figure(figsize=(12, 6))
    bars = plt.barh(category_counts.index, category_counts.values, color='teal', alpha=0.7)
    plt.xlabel('Count', fontsize=12)
    plt.ylabel('Material Type', fontsize=12)
    plt.title('Top 10 Material Types by Frequency', fontsize=14, fontweight='bold')
    plt.grid(axis='x', alpha=0.3)
    
    # Add value labels
    for i, bar in enumerate(bars):
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2, 
                f'{int(width)}', ha='left', va='center', fontweight='bold')
    
    plt.tight_layout()
    output_path = Path(__file__).parent.parent / 'visualizations' / 'category_distribution.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()


def generate_all_visualizations():
    """Generate all visualizations"""
    print("=" * 60)
    print("GENERATING DATA VISUALIZATIONS")
    print("=" * 60)
    
    visualizations = [
        ("Cost Distribution", plot_cost_distribution),
        ("Sustainability Metrics", plot_sustainability_metrics),
        ("Recyclability Distribution", plot_recyclability_pie),
        ("CO₂ vs Cost Scatter", plot_co2_vs_cost),
        ("Feature Indices", plot_feature_indices),
        ("Correlation Heatmap", plot_correlation_heatmap),
        ("Category Distribution", plot_category_distribution)
    ]
    
    for i, (name, func) in enumerate(visualizations, 1):
        print(f"\n[{i}/{len(visualizations)}] Creating {name}...")
        try:
            func()
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ ALL VISUALIZATIONS GENERATED!")
    print("=" * 60)
    print(f"\nSaved to: visualizations/")
    print("\nGenerated files:")
    print("  1. cost_distribution.png")
    print("  2. sustainability_comparison.png")
    print("  3. recyclability_pie.png")
    print("  4. co2_vs_cost.png")
    print("  5. feature_indices.png")
    print("  6. correlation_heatmap.png")
    print("  7. category_distribution.png")


if __name__ == "__main__":
    generate_all_visualizations()
