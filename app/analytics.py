import sys
from pathlib import Path
import pandas as pd
import numpy as np

sys.path.append(str(Path(__file__).parent.parent))
from src.database_utils import get_all_materials

class Analytics:
    
    def __init__(self):
        self.materials = get_all_materials()
        self.df = pd.DataFrame(self.materials, columns=[
            'id', 'material_type', 'cost_per_unit', 'durability_score',
            'co2_footprint', 'biodegradability_score', 'recyclable',
            'product_weight', 'product_fragility', 'shipping_distance',
            'recommended_use'
        ])
    
    def calculate_co2_reduction(self):
        baseline_co2 = float(self.df['co2_footprint'].mean())
        eco_materials = self.df[self.df['biodegradability_score'] >= 7]
        eco_co2 = float(eco_materials['co2_footprint'].mean()) if len(eco_materials) > 0 else baseline_co2
        
        reduction_percent = ((baseline_co2 - eco_co2) / baseline_co2) * 100
        
        return {
            'baseline_co2': round(baseline_co2, 3),
            'eco_co2': round(eco_co2, 3),
            'reduction_percent': round(reduction_percent, 2),
            'total_saved': round(baseline_co2 - eco_co2, 3)
        }
    
    def calculate_cost_savings(self):
        baseline_cost = float(self.df['cost_per_unit'].mean())
        budget_materials = self.df[self.df['cost_per_unit'] <= self.df['cost_per_unit'].median()]
        budget_cost = float(budget_materials['cost_per_unit'].mean())
        
        savings_percent = ((baseline_cost - budget_cost) / baseline_cost) * 100
        
        return {
            'baseline_cost': round(baseline_cost, 2),
            'budget_cost': round(budget_cost, 2),
            'savings_percent': round(savings_percent, 2),
            'total_saved': round(baseline_cost - budget_cost, 2)
        }
    
    def get_material_usage_trends(self):
        recyclable_count = int(self.df['recyclable'].sum())
        total_count = len(self.df)
        
        material_categories = {
            'Eco-Friendly': len(self.df[self.df['biodegradability_score'] >= 7]),
            'Budget': len(self.df[self.df['cost_per_unit'] <= self.df['cost_per_unit'].median()]),
            'Durable': len(self.df[self.df['durability_score'] >= 7]),
            'Recyclable': recyclable_count,
            'Non-Recyclable': total_count - recyclable_count
        }
        
        return material_categories
    
    def get_sustainability_metrics(self):
        eco_score_ranges = {
            'Excellent (9-10)': len(self.df[self.df['biodegradability_score'] >= 9]),
            'Good (7-8)': len(self.df[(self.df['biodegradability_score'] >= 7) & (self.df['biodegradability_score'] < 9)]),
            'Fair (5-6)': len(self.df[(self.df['biodegradability_score'] >= 5) & (self.df['biodegradability_score'] < 7)]),
            'Poor (1-4)': len(self.df[self.df['biodegradability_score'] < 5])
        }
        
        return eco_score_ranges
    
    def get_key_metrics(self):
        co2_data = self.calculate_co2_reduction()
        cost_data = self.calculate_cost_savings()
        
        return {
            'total_materials': len(self.df),
            'co2_saved_percent': co2_data['reduction_percent'],
            'cost_saved': cost_data['total_saved'],
            'eco_friendly_percent': round((len(self.df[self.df['recyclable'] == True]) / len(self.df)) * 100, 1)
        }
    
    def get_top_materials(self, n=10):
        eco_materials = self.df.nlargest(n, 'biodegradability_score')
        
        return [{
            'material': row['material_type'],
            'eco_score': row['biodegradability_score'],
            'cost': float(row['cost_per_unit']),
            'co2': float(row['co2_footprint'])
        } for _, row in eco_materials.iterrows()]
