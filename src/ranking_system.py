import sys
from pathlib import Path
import numpy as np
import pandas as pd
import joblib

sys.path.append(str(Path(__file__).parent.parent))
from src.database_utils import get_all_materials


class MaterialRanker:
    
    def __init__(self):
        """Load trained models and scaler."""
        models_dir = Path(__file__).parent.parent / 'models'
        
        self.cost_model = joblib.load(models_dir / 'xgboost_cost_model.pkl')
        self.co2_model = joblib.load(models_dir / 'xgboost_co2_model.pkl')
        self.scaler = joblib.load(models_dir / 'feature_scaler.pkl')
        
        print("✓ Models and scaler loaded")
    
    def prepare_features(self, material, product_weight=100, product_fragility=3, shipping_distance=100):
        features = [
            material['cost_per_unit'],
            material['durability_score'],
            material['co2_footprint'],
            material['biodegradability_score'],
            product_weight,
            product_fragility,
            shipping_distance,
            int(material['recyclable'])
        ]
        return np.array(features).reshape(1, -1)
    
    def rank_materials(self, requirements=None, top_n=10):
   
        print("\n" + "=" * 70)
        print("MATERIAL RANKING SYSTEM")
        print("=" * 70)
        
        # Load all materials
        materials = get_all_materials()
        df = pd.DataFrame(materials, columns=[
            'id', 'material_type', 'cost_per_unit', 'durability_score',
            'co2_footprint', 'biodegradability_score', 'recyclable',
            'product_weight', 'product_fragility', 'shipping_distance',
            'recommended_use'
        ])
        
        print(f"\n✓ Evaluating {len(df)} materials...")
        
        # Set default requirements
        if requirements is None:
            requirements = {}
        
        eco_priority = requirements.get('eco_priority', 'medium')
        product_weight = requirements.get('product_weight', 100)
        product_fragility = requirements.get('product_fragility', 3)
        shipping_distance = requirements.get('shipping_distance', 100)
        
        ranked_materials = []
        
        for idx, row in df.iterrows():
            features = self.prepare_features(row, product_weight, product_fragility, shipping_distance)
            features_scaled = self.scaler.transform(features)
            
            # Predict cost and CO2
            pred_cost = float(self.cost_model.predict(features_scaled)[0])
            pred_co2 = float(self.co2_model.predict(features_scaled)[0])
            
            # Calculate individual scores (0-1 scale)
            # Lower cost = higher score
            cost_score = 1 - (pred_cost / float(df['cost_per_unit'].max()))
            co2_score = 1 - (pred_co2 / float(df['co2_footprint'].max()))
            durability_score = row['durability_score'] / 10
            bio_score = row['biodegradability_score'] / 10
            recyclable_bonus = 0.1 if row['recyclable'] else 0
            
            # Add bonuses based on product characteristics
            fragility_match = 0
            if product_fragility >= 4 and row['durability_score'] >= 8:
                fragility_match = 0.15
            elif product_fragility <= 2 and row['durability_score'] <= 6:
                fragility_match = 0.1
            
            weight_match = 0
            if product_weight > 1000 and row['durability_score'] >= 7:
                weight_match = 0.1
            elif product_weight < 200 and row['biodegradability_score'] >= 7:
                weight_match = 0.1
            
            distance_penalty = 0
            if shipping_distance > 1000 and row['co2_footprint'] > 2.0:
                distance_penalty = -0.15
            
            if eco_priority == 'high':
                weights = {'cost': 0.15, 'co2': 0.45, 'durability': 0.2, 'bio': 0.2}
            elif eco_priority == 'low':
                weights = {'cost': 0.55, 'co2': 0.05, 'durability': 0.3, 'bio': 0.1}
            else:
                weights = {'cost': 0.3, 'co2': 0.3, 'durability': 0.2, 'bio': 0.2}
            
            composite_score = (
                weights['cost'] * cost_score +
                weights['co2'] * co2_score +
                weights['durability'] * durability_score +
                weights['bio'] * bio_score +
                recyclable_bonus +
                fragility_match +
                weight_match +
                distance_penalty
            )
            
            composite_score = max(0, min(1, composite_score))
            
            # Apply filters
            passes_filters = True
            
            # Practical suitability check for heavy products
            unsuitable_for_heavy = ['Air Pillows', 'Aluminum Foil Packaging', 'Tissue Paper', 
                                   'Kraft Paper', 'Wax Paper', 'Parchment Paper']
            if product_weight > 2000 and row['material_type'] in unsuitable_for_heavy:
                passes_filters = False
            
            # Fragile products need durable materials
            if product_fragility >= 4 and row['durability_score'] < 6:
                passes_filters = False
            
            if 'max_cost' in requirements and pred_cost > requirements['max_cost']:
                passes_filters = False
            if 'max_co2' in requirements and pred_co2 > requirements['max_co2']:
                passes_filters = False
            if 'min_durability' in requirements and row['durability_score'] < requirements['min_durability']:
                passes_filters = False
            
            if passes_filters:
                ranked_materials.append({
                    'rank': 0,  # Will be set after sorting
                    'material': row['material_type'],
                    'score': composite_score,
                    'predicted_cost': pred_cost,
                    'predicted_co2': pred_co2,
                    'durability': row['durability_score'],
                    'biodegradability': row['biodegradability_score'],
                    'recyclable': row['recyclable'],
                    'recommended_use': row['recommended_use']
                })
        
        # Sort by score (descending)
        ranked_materials.sort(key=lambda x: x['score'], reverse=True)
        
        # Assign ranks
        for i, material in enumerate(ranked_materials[:top_n], 1):
            material['rank'] = i
        
        print(f"✓ Ranked {len(ranked_materials)} materials")
        print(f"✓ Returning top {min(top_n, len(ranked_materials))} recommendations")
        
        return ranked_materials[:top_n]
    
    def display_rankings(self, ranked_materials):
        """Display ranked materials in a formatted table."""
        print("\n" + "=" * 70)
        print("TOP MATERIAL RECOMMENDATIONS")
        print("=" * 70)
        
        for material in ranked_materials:
            print(f"\n{material['rank']}. {material['material']}")
            print(f"   Score: {material['score']:.3f}")
            print(f"   Predicted Cost: ₹{material['predicted_cost']:.2f}")
            print(f"   Predicted CO₂: {material['predicted_co2']:.3f} kg")
            print(f"   Durability: {material['durability']}/10")
            print(f"   Biodegradability: {material['biodegradability']}/10")
            print(f"   Recyclable: {'Yes' if material['recyclable'] else 'No'}")
            print(f"   Use: {material['recommended_use']}")


