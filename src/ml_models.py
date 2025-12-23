import sys
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score
import joblib

sys.path.append(str(Path(__file__).parent.parent))
from src.database_utils import get_all_materials


def prepare_data():
    print("\n" + "=" * 60)
    print("PREPARING DATA FOR ML MODELS")
    print("=" * 60)
    
    # Get materials from database
    materials = get_all_materials()
    
    # Convert to DataFrame
    df = pd.DataFrame(materials, columns=[
        'id', 'material_type', 'cost_per_unit', 'durability_score',
        'co2_footprint', 'biodegradability_score', 'recyclable',
        'product_weight', 'product_fragility', 'shipping_distance',
        'recommended_use'
    ])
    
    print(f"\n✓ Loaded {len(df)} materials")
    
    # Features for prediction
    feature_columns = [
        'cost_per_unit', 'durability_score', 'co2_footprint',
        'biodegradability_score', 'product_weight', 
        'product_fragility', 'shipping_distance'
    ]
    
    X = df[feature_columns].values
    
    # Convert recyclable to int
    recyclable = df['recyclable'].astype(int).values
    
    # Add recyclable as feature
    X = np.column_stack([X, recyclable])
    
    # Targets
    y_material = df['material_type'].values  # For classification
    y_cost = df['cost_per_unit'].values  # For regression
    y_co2 = df['co2_footprint'].values  # For regression
    
    print(f"✓ Features shape: {X.shape}")
    print(f"✓ Feature columns: {feature_columns + ['recyclable']}")
    
    return X, y_material, y_cost, y_co2, df


def train_classification_model(X, y):
    """
    Train Random Forest Classifier to predict material type.
    """
    print("\n" + "=" * 60)
    print("TRAINING CLASSIFICATION MODEL")
    print("=" * 60)
    
    # Encode material types
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42
    )
    
    print(f"\n✓ Training set: {len(X_train)} samples")
    print(f"✓ Test set: {len(X_test)} samples")
    
    # Train model
    print("\n[Training Random Forest Classifier...]")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    print("✓ Model trained successfully")
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print("\n" + "=" * 60)
    print("CLASSIFICATION MODEL PERFORMANCE")
    print("=" * 60)
    print(f"Accuracy: {accuracy:.2%}")
    
    # Feature importance
    feature_names = [
        'cost', 'durability', 'co2', 'biodegradability',
        'weight', 'fragility', 'distance', 'recyclable'
    ]
    
    importances = model.feature_importances_
    print("\nFeature Importance:")
    for name, importance in sorted(zip(feature_names, importances), 
                                   key=lambda x: x[1], reverse=True):
        print(f"  {name}: {importance:.3f}")
    
    return model, le, accuracy


def train_regression_model(X, y_cost, y_co2):
    """
    Train Random Forest Regressor to predict cost and CO₂.
    """
    print("\n" + "=" * 60)
    print("TRAINING REGRESSION MODELS")
    print("=" * 60)
    
    # Split data
    X_train, X_test, y_cost_train, y_cost_test = train_test_split(
        X, y_cost, test_size=0.2, random_state=42
    )
    
    _, _, y_co2_train, y_co2_test = train_test_split(
        X, y_co2, test_size=0.2, random_state=42
    )
    
    # Train cost predictor
    print("\n[1/2] Training Cost Predictor...")
    cost_model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    cost_model.fit(X_train, y_cost_train)
    
    cost_pred = cost_model.predict(X_test)
    cost_r2 = r2_score(y_cost_test, cost_pred)
    cost_rmse = np.sqrt(mean_squared_error(y_cost_test, cost_pred))
    
    print(f"✓ Cost Model R² Score: {cost_r2:.3f}")
    print(f"✓ Cost Model RMSE: ₹{cost_rmse:.2f}")
    
    # Train CO₂ predictor
    print("\n[2/2] Training CO₂ Predictor...")
    co2_model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    co2_model.fit(X_train, y_co2_train)
    
    co2_pred = co2_model.predict(X_test)
    co2_r2 = r2_score(y_co2_test, co2_pred)
    co2_rmse = np.sqrt(mean_squared_error(y_co2_test, co2_pred))
    
    print(f"✓ CO₂ Model R² Score: {co2_r2:.3f}")
    print(f"✓ CO₂ Model RMSE: {co2_rmse:.3f} kg")
    
    return cost_model, co2_model, cost_r2, co2_r2


def save_models(classifier, label_encoder, cost_model, co2_model):
    """
    Save trained models to disk.
    """
    print("\n" + "=" * 60)
    print("SAVING MODELS")
    print("=" * 60)
    
    # Create models directory
    models_dir = Path(__file__).parent.parent / 'models'
    models_dir.mkdir(exist_ok=True)
    
    # Save models
    joblib.dump(classifier, models_dir / 'classifier_model.pkl')
    joblib.dump(label_encoder, models_dir / 'label_encoder.pkl')
    joblib.dump(cost_model, models_dir / 'cost_model.pkl')
    joblib.dump(co2_model, models_dir / 'co2_model.pkl')
    
    print(f"✓ Saved to: {models_dir}")
    print("  - classifier_model.pkl")
    print("  - label_encoder.pkl")
    print("  - cost_model.pkl")
    print("  - co2_model.pkl")


def main():
    """
    Main function to train all models.
    """
    print("\n" + "=" * 60)
    print("ML MODEL TRAINING PIPELINE")
    print("Packaging Recommendation System")
    print("=" * 60)
    
    # Prepare data
    X, y_material, y_cost, y_co2, df = prepare_data()
    
    # Train classification model
    classifier, label_encoder, accuracy = train_classification_model(X, y_material)
    
    # Train regression models
    cost_model, co2_model, cost_r2, co2_r2 = train_regression_model(X, y_cost, y_co2)
    
    # Save models
    save_models(classifier, label_encoder, cost_model, co2_model)
    
    # Summary
    print("\n" + "=" * 60)
    print("TRAINING SUMMARY")
    print("=" * 60)
    print(f"Dataset size: {len(df)} materials")
    print(f"Classification Accuracy: {accuracy:.2%}")
    print(f"Cost Prediction R²: {cost_r2:.3f}")
    print(f"CO₂ Prediction R²: {co2_r2:.3f}")
    print("\n✅ ALL MODELS TRAINED SUCCESSFULLY!")
    print("=" * 60)


if __name__ == "__main__":
    main()
