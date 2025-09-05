import streamlit as st
import pandas as pd
from pathlib import Path
import sys
import os
import io
import numpy as np
from datetime import datetime

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.analyzers.dataset_analyzer import DatasetAnalyzer
from src.utils.report_utils import print_report
from src.data_quality_consultation.consultation import DataConsultation
from src.utils.pdf_report_generator import PDFReportGenerator
from src.utils.report_collector import ReportCollector

# Import from data_quality_tool if needed
# from data_quality_tool.app import analyze_data_quality

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

def analyze_data_quality(df):
    """
    Analyze data quality and return a detailed report following the original tool's structure
    """
    report = {
        "1. Dataset Overview": {
            "Number of rows": df.shape[0],
            "Number of columns": df.shape[1]
        },
        "2. Missing Values": {},
        "3. Duplicate Rows": {
            "count": df.duplicated().sum()
        },
        "4. Data Types": df.dtypes.to_dict(),
        "5. Descriptive Statistics": df.describe().to_dict(),
        "6. Categorical Columns": {}
    }

    # Missing values analysis
    missing_values = df.isnull().sum()
    missing_summary = missing_values[missing_values > 0]
    report["2. Missing Values"] = missing_summary.to_dict()

    # Categorical columns analysis
    categorical_columns = df.select_dtypes(include=["object"]).columns
    for col in categorical_columns:
        report["6. Categorical Columns"][col] = df[col].nunique()

    return report

def display_quality_report(report, df):
    """Display the data quality report in a structured format"""
    st.header("📊 Data Quality Analysis Report")
    
    # 1. Dataset Overview
    st.subheader("1. Dataset Overview")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Number of Rows", f"{report['1. Dataset Overview']['Number of rows']:,}")
    with col2:
        st.metric("Number of Columns", report['1. Dataset Overview']['Number of columns'])
    
    # 2. Missing Values
    st.subheader("2. Missing Values")
    if report['2. Missing Values']:
        missing_df = pd.DataFrame.from_dict(report['2. Missing Values'], 
                                          orient='index', 
                                          columns=['Count'])
        missing_df['Percentage'] = (missing_df['Count'] / report['1. Dataset Overview']['Number of rows'] * 100).round(2)
        st.dataframe(missing_df.style.background_gradient(cmap='Reds'))
    else:
        st.success("✅ No missing values found!")
    
    # 3. Duplicate Rows
    st.subheader("3. Duplicate Rows")
    if report['3. Duplicate Rows']['count'] > 0:
        st.warning(f"⚠️ Found {report['3. Duplicate Rows']['count']:,} duplicate rows")
    else:
        st.success("✅ No duplicate rows found!")
    
    # 4. Data Types
    st.subheader("4. Data Types and Inconsistencies")
    dtype_df = pd.DataFrame.from_dict(report['4. Data Types'], 
                                    orient='index', 
                                    columns=['Type'])
    # Convert object dtype to string for better Arrow compatibility
    dtype_df['Type'] = dtype_df['Type'].astype(str)
    st.dataframe(dtype_df)
    
    # 5. Descriptive Statistics
    st.subheader("5. Descriptive Statistics (Numerical Columns)")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if not numeric_cols.empty:
        desc_stats = df[numeric_cols].describe()
        # Format numbers without converting to string first
        st.dataframe(
            desc_stats.style.format(formatter=lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else x)
        )
    else:
        st.info("No numerical columns found in the dataset.")
    
    # 6. Categorical Columns
    st.subheader("6. Unique Values in Categorical Columns")
    if report['6. Categorical Columns']:
        cat_df = pd.DataFrame.from_dict(report['6. Categorical Columns'], 
                                      orient='index', 
                                      columns=['Unique Values'])
        st.dataframe(cat_df.style.background_gradient(cmap='Blues'))
    else:
        st.info("No categorical columns found in the dataset.")

def download_cleaned_data(df):
    """Create a download button for the cleaned dataset"""
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    return buffer

