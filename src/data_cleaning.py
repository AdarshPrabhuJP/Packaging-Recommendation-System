"""
Data Cleaning Module
Handles data cleaning, normalization, and encoding for packaging materials.
"""

import sys
from pathlib import Path
import json
import numpy as np

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from src.database_utils import get_all_materials
from database.config import get_db_connection


def get_feature_statistics():
    """
    Get min/max values for normalization.
    
    Returns:
        dict: Statistics for each numerical feature
    """
    materials = get_all_materials()
    
    costs = [float(m[2]) for m in materials if m[2]]
    durabilities = [m[3] for m in materials if m[3]]
    co2_values = [float(m[4]) for m in materials if m[4]]
    biodegradabilities = [m[5] for m in materials if m[5]]
    weights = [m[7] for m in materials if m[7]]
    fragilites = [m[8] for m in materials if m[8]]
    shipping_distances = [m[9] for m in materials if m[9]]
    
    stats = {
        'cost_per_unit': {
            'min': min(costs),
            'max': max(costs),
            'mean': np.mean(costs),
            'std': np.std(costs)
        },
        'durability_score': {
            'min': min(durabilities),
            'max': max(durabilities),
            'mean': np.mean(durabilities),
            'std': np.std(durabilities)
        },
        'co2_footprint': {
            'min': min(co2_values),
            'max': max(co2_values),
            'mean': np.mean(co2_values),
            'std': np.std(co2_values)
        },
        'biodegradability_score': {
            'min': min(biodegradabilities),
            'max': max(biodegradabilities),
            'mean': np.mean(biodegradabilities),
            'std': np.std(biodegradabilities)
        },
        'product_weight': {
            'min': min(weights),
            'max': max(weights),
            'mean': np.mean(weights),
            'std': np.std(weights)
        },
        'product_fragility': {
            'min': min(fragilites),
            'max': max(fragilites),
            'mean': np.mean(fragilites),
            'std': np.std(fragilites)
        },
        'shipping_distance': {
            'min': min(shipping_distances),
            'max': max(shipping_distances),
            'mean': np.mean(shipping_distances),
            'std': np.std(shipping_distances)
        }
    }
    
    return stats


def normalize_value(value, min_val, max_val):
    """
    Min-Max normalization to scale value to 0-1 range.
    
    Args:
        value: Value to normalize
        min_val: Minimum value in dataset
        max_val: Maximum value in dataset
        
    Returns:
        float: Normalized value (0-1)
    """
    if max_val == min_val:
        return 0.5  # If all values are same, return middle
    return (value - min_val) / (max_val - min_val)


def standardize_value(value, mean, std):
    """
    Z-score standardization (mean=0, std=1).
    
    Args:
        value: Value to standardize
        mean: Mean of dataset
        std: Standard deviation of dataset
        
    Returns:
        float: Standardized value
    """
    if std == 0:
        return 0
    return (value - mean) / std


def normalize_materials_data():
    """
    Normalize all numerical features using Min-Max scaling.
    
    Returns:
        list: Materials with normalized features
    """
    materials = get_all_materials()
    stats = get_feature_statistics()
    
    normalized_materials = []
    
    for material in materials:
        material_id, material_type, cost, durability, co2, biodegradability, \
        recyclable, weight, fragility, shipping, recommended_use = material
        
        normalized = {
            'id': material_id,
            'material_type': material_type,
            # Original values
            'cost_per_unit': float(cost) if cost else 0,
            'durability_score': durability,
            'co2_footprint': float(co2) if co2 else 0,
            'biodegradability_score': biodegradability,
            'recyclable': recyclable,
            'product_weight': weight,
            'product_fragility': fragility,
            'shipping_distance': shipping,
            'recommended_use': recommended_use,
            # Normalized values (0-1 scale)
            'cost_normalized': normalize_value(
                float(cost) if cost else 0,
                stats['cost_per_unit']['min'],
                stats['cost_per_unit']['max']
            ),
            'durability_normalized': normalize_value(
                durability,
                stats['durability_score']['min'],
                stats['durability_score']['max']
            ),
            'co2_normalized': normalize_value(
                float(co2) if co2 else 0,
                stats['co2_footprint']['min'],
                stats['co2_footprint']['max']
            ),
            'biodegradability_normalized': normalize_value(
                biodegradability,
                stats['biodegradability_score']['min'],
                stats['biodegradability_score']['max']
            ),
            'weight_normalized': normalize_value(
                weight,
                stats['product_weight']['min'],
                stats['product_weight']['max']
            ),
            'fragility_normalized': normalize_value(
                fragility,
                stats['product_fragility']['min'],
                stats['product_fragility']['max']
            ),
            'shipping_normalized': normalize_value(
                shipping,
                stats['shipping_distance']['min'],
                stats['shipping_distance']['max']
            ),
            'recyclable_binary': 1 if recyclable else 0
        }
        
        normalized_materials.append(normalized)
    
    return normalized_materials


