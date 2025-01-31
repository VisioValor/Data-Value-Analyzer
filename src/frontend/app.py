import streamlit as st
import pandas as pd
from pathlib import Path
import sys
import os

# Add parent directory to path to import from src
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.analyzers.dataset_analyzer import DatasetAnalyzer
from src.utils.report_utils import print_report

def create_sidebar():
    """Create the sidebar with information about the tool"""
    st.sidebar.title("About")
    st.sidebar.info(
        """
        This tool analyzes datasets and estimates their market value using 
        machine learning. Upload your CSV or Excel file to get:
        
        - Quality metrics
        - Market value estimation
        - Pricing recommendations
        - Detailed analysis report
        """
    )
    
    st.sidebar.title("Features")
    st.sidebar.markdown(
        """
        - 📊 Data Quality Analysis
        - 💰 Market Value Prediction
        - 📈 Multiple Pricing Tiers
        - 📑 Comprehensive Reports
        """
    )

def format_currency(value):
    """Format currency values with appropriate suffixes"""
    if value >= 1_000_000:
        return f"${value/1_000_000:.1f}M"
    elif value >= 1_000:
        return f"${value/1_000:.1f}K"
    else:
        return f"${value:.2f}"

def display_metrics(report):
    """Display key metrics in a clean, modern format"""
    quality_metrics = report["Quality Metrics"]
    
    # Create three columns for metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Data Quality",
            f"{float(quality_metrics['Data Quality Score']):.0%}",
            help="Measures completeness and accuracy of data"
        )
    
    with col2:
        st.metric(
            "Coverage",
            f"{float(quality_metrics['Coverage Score']):.0%}",
            help="Indicates how comprehensive the dataset is"
        )
    
    with col3:
        st.metric(
            "History Score",
            f"{float(quality_metrics['History Score']):.0%}",
            help="Reflects temporal depth of the data"
        )

def display_pricing_tiers(report):
    """Display pricing tiers in an organized table format"""
    value_pred = report["Value Prediction"]
    
    st.subheader("💰 Pricing Tiers")
    
    # Create pricing table
    pricing_data = {
        "Tier": ["Conservative", "Recommended", "Premium"],
        "One-Time Purchase": [
            value_pred["Once-off Purchase"]["Conservative"],
            value_pred["Once-off Purchase"]["Recommended"],
            value_pred["Once-off Purchase"]["Premium"]
        ],
        "Monthly Subscription": [
            value_pred["Monthly Subscription"]["Conservative"],
            value_pred["Monthly Subscription"]["Recommended"],
            value_pred["Monthly Subscription"]["Premium"]
        ],
        "Annual Subscription": [
            value_pred["Yearly Subscription"]["Conservative"],
            value_pred["Yearly Subscription"]["Recommended"],
            value_pred["Yearly Subscription"]["Premium"]
        ]
    }
    
    df_pricing = pd.DataFrame(pricing_data)
    st.dataframe(
        df_pricing.style.highlight_max(axis=0, color='lightgreen'),
        use_container_width=True
    )

def display_dataset_stats(report):
    """Display dataset statistics"""
    stats = report["Dataset Statistics"]
    
    st.subheader("📊 Dataset Overview")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Rows", stats["Number of Rows"])
    with col2:
        st.metric("Columns", stats["Number of Columns"])
    with col3:
        st.metric("Size", stats["Memory Usage"])

def main():
    st.set_page_config(
        page_title="Dataset Value Analyzer",
        page_icon="💎",
        layout="wide"
    )
    
    # Create sidebar
    create_sidebar()
    
    # Main content
    st.title("💎 Dataset Value Analyzer")
    st.markdown(
        """
        Upload your dataset to get an instant value analysis and pricing recommendations.
        Supported formats: CSV and Excel files.
        """
    )
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a file", 
        type=["csv", "xlsx", "xls"],
        help="Upload your dataset file (CSV or Excel)"
    )
    
    if uploaded_file:
        try:
            # Save the uploaded file temporarily
            temp_path = Path("temp_upload")
            temp_path.mkdir(exist_ok=True)
            file_path = temp_path / uploaded_file.name
            
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            
            # Analyze the dataset
            with st.spinner("Analyzing your dataset..."):
                analyzer = DatasetAnalyzer()
                report = analyzer.analyze_dataset(str(file_path))
            
            if report:
                # Display analysis results
                st.success("Analysis complete! 🎉")
                
                # Display key metrics
                display_metrics(report)
                
                # Add some spacing
                st.markdown("---")
                
                # Display dataset statistics
                display_dataset_stats(report)
                
                # Display pricing tiers
                display_pricing_tiers(report)
                
                # Methodology explanation
                with st.expander("📘 Valuation Methodology"):
                    for line in report["Valuation Methodology"]["Overview"]:
                        st.write(line)
                
            else:
                st.error("Analysis failed. Please check your dataset and try again.")
            
            # Cleanup
            os.remove(file_path)
            
        except Exception as e:
            st.error(f"Error analyzing dataset: {str(e)}")
            
if __name__ == "__main__":
    main() 