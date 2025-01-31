import pandas as pd
import numpy as np
from data_value_model import DataValueModel
import sys
import os

class DatasetAnalyzer:
    def __init__(self):
        self.model = DataValueModel()
        # Load the pre-trained model
        try:
            self.model.load_model()
            print("Pre-trained model loaded successfully!")
        except:
            print("No pre-trained model found. Training new model...")
            self.model.train('cleaned_datasets_metadata.csv')
            self.model.save_model()

    def calculate_quality_metrics(self, df):
        """Calculate quality metrics for the dataset"""
        try:
            # Data Quality: Check for null values and data consistency
            null_percentage = 1 - (df.isnull().sum().sum() / (df.shape[0] * df.shape[1]))
            quality_score = max(0, min(1, null_percentage))

            # Coverage: Assess the range and distribution of data
            coverage_score = min(1, df.shape[0] / 10000)  # Example: normalize based on rows

            # History: Check for temporal aspects if available
            if 'date' in df.columns.str.lower() or 'time' in df.columns.str.lower():
                date_cols = df.select_dtypes(include=['datetime64']).columns
                if len(date_cols) > 0:
                    date_range = (df[date_cols[0]].max() - df[date_cols[0]].min()).days
                    history_score = min(1, date_range / 365)  # Normalize based on year
                else:
                    history_score = 0.5  # Default if date format not recognized
            else:
                history_score = 0.5  # Default if no date column

            return quality_score, coverage_score, history_score

        except Exception as e:
            print(f"Error calculating metrics: {str(e)}")
            return 0.5, 0.5, 0.5  # Default values in case of error

    def calculate_usd_value(self, df, quality_score, value_score):
        """Calculate estimated USD value based on dataset characteristics and quality"""
        # Base price per row (higher quality = higher base price)
        base_price_per_row = 0.01 * quality_score  # 1 cent per row at max quality
        
        # Value multiplier based on predicted value score (0-100)
        value_multiplier = (value_score / 100) * 2  # Max 2x multiplier
        
        # Column multiplier (more columns = more value)
        column_multiplier = min(2, np.log10(df.shape[1]) + 1)  # Logarithmic scaling
        
        # Calculate base value
        base_value = (
            df.shape[0] *                # Number of rows
            base_price_per_row *         # Base price per row
            value_multiplier *           # Quality-based multiplier
            column_multiplier            # Column-based multiplier
        )
        
        # Apply minimum and maximum constraints
        min_value = 50    # Minimum dataset value
        max_value = 1000000  # Maximum dataset value
        base_value = max(min_value, min(max_value, base_value))
        
        # Calculate subscription prices
        monthly_price = base_value * 0.15  # 15% of base value per month
        yearly_price = base_value * 1.5    # 1.5x base value per year
        
        return {
            'once_off': base_value,
            'monthly': monthly_price,
            'yearly': yearly_price,
            'metrics': {
                'base_price_per_row': base_price_per_row,
                'value_multiplier': value_multiplier,
                'column_multiplier': column_multiplier
            }
        }

    def analyze_dataset(self, file_path):
        """Analyze the uploaded dataset and predict its value"""
        try:
            # Read the dataset based on file type
            _, ext = os.path.splitext(file_path)
            if ext.lower() == '.csv':
                df = pd.read_csv(file_path, low_memory=False)  # Added low_memory=False to handle mixed types
            elif ext.lower() in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)
            else:
                raise ValueError("Unsupported file format. Please use CSV or Excel files.")

            # Calculate metrics
            quality, coverage, history = self.calculate_quality_metrics(df)

            # Get prediction score
            value_score = self.model.predict_value(quality, coverage, history)
            
            # Calculate USD value
            value_tiers = self.calculate_usd_value(df, quality, value_score)

            # Prepare analysis report
            report = {
                "Dataset Statistics": {
                    "Number of Rows": f"{df.shape[0]:,}",
                    "Number of Columns": df.shape[1],
                    "Memory Usage": f"{df.memory_usage().sum() / 1024**2:.2f} MB"
                },
                "Quality Metrics": {
                    "Data Quality Score": f"{quality:.2f}",
                    "Coverage Score": f"{coverage:.2f}",
                    "History Score": f"{history:.2f}"
                },
                "Value Prediction": {
                    "Quality Score": f"{value_score:.2f}/100",
                    "Once-off Purchase": f"${value_tiers['once_off']:,.2f} USD",
                    "Monthly Subscription": f"${value_tiers['monthly']:,.2f} USD/month",
                    "Yearly Subscription": f"${value_tiers['yearly']:,.2f} USD/year"
                },
                "Valuation Methodology": {
                    "Overview": [
                        "Our valuation process uses advanced machine learning to analyze your dataset and determine its market value. "
                        "We start by examining three key aspects of your data: completeness, coverage, and historical depth. "
                        f"Your dataset scored {quality:.1%} for data quality, indicating how complete and consistent the data is. "
                        f"The coverage score of {coverage:.1%} reflects how comprehensive your dataset is within its domain. "
                        f"The historical depth score of {history:.1%} measures the temporal value of your data.",
                        "",
                        f"Based on these metrics, our AI model assigned your dataset a value score of {value_score:.1f} out of 100. "
                        f"We then calculated the base price considering your dataset's {df.shape[0]:,} rows and {df.shape[1]} columns. "
                        f"The final price incorporates quality factors: a base rate of ${value_tiers['metrics']['base_price_per_row']:.4f} per row, "
                        f"adjusted by a value multiplier of {value_tiers['metrics']['value_multiplier']:.1f}x and a complexity factor of {value_tiers['metrics']['column_multiplier']:.1f}x "
                        "based on the number of data columns.",
                        "",
                        "We offer three pricing options to suit different needs: a one-time purchase for full dataset ownership, "
                        "a monthly subscription at 15% of the base value, and an annual subscription at 1.5x the base value, "
                        "which provides a 37.5% discount compared to monthly payments. This flexible pricing structure allows you "
                        "to choose the most cost-effective option for your specific use case."
                    ]
                }
            }

            return report

        except Exception as e:
            print(f"Error analyzing dataset: {str(e)}")
            return None

