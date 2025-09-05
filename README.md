# Dataset Value Analyzer

A comprehensive tool for analyzing and determining the market value of datasets using machine learning. This application provides both a command-line interface and a web interface for easy dataset analysis.

## Features

- 📊 **Data Quality Analysis** - Comprehensive quality metrics and scoring
- 💰 **Market Value Prediction** - ML-powered value estimation with multiple pricing tiers
- 📈 **Interactive Visualizations** - Beautiful charts and graphs using Plotly
- 📑 **Detailed Reports** - Comprehensive analysis reports with recommendations
- 🌐 **Web Interface** - Easy-to-use Streamlit web application
- 💻 **CLI Interface** - Command-line tool for batch processing

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download this repository**
   ```bash
   # If you have git installed
   git clone <repository-url>
   cd datarade_scraping
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

You have two options to run the application:

#### Option 1: Web Interface (Recommended)

Run the Streamlit web application:
```bash
streamlit run src/frontend/app.py
```

Then open your browser and go to: **http://localhost:8501**

The web interface provides:
- File upload functionality
- Interactive data quality consultation
- Real-time analysis results
- Beautiful visualizations

#### Option 2: Command Line Interface

Run the command-line version:
```bash
python run_analyzer.py
```

Follow the prompts to provide the path to your dataset file.

## Supported File Formats

- CSV files (`.csv`)
- Excel files (`.xlsx`, `.xls`)

## Project Structure

```
datarade_scraping/
├── src/                          # Source code
│   ├── analyzers/               # Dataset analysis modules
│   │   └── dataset_analyzer.py  # Main analyzer class
│   ├── frontend/                # Web interface
│   │   └── app.py              # Streamlit application
│   ├── models/                  # Machine learning models
│   │   └── data_value_model.py # Value prediction model
│   ├── utils/                   # Helper functions
│   │   ├── data_cleaner.py     # Data preprocessing
│   │   └── report_utils.py     # Report generation
│   └── data_quality_consultation/ # Quality assessment
│       ├── consultation.py     # Consultation logic
│       └── visualization.py    # Visualization helpers
├── data/                        # Data files and models
│   ├── models/                 # Trained ML models
│   └── cleaned_datasets_metadata.csv
├── requirements.txt             # Python dependencies
├── run_analyzer.py             # CLI entry point
└── README.md                   # This file
```

## How It Works

1. **Data Upload**: Upload your CSV or Excel file through the web interface or provide the file path via CLI
2. **Quality Analysis**: The system analyzes your dataset for:
   - Completeness and accuracy
   - Data uniqueness and rarity
   - Volume and scale
   - Accessibility and usability
3. **Value Prediction**: Machine learning models predict the market value based on quality metrics
4. **Report Generation**: Generate comprehensive reports with pricing recommendations

## Features in Detail

### Data Quality Analysis
- **Completeness**: Checks for missing values and data gaps
- **Accuracy**: Validates data consistency and correctness
- **Uniqueness**: Assesses data rarity and exclusivity
- **Volume**: Evaluates dataset size and scale
- **Accessibility**: Measures ease of use and integration

### Market Value Prediction
- **Multiple Pricing Tiers**: Basic, Premium, and Enterprise pricing
- **ML-Powered**: Uses trained models for accurate predictions
- **Industry Benchmarks**: Compares against market standards
- **Confidence Scores**: Provides reliability indicators

### Interactive Consultation
- **Guided Assessment**: Step-by-step quality evaluation
- **Custom Scoring**: Tailored scoring based on your specific needs
- **Visual Feedback**: Real-time progress and scoring visualization

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

2. **Port Already in Use**: If port 8501 is busy, Streamlit will automatically use the next available port (8502, 8503, etc.)

3. **File Upload Issues**: Ensure your file is in CSV or Excel format and not corrupted

4. **Model Loading Warnings**: You may see scikit-learn version warnings - these are harmless and won't affect functionality

### Getting Help

If you encounter issues:
1. Check that all dependencies are properly installed
2. Ensure your Python version is 3.8 or higher
3. Verify your dataset file is in a supported format
4. Check the console output for specific error messages

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

---

**Note**: This application uses machine learning models that have been pre-trained on dataset metadata. The value predictions are estimates based on quality metrics and should be used as guidance rather than definitive market values.