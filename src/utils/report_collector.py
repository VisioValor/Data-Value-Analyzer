import streamlit as st
from typing import Dict, Any, Optional
import pandas as pd
from pathlib import Path

class ReportCollector:
    """Collect and organize analysis results for PDF report generation"""
    
    @staticmethod
    def collect_data_quality_results(df: pd.DataFrame) -> Dict[str, Any]:
        """Collect data quality analysis results"""
        if df is None or df.empty:
            return {}
        
        # Calculate basic quality metrics
        total_cells = df.size
        null_cells = df.isnull().sum().sum()
        completeness = 1 - (null_cells / total_cells) if total_cells > 0 else 0
        
        # Calculate accuracy (simplified - based on data types consistency)
        numeric_cols = df.select_dtypes(include=['number']).columns
        accuracy = len(numeric_cols) / len(df.columns) if len(df.columns) > 0 else 0
        
        # Calculate consistency (simplified - based on duplicate rows)
        duplicate_rows = df.duplicated().sum()
        consistency = 1 - (duplicate_rows / len(df)) if len(df) > 0 else 0
        
        # Calculate uniqueness (simplified - based on unique values)
        unique_ratio = df.nunique().sum() / total_cells if total_cells > 0 else 0
        uniqueness = min(unique_ratio, 1.0)
        
        # Calculate validity (simplified - based on non-null values in key columns)
        valid_cells = (df.notnull().sum().sum())
        validity = valid_cells / total_cells if total_cells > 0 else 0
        
        return {
            'completeness': completeness,
            'accuracy': accuracy,
            'consistency': consistency,
            'uniqueness': uniqueness,
            'validity': validity,
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'null_cells': int(null_cells),
            'duplicate_rows': int(duplicate_rows)
        }
    
    @staticmethod
    def collect_consultation_results() -> Dict[str, Any]:
        """Collect consultation results from session state"""
        if 'responses' not in st.session_state or not st.session_state.responses:
            return {}
        
        responses = st.session_state.responses
        weights = {
            "Data Uniqueness": 0.20,
            "Data Volume": 0.10,
            "Data Accuracy and Quality": 0.15,
            "Data Access and Usability": 0.15,
            "Data Governance": 0.10,
            "Data Security": 0.10,
            "Data Monetization Potential": 0.15,
            "Strategic Value of Data": 0.05
        }
        
        categories = {}
        total_weighted_score = 0
        
        for category, responses_list in responses.items():
            if responses_list and len(responses_list) > 0:
                avg_score = sum(responses_list) / len(responses_list)
                weight = weights.get(category, 0)
                weighted_score = avg_score * weight
                total_weighted_score += weighted_score
                
                categories[category] = {
                    'score': avg_score,
                    'weight': weight,
                    'weighted_score': weighted_score,
                    'responses': responses_list
                }
        
        return {
            'total_score': total_weighted_score,
            'categories': categories,
            'completion_date': st.session_state.get('consultation_complete', False)
        }
    
    @staticmethod
    def collect_valuation_results() -> Dict[str, Any]:
        """Collect valuation results from session state"""
        if 'valuation_complete' not in st.session_state or not st.session_state.valuation_complete:
            return {}
        
        # This would typically come from the actual valuation analysis
        # For now, we'll create a placeholder structure
        return {
            'estimated_value': 50000,  # This should come from actual analysis
            'quality_score': 7.5,     # This should come from actual analysis
            'pricing_tiers': {
                'Basic': {
                    'price': 10000,
                    'target_market': 'Small businesses and startups',
                    'features': 'Basic data access, standard support',
                    'value_proposition': 'Essential data insights for small-scale operations'
                },
                'Professional': {
                    'price': 25000,
                    'target_market': 'Mid-size companies',
                    'features': 'Advanced analytics, priority support, API access',
                    'value_proposition': 'Comprehensive data solutions for growing businesses'
                },
                'Enterprise': {
                    'price': 50000,
                    'target_market': 'Large enterprises',
                    'features': 'Full data suite, dedicated support, custom integration',
                    'value_proposition': 'Enterprise-grade data solutions with full customization'
                }
            },
            'market_factors': {
                'data_rarity': 'High',
                'market_demand': 'Strong',
                'competitive_advantage': 'Moderate',
                'commercial_applicability': 'High'
            }
        }
    
    @staticmethod
    def collect_dataset_info(df: pd.DataFrame, file_path: str = None) -> Dict[str, Any]:
        """Collect basic dataset information"""
        if df is None or df.empty:
            return {}
        
        file_path_obj = Path(file_path) if file_path else None
        
        return {
            'name': file_path_obj.stem if file_path_obj else 'Dataset',
            'file_type': file_path_obj.suffix[1:].upper() if file_path_obj else 'CSV',
            'rows': len(df),
            'columns': len(df.columns),
            'file_size': f"{file_path_obj.stat().st_size / 1024:.1f} KB" if file_path_obj and file_path_obj.exists() else 'Unknown',
            'column_names': list(df.columns),
            'data_types': df.dtypes.to_dict()
        }
    
    @staticmethod
    def collect_all_results(df: pd.DataFrame, file_path: str = None) -> Dict[str, Any]:
        """Collect all analysis results for PDF generation"""
        return {
            'data_quality': ReportCollector.collect_data_quality_results(df),
            'consultation': ReportCollector.collect_consultation_results(),
            'valuation': ReportCollector.collect_valuation_results(),
            'dataset_info': ReportCollector.collect_dataset_info(df, file_path)
        }
