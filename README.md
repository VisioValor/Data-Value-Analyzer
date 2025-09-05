# VisioValor Data Valuation App

A comprehensive tool for analyzing and determining the market value of datasets using machine learning. This application provides both a command-line interface and a web interface for easy dataset analysis.

**🔐 Secure Access Required** - Login authentication system protects your data and analysis.

## Features

- 🔐 **Secure Authentication** - Login system protects your data and analysis
- 📊 **Data Quality Analysis** - Comprehensive quality metrics and scoring
- 💰 **Market Value Prediction** - ML-powered value estimation with multiple pricing tiers
- 📈 **Interactive Visualizations** - Beautiful charts and graphs using Plotly
- 📑 **PDF Report Generation** - Download comprehensive analysis reports
- 🌐 **Web Interface** - Easy-to-use Streamlit web application
- 💻 **CLI Interface** - Command-line tool for batch processing
- 🤝 **Data Consultation** - Interactive quality assessment workflow
- 📋 **Progress Tracking** - Visual progress indicators for analysis steps

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

**Login Credentials:**
- **Username:** `admin`
- **Password:** `D@ta4L1fe!`

The web interface provides:
- Secure login authentication
- File upload functionality
- Interactive data quality consultation
- Real-time analysis results
- Beautiful visualizations
- PDF report generation

#### Option 2: Command Line Interface

Run the command-line version:
```bash
python run_analyzer.py
```

Follow the prompts to provide the path to your dataset file.

## Supported File Formats

- CSV files (`.csv`)
- Excel files (`.xlsx`, `.xls`)
- JSON files (`.json`)

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
│   │   ├── auth.py             # Authentication system
│   │   ├── data_cleaner.py     # Data preprocessing
│   │   ├── pdf_report_generator.py # PDF report generation
│   │   ├── report_collector.py # Report data collection
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

1. **Authentication**: Login with your credentials to access the application
2. **Data Upload**: Upload your CSV, Excel, or JSON file through the web interface
3. **Data Quality Check**: The system analyzes your dataset for:
   - Completeness and accuracy
   - Data coverage and history
   - Missing values and data quality
4. **Data Consultation**: Interactive assessment covering:
   - Data uniqueness and rarity
   - Volume and scale
   - Access and governance
   - Security and monetization
5. **Value Analysis**: Machine learning models predict market value with:
   - Multiple pricing tiers
   - Confidence scores
   - Industry benchmarks
6. **Report Generation**: Download comprehensive PDF reports with all analysis results

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
- **Progress Tracking**: Visual indicators for completion status

### PDF Report Generation
- **Comprehensive Reports**: All analysis results in one document
- **Professional Formatting**: Clean, branded report layout
- **Download Ready**: Instant PDF generation and download
- **Complete Analysis**: Includes quality metrics, consultation results, and valuation

### Security Features
- **Login Authentication**: Secure access with username/password
- **Session Management**: 24-hour session timeout
- **Data Protection**: Your data stays secure during analysis

## Troubleshooting

### Common Issues

1. **Login Issues**: Make sure you're using the correct credentials:
   - Username: `admin`
   - Password: `D@ta4L1fe!`

2. **Import Errors**: Make sure all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

3. **Port Already in Use**: If port 8501 is busy, Streamlit will automatically use the next available port (8502, 8503, etc.)

4. **File Upload Issues**: Ensure your file is in CSV, Excel, or JSON format and not corrupted

5. **Model Loading Warnings**: You may see scikit-learn version warnings - these are harmless and won't affect functionality

6. **Session Timeout**: If you're logged out automatically, simply log in again - sessions expire after 24 hours

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