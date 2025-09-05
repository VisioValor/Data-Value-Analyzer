import pandas as pd
import numpy as np
import os
from pathlib import Path
from ..models.data_value_model import DataValueModel

class DatasetAnalyzer:
    """
    Analyzes datasets to determine their market value based on various quality metrics.
    Uses machine learning to predict dataset value and generates detailed reports.
    """
    
    def __init__(self):
        """
        Initialize the analyzer with a DataValueModel.
        """
        self.model = DataValueModel()
        
        # Create base directory paths
        self.base_dir = Path(__file__).parent.parent.parent
        self.model_dir = self.base_dir / 'data' / 'models'
        self.data_dir = self.base_dir / 'data'
        
        # Create directories if they don't exist
        self.model_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Set model path
        self.model_path = self.model_dir / 'data_value_model.joblib'
        self.metadata_path = self.data_dir / 'cleaned_datasets_metadata.csv'
        
        self._load_or_train_model()

    def _load_or_train_model(self):
        """Loads existing model or trains a new one if not found."""
        try:
            self.model.load_model(str(self.model_path))
            print("Pre-trained model loaded successfully!")
        except:
            print("No pre-trained model found. Training new model...")
            self.model.train(str(self.metadata_path))
            self.model.save_model(str(self.model_path))

    def analyze_dataset(self, file_path, consultation_results=None):
        """
        Analyze a dataset file and generate a comprehensive value report.
        
        Args:
            file_path (str): Path to the dataset file (CSV or Excel)
            consultation_results (dict): Optional consultation results with weighted scores
            
        Returns:
            dict: Detailed analysis report including statistics, quality metrics, and valuations
        """
        try:
            df = self._load_dataset(file_path)
            quality, coverage, history = self.calculate_quality_metrics(df)
            
            # Use consultation results if available, otherwise fall back to ML model
            if consultation_results and 'total_score' in consultation_results:
                # Convert consultation score (0-10 scale) to value score (0-100 scale)
                consultation_score = consultation_results['total_score']
                value_score = min(100, max(0, consultation_score * 10))  # Scale 0-10 to 0-100
                
                # Enhance with basic quality metrics
                enhanced_value_score = self._enhance_with_quality_metrics(
                    value_score, quality, coverage, history
                )
            else:
                # Fall back to ML model prediction
                value_score = self.model.predict_value(quality, coverage, history)
                enhanced_value_score = value_score
            
            value_tiers = self.calculate_usd_value(df, quality, enhanced_value_score)
            
            return self._generate_report(df, quality, coverage, history, enhanced_value_score, value_tiers, consultation_results)
        except Exception as e:
            print(f"Error analyzing dataset: {str(e)}")
            return None

    def _load_dataset(self, file_path):
        """Load dataset from file based on extension."""
        _, ext = os.path.splitext(file_path)
        if ext.lower() == '.csv':
            return pd.read_csv(file_path, low_memory=False)
        elif ext.lower() in ['.xlsx', '.xls']:
            return pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format. Please use CSV or Excel files.")

    def calculate_quality_metrics(self, df):
        """
        Calculate quality metrics for the dataset.
        
        Args:
            df (pd.DataFrame): The dataset to analyze
            
        Returns:
            tuple: (quality_score, coverage_score, history_score)
        """
        try:
            # Data Quality: Check for null values and data consistency
            null_percentage = 1 - (df.isnull().sum().sum() / (df.shape[0] * df.shape[1]))
            quality_score = max(0, min(1, null_percentage))

            # Coverage: Assess the range and distribution of data
            # Normalize based on number of rows (10,000 rows = 1.0 score)
            coverage_score = min(1, df.shape[0] / 10000)

            # History: Check for temporal aspects if available
            history_score = self._calculate_history_score(df)

            return quality_score, coverage_score, history_score

        except Exception as e:
            print(f"Error calculating metrics: {str(e)}")
            return 0.5, 0.5, 0.5  # Default values in case of error

    def _calculate_history_score(self, df):
        """Calculate history score based on temporal data if available."""
        # Look for date/time columns
        date_columns = []
        
        # Check column names for date-related terms
        date_terms = ['date', 'time', 'year', 'month', 'day']
        for col in df.columns:
            if any(term in col.lower() for term in date_terms):
                date_columns.append(col)

        if date_columns:
            try:
                # Convert first found date column to datetime
                date_col = df[date_columns[0]]
                if not pd.api.types.is_datetime64_any_dtype(date_col):
                    date_col = pd.to_datetime(date_col, errors='coerce')

                if not date_col.isnull().all():
                    # Calculate date range in days
                    date_range = (date_col.max() - date_col.min()).days
                    # Normalize: 1 year = 0.8 score, 2 years = 0.9 score, 3+ years = 1.0 score
                    if date_range <= 365:
                        return min(0.8, date_range / (365 * 0.8))
                    elif date_range <= 730:
                        return 0.8 + (date_range - 365) / (365 * 10)
                    else:
                        return 1.0

            except Exception as e:
                print(f"Error processing date column: {str(e)}")
                return 0.5

        return 0.5  # Default score if no valid date columns found

    def _enhance_with_quality_metrics(self, consultation_score, quality, coverage, history):
        """
        Enhance consultation score with basic quality metrics.
        
        Args:
            consultation_score (float): Base consultation score (0-100)
            quality (float): Data quality score (0-1)
            coverage (float): Data coverage score (0-1)
            history (float): Data history score (0-1)
            
        Returns:
            float: Enhanced value score (0-100)
        """
        # Convert quality metrics to 0-100 scale
        quality_100 = quality * 100
        coverage_100 = coverage * 100
        history_100 = history * 100
        
        # Weighted combination: 70% consultation, 30% quality metrics
        enhanced_score = (
            consultation_score * 0.7 +  # Primary: consultation results
            quality_100 * 0.15 +        # Secondary: data quality
            coverage_100 * 0.10 +       # Tertiary: data coverage
            history_100 * 0.05          # Quaternary: data history
        )
        
        return min(100, max(0, enhanced_score))

    def calculate_usd_value(self, df, quality_score, value_score):
        """
        Calculate estimated USD value based on dataset characteristics and quality.
        Includes low, medium, and high estimates for each pricing tier.
        
        Args:
            df (pd.DataFrame): The dataset
            quality_score (float): Quality metric (0-1)
            value_score (float): Predicted value score (0-100)
            
        Returns:
            dict: Value tiers and calculation metrics with low/medium/high estimates
        """
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
        
        # Calculate price variations
        low_multiplier = 0.8     # 20% below base price
        high_multiplier = 1.2    # 20% above base price
        
        # Calculate subscription prices with variations
        price_tiers = {
            'once_off': {
                'low': base_value * low_multiplier,
                'medium': base_value,
                'high': base_value * high_multiplier
            },
            'monthly': {
                'low': (base_value * 0.15) * low_multiplier,    # 15% of base value per month
                'medium': base_value * 0.15,
                'high': (base_value * 0.15) * high_multiplier
            },
            'yearly': {
                'low': (base_value * 1.5) * low_multiplier,     # 1.5x base value per year
                'medium': base_value * 1.5,
                'high': (base_value * 1.5) * high_multiplier
            },
            'metrics': {
                'base_price_per_row': base_price_per_row,
                'value_multiplier': value_multiplier,
                'column_multiplier': column_multiplier
            }
        }
        
        return price_tiers

    def _generate_report(self, df, quality, coverage, history, value_score, value_tiers, consultation_results=None):
        """Generate a comprehensive analysis report."""
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
                "Once-off Purchase": {
                    "Conservative": f"${value_tiers['once_off']['low']:,.2f} USD",
                    "Recommended": f"${value_tiers['once_off']['medium']:,.2f} USD",
                    "Premium": f"${value_tiers['once_off']['high']:,.2f} USD"
                },
                "Monthly Subscription": {
                    "Conservative": f"${value_tiers['monthly']['low']:,.2f} USD/month",
                    "Recommended": f"${value_tiers['monthly']['medium']:,.2f} USD/month",
                    "Premium": f"${value_tiers['monthly']['high']:,.2f} USD/month"
                },
                "Yearly Subscription": {
                    "Conservative": f"${value_tiers['yearly']['low']:,.2f} USD/year",
                    "Recommended": f"${value_tiers['yearly']['medium']:,.2f} USD/year",
                    "Premium": f"${value_tiers['yearly']['high']:,.2f} USD/year"
                }
            },
            "Valuation Methodology": {
                "Overview": [
                    f"We've analyzed your dataset using advanced AI technology to determine its market value. "
                    f"Your data shows a quality score of {quality:.1%}, which measures how complete and accurate your dataset is. "
                    f"The coverage score of {coverage:.1%} tells us how comprehensive your data is, and the historical depth "
                    f"score of {history:.1%} indicates how well it captures changes over time.",
                    "",
                    f"Based on these factors, your dataset received an overall value score of {value_score:.1f} out of 100. "
                    f"We looked at your {df.shape[0]:,} rows of data and {df.shape[1]} different types of information "
                    "to calculate fair market prices across different tiers.",
                    "",
                    "For each pricing option (one-time purchase, monthly subscription, or yearly subscription), "
                    "we provide three price points:",
                    "- Conservative: A lower-risk pricing suitable for bulk purchases or long-term commitments",
                    "- Recommended: Our suggested optimal price based on market analysis",
                    "- Premium: A premium tier for high-value use cases or exclusive rights",
                    "",
                    "The yearly subscription offers the best value, providing a significant discount compared to "
                    "monthly payments while ensuring access to updates and support."
                ]
            }
        }
        
        # Add consultation results if available
        if consultation_results and 'total_score' in consultation_results:
            report["Consultation Results"] = {
                "Total Weighted Score": f"{consultation_results['total_score']:.2f}/10",
                "Categories": consultation_results.get('categories', {}),
                "Methodology": "Enhanced valuation based on comprehensive data consultation assessment"
            }
        
        return report 