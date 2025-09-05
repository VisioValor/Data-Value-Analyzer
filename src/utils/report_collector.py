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
        
        # Get the actual valuation report from session state if available
        if hasattr(st.session_state, 'valuation_report') and st.session_state.valuation_report:
            report = st.session_state.valuation_report
            
            # Extract pricing information from the actual report
            value_pred = report.get("Value Prediction", {})
            
            # Calculate estimated value from the recommended one-time purchase
            estimated_value = 0
            if "Once-off Purchase" in value_pred and "Recommended" in value_pred["Once-off Purchase"]:
                # Extract numeric value from formatted string like "$1,234.56 USD"
                price_str = value_pred["Once-off Purchase"]["Recommended"]
                try:
                    estimated_value = float(price_str.replace("$", "").replace(",", "").replace(" USD", ""))
                except:
                    estimated_value = 0
            
            # Extract quality score
            quality_score = 0
            if "Quality Score" in value_pred:
                try:
                    quality_score = float(value_pred["Quality Score"].replace("/100", ""))
                except:
                    quality_score = 0
            
            # Convert pricing tiers to the format expected by PDF generator
            pricing_tiers = {}
            if "Once-off Purchase" in value_pred:
                pricing_tiers['One-Time Purchase'] = {
                    'Conservative': value_pred["Once-off Purchase"]["Conservative"],
                    'Recommended': value_pred["Once-off Purchase"]["Recommended"],
                    'Premium': value_pred["Once-off Purchase"]["Premium"]
                }
            
            if "Monthly Subscription" in value_pred:
                pricing_tiers['Monthly Subscription'] = {
                    'Conservative': value_pred["Monthly Subscription"]["Conservative"],
                    'Recommended': value_pred["Monthly Subscription"]["Recommended"],
                    'Premium': value_pred["Monthly Subscription"]["Premium"]
                }
            
            if "Yearly Subscription" in value_pred:
                pricing_tiers['Yearly Subscription'] = {
                    'Conservative': value_pred["Yearly Subscription"]["Conservative"],
                    'Recommended': value_pred["Yearly Subscription"]["Recommended"],
                    'Premium': value_pred["Yearly Subscription"]["Premium"]
                }
            
            return {
                'estimated_value': estimated_value,
                'quality_score': quality_score,
                'pricing_tiers': pricing_tiers,
                'value_prediction': value_pred,
                'market_factors': {
                    'data_rarity': 'High' if quality_score > 80 else 'Medium' if quality_score > 60 else 'Low',
                    'market_demand': 'Strong' if quality_score > 75 else 'Moderate' if quality_score > 50 else 'Weak',
                    'competitive_advantage': 'High' if quality_score > 85 else 'Moderate' if quality_score > 65 else 'Low',
                    'commercial_applicability': 'High' if quality_score > 70 else 'Medium' if quality_score > 45 else 'Low'
                }
            }
        
        # Fallback to placeholder if no actual data available
        return {
            'estimated_value': 0,
            'quality_score': 0,
            'pricing_tiers': {},
            'market_factors': {
                'data_rarity': 'Unknown',
                'market_demand': 'Unknown',
                'competitive_advantage': 'Unknown',
                'commercial_applicability': 'Unknown'
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