def encode_categorical_variables():
    """
    One-hot encode categorical variables (material_type, recommended_use).
    
    Returns:
        dict: Encoding mappings
    """
    materials = get_all_materials()
    
    # Get unique values
    material_types = list(set(m[1] for m in materials))
    recommended_uses = list(set(m[10] for m in materials if m[10]))
    
    # Create encoding
    material_type_encoding = {mat_type: i for i, mat_type in enumerate(sorted(material_types))}
    use_encoding = {use: i for i, use in enumerate(sorted(recommended_uses))}
    
    encoding_map = {
        'material_type': material_type_encoding,
        'recommended_use': use_encoding
    }
    
    return encoding_map


def get_cleaned_dataset():
    """
    Get complete cleaned and normalized dataset.
    
    Returns:
        dict: Cleaned dataset with normalized features and encodings
    """
    normalized_data = normalize_materials_data()
    encodings = encode_categorical_variables()
    
    # Add encoded categorical variables
    for material in normalized_data:
        material['material_type_encoded'] = encodings['material_type'].get(material['material_type'], -1)
        material['recommended_use_encoded'] = encodings['recommended_use'].get(material['recommended_use'], -1)
    
    return {
        'materials': normalized_data,
        'encodings': encodings,
        'statistics': get_feature_statistics()
    }


if __name__ == "__main__":
    print("=" * 60)
    print("DATA CLEANING & NORMALIZATION")
    print("=" * 60)
    
    # Get statistics
    print("\n📊 Computing feature statistics...")
    stats = get_feature_statistics()
    
    print("\nFeature Ranges:")
    for feature, values in stats.items():
        print(f"  {feature}:")
        print(f"    Min: {values['min']:.2f}, Max: {values['max']:.2f}")
        print(f"    Mean: {values['mean']:.2f}, Std: {values['std']:.2f}")
    
    # Normalize data
    print("\n🔄 Normalizing numerical features...")
    normalized = normalize_materials_data()
    print(f"✓ Normalized {len(normalized)} materials")
    
    # Encode categorical
    print("\n🏷️  Encoding categorical variables...")
    encodings = encode_categorical_variables()
    print(f"✓ Material types: {len(encodings['material_type'])} categories")
    print(f"✓ Recommended uses: {len(encodings['recommended_use'])} categories")
    
    # Get complete dataset
    print("\n📦 Creating cleaned dataset...")
    cleaned_data = get_cleaned_dataset()
    
    # Save to file
    output_file = Path(__file__).parent.parent / 'cleaned_dataset.json'
    with open(output_file, 'w') as f:
        json.dump(cleaned_data, f, indent=2)
    
    print(f"\n✅ Cleaned dataset saved to: {output_file}")
    
    # Show sample
    print("\n📋 Sample normalized material:")
    sample = cleaned_data['materials'][0]
    print(f"  Material: {sample['material_type']}")
    print(f"  Cost: ${sample['cost_per_unit']:.2f} → Normalized: {sample['cost_normalized']:.3f}")
    print(f"  CO₂: {sample['co2_footprint']:.2f} → Normalized: {sample['co2_normalized']:.3f}")
    print(f"  Durability: {sample['durability_score']}/10 → Normalized: {sample['durability_normalized']:.3f}")
    print(f"  Recyclable: {sample['recyclable']} → Binary: {sample['recyclable_binary']}")
    
    print("\n" + "=" * 60)
    print("✅ DATA CLEANING COMPLETE!")
    print("=" * 60)
