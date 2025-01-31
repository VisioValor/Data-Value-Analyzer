from src.models.data_value_model import DataValueModel

def test_model():
    print("Initializing Data Value Model...")
    model = DataValueModel()
    
    print("\nTraining model on dataset...")
    train_score, test_score = model.train('cleaned_datasets_metadata.csv')
    
    print("\nTesting different data value scenarios:")
    
    test_cases = [
        (1.0, 1.0, 1.0),      # Perfect data
        (0.9, 0.8, 0.7),      # High quality data
        (0.7, 0.6, 0.5),      # Medium quality data
        (0.4, 0.3, 0.2),      # Low quality data
        (0.1, 0.1, 0.1),      # Very poor data
    ]
    
    for quality, coverage, history in test_cases:
        value = model.predict_value(quality, coverage, history)
        print(f"\nTest Case:")
        print(f"  Data Quality: {quality:.2f}")
        print(f"  Coverage: {coverage:.2f}")
        print(f"  History: {history:.2f}")
        print(f"  Predicted Value Score: {value:.2f}")
    
    print("\nSaving model...")
    model.save_model()
    
    print("\nTesting model loading...")
    new_model = DataValueModel()
    new_model.load_model()
    
    # Verify loaded model works
    test_quality, test_coverage, test_history = 0.95, 0.85, 0.75
    value = new_model.predict_value(test_quality, test_coverage, test_history)
    print(f"\nVerification prediction with loaded model:")
    print(f"  Data Quality: {test_quality}")
    print(f"  Coverage: {test_coverage}")
    print(f"  History: {test_history}")
    print(f"  Predicted Value Score: {value:.2f}")

if __name__ == "__main__":
    test_model() 