def create_progress_sidebar():
    """Create a detailed progress tracking sidebar"""
    st.sidebar.title("Navigation")
    
    # Define steps and their requirements
    steps = {
        "Data Quality Check": {
            "icon": "🔍",
            "substeps": [
                "Upload Data",
                "Quality Analysis",
                "Data Cleaning"
            ],
            "required": True
        },
        "Data Consultation": {
            "icon": "🤝",
            "substeps": [
                "Data Uniqueness",
                "Data Volume",
                "Data Quality",
                "Data Access",
                "Data Governance",
                "Data Security",
                "Monetization",
                "Strategic Value"
            ],
            "required": True
        },
        "Value Analysis": {
            "icon": "💎",
            "substeps": [
                "Value Calculation",
                "Pricing Analysis",
                "Report Generation"
            ],
            "required": True
        }
    }
    
    # Calculate overall progress
    total_steps = sum(len(step["substeps"]) for step in steps.values())
    completed_steps = 0
    
    # Display progress for each main step
    st.sidebar.markdown("### Progress Overview")
    current_page = st.session_state.page
    
    for step_name, step_info in steps.items():
        # Determine step status
        if step_name == current_page:
            status = "in_progress"
        elif completed_steps == total_steps:
            status = "completed"
        elif step_name == "Data Quality Check" and st.session_state.cleaned_df is not None:
            status = "completed"
        elif step_name == "Data Consultation" and st.session_state.consultation_complete:
            status = "completed"
        elif step_name == "Value Analysis" and 'valuation_complete' in st.session_state:
            status = "completed"
        else:
            status = "pending"
        
        # Create expandable section for each step
        with st.sidebar.expander(f"{step_info['icon']} {step_name}", 
                               expanded=(step_name == current_page)):
            # Display substeps
            for substep in step_info["substeps"]:
                if status == "completed":
                    st.markdown(f"✅ {substep}")
                    completed_steps += 1
                elif status == "in_progress" and step_name == current_page:
                    # Check specific substep completion
                    if step_name == "Data Consultation" and 'consultation_step' in st.session_state:
                        current_substep_index = st.session_state.consultation_step
                        substep_index = step_info["substeps"].index(substep)
                        if substep_index < current_substep_index:
                            st.markdown(f"✅ {substep}")
                            completed_steps += 1
                        elif substep_index == current_substep_index:
                            st.markdown(f"🔵 {substep}")
                        else:
                            st.markdown(f"⚪ {substep}")
                    else:
                        st.markdown(f"⚪ {substep}")
                else:
                    st.markdown(f"⚪ {substep}")
    
    # Display overall progress bar
    progress = completed_steps / total_steps
    st.sidebar.markdown("### Overall Progress")
    st.sidebar.progress(progress)
    st.sidebar.markdown(f"**{progress:.0%}** Complete")
    
    # Add helpful information
    if current_page == "Data Quality Check":
        st.sidebar.info("💡 Upload your dataset and review its quality metrics")
    elif current_page == "Data Consultation":
        st.sidebar.info("💡 Answer questions about your dataset to help determine its value")
    elif current_page == "Value Analysis":
        st.sidebar.info("💡 Review the final analysis and value estimation")

