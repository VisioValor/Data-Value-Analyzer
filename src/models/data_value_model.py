import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib
from pathlib import Path

class DataValueModel:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.is_trained = False
        self.scaler = StandardScaler()
        
    def train(self, metadata_path):
        """Train the model using historical dataset metadata"""
        try:
            # Load and preprocess training data
            data = pd.read_csv(metadata_path)
            
            # Prepare features and target
            X = data[['quality', 'coverage', 'history']]
            y = data['value']
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Train model
            self.model.fit(X_train, y_train)
            self.is_trained = True
            
            # Print model performance
            train_score = self.model.score(X_train, y_train)
            test_score = self.model.score(X_test, y_test)
            print(f"Training R² Score: {train_score:.4f}")
            print(f"Testing R² Score: {test_score:.4f}")
            
        except Exception as e:
            print(f"Error training model: {str(e)}")
            raise
    
    def predict_value(self, quality, coverage, history):
        """
        Predict the value of data based on its metrics
        
        Args:
            quality (float): Data quality score (0-1)
            coverage (float): Data coverage score (0-1)
            history (float): Data history score (0-1)
            
        Returns:
            float: Predicted value score (0-100)
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
            
        features = np.array([[quality, coverage, history]])
        return self.model.predict(features)[0]
    
    def save_model(self, model_path):
        """Save the trained model"""
        if not self.is_trained:
            raise ValueError("Model must be trained before saving")
            
        # Create directory if it doesn't exist
        Path(model_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Save the model
        joblib.dump({
            'model': self.model,
            'is_trained': self.is_trained
        }, model_path)
        
    def load_model(self, model_path):
        """Load a trained model"""
        saved_model = joblib.load(model_path)
        self.model = saved_model['model']
        self.is_trained = saved_model['is_trained']

# Example usage
if __name__ == "__main__":
    model = DataValueModel()
    
    # Train the model
    model.train('cleaned_datasets_metadata.csv')
    
    # Save the model
    model.save_model('data/models/data_value_model.joblib')
    
    # Example prediction
    sample_quality = 0.95
    sample_coverage = 0.85
    sample_history = 0.75
    
    predicted_value = model.predict_value(sample_quality, sample_coverage, sample_history)
    print(f"\nExample Prediction:")
    print(f"Data Quality: {sample_quality}")
    print(f"Coverage: {sample_coverage}")
    print(f"History: {sample_history}")
    print(f"Predicted Value Score: {predicted_value:.2f}") 