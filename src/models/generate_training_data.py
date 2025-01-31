import pandas as pd
import numpy as np

def generate_training_data(output_path):
    """Generate synthetic training data for the model"""
    np.random.seed(42)
    n_samples = 1000
    
    # Generate synthetic data
    data = pd.DataFrame({
        'quality': np.random.uniform(0.5, 1.0, n_samples),
        'coverage': np.random.uniform(0.3, 1.0, n_samples),
        'history': np.random.uniform(0.2, 1.0, n_samples)
    })
    
    # Calculate synthetic value scores (0-100)
    data['value'] = (
        data['quality'] * 40 +  # Quality has highest impact
        data['coverage'] * 35 + # Coverage has medium impact
        data['history'] * 25    # History has lowest impact
    )
    
    # Add some noise to make it more realistic
    data['value'] += np.random.normal(0, 5, n_samples)
    
    # Ensure values are within 0-100 range
    data['value'] = data['value'].clip(0, 100)
    
    # Save to CSV
    data.to_csv(output_path, index=False)
    print(f"Training data generated and saved to {output_path}")
    print(f"Generated {n_samples} training samples")

if __name__ == "__main__":
    from pathlib import Path
    
    # Create data directory if it doesn't exist
    data_dir = Path(__file__).parent.parent.parent / 'data'
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate and save training data
    output_path = data_dir / 'cleaned_datasets_metadata.csv'
    generate_training_data(str(output_path)) 