def print_report(report):
    """Print the analysis report in a formatted way"""
    if report is None:
        print("Analysis failed. Please check your dataset and try again.")
        return

    print("\n" + "="*50)
    print("DATASET ANALYSIS REPORT")
    print("="*50)

    for section, details in report.items():
        print(f"\n{section}:")
        print("-" * len(section))
        if isinstance(details, dict):
            for key, value in details.items():
                print(f"{key}: {value}")
        elif isinstance(details, list):
            for item in details:
                print(item)
        else:
            print(details)

def main():
    print("\n" + "="*60)
    print("Dataset Value Analyzer")
    print("="*50)
    print("\nThis tool analyzes your dataset and estimates its market value.")
    print("\nSupported file formats:")
    print("- CSV files (.csv)")
    print("- Excel files (.xlsx, .xls)")
    
    analyzer = DatasetAnalyzer()

    while True:
        print("\nTo analyze your dataset:")
        print("1. Make sure your file is in CSV or Excel format")
        print("2. Copy the full path to your file")
        print("3. Paste the path below")
        print("\nExample paths:")
        print("Windows: C:\\Users\\YourName\\Documents\\dataset.csv")
        print("Mac/Linux: /home/username/documents/dataset.csv")
        print("\nEnter 'quit' to exit the program")
        
        print("\nPlease paste your file path:")
        file_path = input().strip()

        if file_path.lower() == 'quit':
            print("\nThank you for using Dataset Value Analyzer!")
            break

        if not os.path.exists(file_path):
            print("\nError: File not found!")
            print("Please check that:")
            print("- The file path is correct")
            print("- The file exists")
            print("- You have permission to access the file")
            continue

        print("\nAnalyzing dataset...")
        print("This may take a moment depending on the size of your dataset...")
        report = analyzer.analyze_dataset(file_path)
        print_report(report)
        
        print("\nWould you like to analyze another dataset? (yes/no)")
        if input().lower().strip() != 'yes':
            print("\nThank you for using Dataset Value Analyzer!")
            break

if __name__ == "__main__":
    main() 