def main():
    st.set_page_config(
        page_title="Dataset Analysis Suite",
        page_icon="💎",
        layout="wide"
    )
    
    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = "Data Quality Check"
    if 'cleaned_df' not in st.session_state:
        st.session_state.cleaned_df = None
    if 'consultation_complete' not in st.session_state:
        st.session_state.consultation_complete = False
    
    # Create detailed progress sidebar
    create_progress_sidebar()
    
    # Create sidebar
    st.sidebar.title("Navigation")
    
    # Create radio button - let it control the page directly
    page = st.sidebar.radio(
        "Go to", 
        ["Data Quality Check", "Data Consultation", "Value Analysis"],
        index=["Data Quality Check", "Data Consultation", "Value Analysis"].index(st.session_state.page),
        key="navigation_radio"
    )
    
    # Update session state if radio button selection changed
    if page != st.session_state.page:
        st.session_state.page = page
        st.rerun()
    
    # Use the page from radio button for consistency
    current_page = page
    
    if current_page == "Data Quality Check":
        st.title("🔍 Data Quality Analysis")
        st.markdown("""
        Before valuing your dataset, let's analyze its quality and make necessary improvements.
        Upload your file to begin the analysis.
        
        **Supported formats:**
        - CSV (.csv)
        - Excel (.xlsx, .xls)
        - JSON (.json)
        """)
        
        uploaded_file = st.file_uploader(
            "Choose a file", 
            type=["csv", "xlsx", "xls", "json"],
            help="Upload your dataset file"
        )
        
        if uploaded_file:
            try:
                # Load the data based on file type
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                elif uploaded_file.name.endswith('.json'):
                    df = pd.read_json(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                # Analyze data quality
                with st.spinner("Analyzing data quality..."):
                    quality_report = analyze_data_quality(df)
                    display_quality_report(quality_report, df)
                
                # Data Cleaning Options
                st.header("🧹 Data Cleaning Options")
                
                with st.expander("Clean Dataset", expanded=True):
                    # Handle missing values
                    st.subheader("Handle Missing Values")
                    missing_strategy = st.selectbox(
                        "Choose how to handle missing values:",
                        ["Keep as is", "Drop rows", "Fill with mean/mode"]
                    )
                    
                    if missing_strategy == "Drop rows":
                        df = df.dropna()
                        st.success("✅ Dropped rows with missing values")
                    elif missing_strategy == "Fill with mean/mode":
                        for col in df.columns:
                            if df[col].dtype.kind in 'biufc':  # numeric
                                df[col].fillna(df[col].mean(), inplace=True)
                            else:
                                df[col].fillna(df[col].mode()[0], inplace=True)
                        st.success("✅ Filled missing values with mean/mode")
                    
                    # Handle duplicates
                    st.subheader("Handle Duplicate Rows")
                    if st.checkbox("Remove duplicate rows"):
                        original_count = len(df)
                        df = df.drop_duplicates()
                        st.success(f"✅ Removed {original_count - len(df)} duplicate rows")
                
                # Download cleaned data
                st.header("📥 Download Options")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Generate Cleaned Dataset"):
                        cleaned_data = io.BytesIO()
                        df.to_csv(cleaned_data, index=False)
                        cleaned_data.seek(0)
                        st.download_button(
                            label="Download Cleaned Data (CSV)",
                            data=cleaned_data,
                            file_name=f"cleaned_{uploaded_file.name}",
                            mime="text/csv"
                        )
                
                with col2:
                    if st.button("Proceed to Data Consultation ➡️"):
                        st.session_state.cleaned_df = df
                        st.session_state.page = "Data Consultation"
                        st.rerun()
                
            except Exception as e:
                st.error(f"Error analyzing dataset: {str(e)}")
    
    elif current_page == "Data Consultation":
        st.title("🤝 Data Consultation")
        
        if st.session_state.cleaned_df is not None:
            # Create an instance of DataConsultation
            consultation = DataConsultation()
            consultation.display_consultation()  # Call the display method
        else:
            st.warning("Please complete the Data Quality Check first!")
            if st.button("⬅️ Go to Data Quality Check"):
                st.session_state.page = "Data Quality Check"
                st.rerun()
    
    elif current_page == "Value Analysis":  # Value Analysis page
        st.title("💎 Dataset Value Analysis")
        
        if st.session_state.cleaned_df is not None:
            df = st.session_state.cleaned_df
            
            try:
                # Save the dataframe temporarily
                temp_path = Path("temp_upload")
                temp_path.mkdir(exist_ok=True)
                file_path = temp_path / "temp_analysis.csv"
                df.to_csv(file_path, index=False)
                
                # Analyze the dataset
                with st.spinner("Analyzing your dataset..."):
                    analyzer = DatasetAnalyzer()
                    report = analyzer.analyze_dataset(str(file_path))
                
                if report:
                    # Mark valuation as complete
                    st.session_state.valuation_complete = True
                    
                    # Display analysis results
                    st.success("Analysis complete! 🎉")
                    
                    # Display key metrics
                    display_metrics(report)
                    st.markdown("---")
                    display_dataset_stats(report)
                    display_pricing_tiers(report)
                    
                    with st.expander("📘 Valuation Methodology"):
                        for line in report["Valuation Methodology"]["Overview"]:
                            st.write(line)
                    
                    # Add PDF download section
                    st.markdown("---")
                    st.subheader("📄 Download Comprehensive Report")
                    
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        if st.button("📥 Generate & Download PDF Report", type="primary", use_container_width=True):
                            with st.spinner("Generating comprehensive PDF report..."):
                                try:
                                    # Collect all analysis results
                                    all_results = ReportCollector.collect_all_results(df, str(file_path))
                                    
                                    # Generate PDF report
                                    pdf_generator = PDFReportGenerator()
                                    pdf_bytes = pdf_generator.generate_report(
                                        data_quality_results=all_results.get('data_quality'),
                                        consultation_results=all_results.get('consultation'),
                                        valuation_results=all_results.get('valuation'),
                                        dataset_info=all_results.get('dataset_info')
                                    )
                                    
                                    # Create download button
                                    st.download_button(
                                        label="📥 Download PDF Report",
                                        data=pdf_bytes,
                                        file_name=f"dataset_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                                        mime="application/pdf",
                                        type="primary",
                                        use_container_width=True
                                    )
                                    
                                    st.success("✅ PDF report generated successfully! Click the download button above to save it.")
                                    
                                except Exception as e:
                                    st.error(f"Error generating PDF report: {str(e)}")
                                    st.write("Please ensure all analysis steps are completed before generating the report.")
                
                # Cleanup
                os.remove(file_path)
                
            except Exception as e:
                st.error(f"Error analyzing dataset: {str(e)}")
        
        else:
            st.warning("Please complete the Data Quality Check first!")
            if st.button("⬅️ Go to Data Quality Check"):
                st.session_state.page = "Data Quality Check"
                st.rerun()

if __name__ == "__main__":
    main() 