def demo_ranking():
    """Demonstrate ranking system with different scenarios."""
    print("\n" + "=" * 70)
    print("MATERIAL RANKING SYSTEM DEMO")
    print("=" * 70)
    
    ranker = MaterialRanker()
    
    # Scenario 1: Eco-friendly priority
    print("\n" + "-" * 70)
    print("SCENARIO 1: High Eco-Priority (Environmental Focus)")
    print("-" * 70)
    
    eco_rankings = ranker.rank_materials(
        requirements={'eco_priority': 'high'},
        top_n=5
    )
    ranker.display_rankings(eco_rankings)
    
    # Scenario 2: Budget-conscious
    print("\n" + "-" * 70)
    print("SCENARIO 2: Budget-Conscious (Cost Focus)")
    print("-" * 70)
    
    budget_rankings = ranker.rank_materials(
        requirements={'eco_priority': 'low', 'max_cost': 1000},
        top_n=5
    )
    ranker.display_rankings(budget_rankings)
    
    # Scenario 3: Balanced
    print("\n" + "-" * 70)
    print("SCENARIO 3: Balanced (Medium Priority)")
    print("-" * 70)
    
    balanced_rankings = ranker.rank_materials(
        requirements={'eco_priority': 'medium'},
        top_n=5
    )
    ranker.display_rankings(balanced_rankings)
    
    print("\n" + "=" * 70)
    print("RANKING COMPLETE!")
    print("=" * 70)


if __name__ == "__main__":
    demo_ranking()
