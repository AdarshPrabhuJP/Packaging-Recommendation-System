"""
Inference Module for Packaging Recommendation System
Load trained models and make predictions
"""

import sys
from pathlib import Path
import numpy as np
import joblib

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))


class PackagingRecommender:
    """
    Packaging material recommender using trained ML models.
    """
    
    def __init__(self):
        """Initialize and load trained models."""
        models_dir = Path(__file__).parent.parent / 'models'
        
        self.classifier = joblib.load(models_dir / 'classifier_model.pkl')
        self.label_encoder = joblib.load(models_dir / 'label_encoder.pkl')
        self.cost_model = joblib.load(models_dir / 'cost_model.pkl')
        self.co2_model = joblib.load(models_dir / 'co2_model.pkl')
        
        print("✓ Models loaded successfully")
    
    def predict(self, product_weight, product_fragility, shipping_distance, 
                durability_req=7, biodegradability_req=7, recyclable=True):
        """
        Predict best packaging material and estimated cost/CO₂.
        
        Args:
            product_weight: Weight in grams
            product_fragility: Fragility score (1-5)
            shipping_distance: Distance in km
            durability_req: Required durability (0-10)
            biodegradability_req: Required biodegradability (0-10)
            recyclable: Whether recyclable material is required
        
        Returns:
            dict: Prediction results
        """
        # Prepare features (cost will be predicted, so use average)
        avg_cost = 1000  # Placeholder
        avg_co2 = 1.5  # Placeholder
        
        features = np.array([[
            avg_cost,
            durability_req,
            avg_co2,
            biodegradability_req,
            product_weight,
            product_fragility,
            shipping_distance,
            int(recyclable)
        ]])
        
        # Predict material type
        material_encoded = self.classifier.predict(features)[0]
        material_type = self.label_encoder.inverse_transform([material_encoded])[0]
        confidence = self.classifier.predict_proba(features)[0].max()
        
        # Predict cost and CO₂
        predicted_cost = self.cost_model.predict(features)[0]
        predicted_co2 = self.co2_model.predict(features)[0]
        
        return {
            'recommended_material': material_type,
            'confidence': confidence,
            'predicted_cost': predicted_cost,
            'predicted_co2': predicted_co2
        }
    
    def get_top_recommendations(self, product_weight, product_fragility, 
                                shipping_distance, top_n=3):
        """
        Get top N material recommendations.
        
        Returns:
            list: Top N recommendations with probabilities
        """
        avg_cost = 1000
        avg_co2 = 1.5
        durability_req = 7
        biodegradability_req = 7
        recyclable = True
        
        features = np.array([[
            avg_cost, durability_req, avg_co2, biodegradability_req,
            product_weight, product_fragility, shipping_distance, int(recyclable)
        ]])
        
        # Get probabilities for all classes
        probabilities = self.classifier.predict_proba(features)[0]
        
        # Get top N indices
        top_indices = np.argsort(probabilities)[-top_n:][::-1]
        
        recommendations = []
        for idx in top_indices:
            material = self.label_encoder.inverse_transform([idx])[0]
            confidence = probabilities[idx]
            
            # Predict cost and CO₂ for this material
            cost = self.cost_model.predict(features)[0]
            co2 = self.co2_model.predict(features)[0]
            
            recommendations.append({
                'material': material,
                'confidence': confidence,
                'predicted_cost': cost,
                'predicted_co2': co2
            })
        
        return recommendations


def demo_inference():
    """
    Demonstrate inference with example products.
    """
    print("\n" + "=" * 60)
    print("PACKAGING RECOMMENDATION INFERENCE DEMO")
    print("=" * 60)
    
    # Initialize recommender
    recommender = PackagingRecommender()
    
    # Example 1: Electronics
    print("\n" + "=" * 60)
    print("Example 1: Electronics Product")
    print("=" * 60)
    print("Product: Smartphone")
    print("Weight: 200g, Fragility: 5, Distance: 500km")
    
    result = recommender.predict(
        product_weight=200,
        product_fragility=5,
        shipping_distance=500,
        durability_req=9,
        biodegradability_req=5
    )
    
    print(f"\n✓ Recommended: {result['recommended_material']}")
    print(f"  Confidence: {result['confidence']:.1%}")
    print(f"  Estimated Cost: ₹{result['predicted_cost']:.2f}")
    print(f"  Estimated CO₂: {result['predicted_co2']:.2f} kg")
    
    # Example 2: Clothing
    print("\n" + "=" * 60)
    print("Example 2: Clothing Item")
    print("=" * 60)
    print("Product: T-Shirt")
    print("Weight: 150g, Fragility: 2, Distance: 200km")
    
    result = recommender.predict(
        product_weight=150,
        product_fragility=2,
        shipping_distance=200,
        durability_req=6,
        biodegradability_req=9
    )
    
    print(f"\n✓ Recommended: {result['recommended_material']}")
    print(f"  Confidence: {result['confidence']:.1%}")
    print(f"  Estimated Cost: ₹{result['predicted_cost']:.2f}")
    print(f"  Estimated CO₂: {result['predicted_co2']:.2f} kg")
    
    # Example 3: Heavy Item
    print("\n" + "=" * 60)
    print("Example 3: Heavy Industrial Part")
    print("=" * 60)
    print("Product: Machine Part")
    print("Weight: 2000g, Fragility: 4, Distance: 1000km")
    
    result = recommender.predict(
        product_weight=2000,
        product_fragility=4,
        shipping_distance=1000,
        durability_req=10,
        biodegradability_req=4
    )
    
    print(f"\n✓ Recommended: {result['recommended_material']}")
    print(f"  Confidence: {result['confidence']:.1%}")
    print(f"  Estimated Cost: ₹{result['predicted_cost']:.2f}")
    print(f"  Estimated CO₂: {result['predicted_co2']:.2f} kg")
    
    # Top 3 recommendations
    print("\n" + "=" * 60)
    print("Top 3 Recommendations for Electronics")
    print("=" * 60)
    
    top_recs = recommender.get_top_recommendations(
        product_weight=200,
        product_fragility=5,
        shipping_distance=500,
        top_n=3
    )
    
    for i, rec in enumerate(top_recs, 1):
        print(f"\n{i}. {rec['material']}")
        print(f"   Confidence: {rec['confidence']:.1%}")
        print(f"   Cost: ₹{rec['predicted_cost']:.2f}")
        print(f"   CO₂: {rec['predicted_co2']:.2f} kg")
    
    print("\n" + "=" * 60)
    print("✅ INFERENCE DEMO COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    demo_inference()
