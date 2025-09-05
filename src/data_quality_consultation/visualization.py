import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import Dict
from datetime import datetime

def create_radar_chart(responses: Dict, weights: Dict):
    """Create a radar chart from consultation responses"""
    categories = list(responses.keys())
    values = [np.mean(responses[cat]) for cat in categories]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Dataset Score'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )
        ),
        showlegend=True,
        title="Dataset Value Assessment"
    )
    
    return fig

def display_score_table(responses: Dict, weights: Dict):
    """Display a table of scores with weights and calculations"""
    data = []
    total_weighted_score = 0
    
    for category in responses:
        score = np.mean(responses[category])
        weight = weights[category]
        weighted_score = score * weight
        total_weighted_score += weighted_score
        
        data.append({
            'Category': category,
            'Weight': f"{weight*100:.0f}%",
            'Score': f"{score:.1f}",
            'Weighted Score': f"{weighted_score:.2f}"
        })
    
    df = pd.DataFrame(data)

    # Ensure numeric columns are of the correct type
    df['Score'] = pd.to_numeric(df['Score'], errors='coerce')
    df['Weighted Score'] = pd.to_numeric(df['Weighted Score'], errors='coerce')

    # Display total score card
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            f"""
            <div style='text-align: center; padding: 20px; background-color: #f0f2f6; border-radius: 10px;'>
                <h2 style='margin: 0;'>Total Score</h2>
                <h1 style='color: #0066cc; margin: 10px 0;'>{total_weighted_score:.1f}</h1>
                <p style='margin: 0;'>out of 10</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    return total_weighted_score

def show_results(responses, weights):
    """Display the consultation results"""
    total_score = display_score_table(responses, weights)

    # Use a single container for the entire output section
    st.header("Total Score")
    st.write(total_score)

    st.markdown("### Detailed Scores")
    
    # Create the DataFrame for detailed scores
    data = []
    for category in responses:
        score = np.mean(responses[category])
        weight = weights[category]
        weighted_score = score * weight
        
        data.append({
            'Category': category,
            'Weight': f"{weight*100:.0f}%",
            'Score': f"{score:.1f}",
            'Weighted Score': f"{weighted_score:.2f}"
        })
    
    df = pd.DataFrame(data)

    # Ensure numeric columns are of the correct type
    df['Score'] = pd.to_numeric(df['Score'], errors='coerce')
    df['Weighted Score'] = pd.to_numeric(df['Weighted Score'], errors='coerce')

    # Display the detailed score table
    st.dataframe(
        df.style
        .format({
            'Weighted Score': '{:.2f}',
            'Score': '{:.1f}'  # Ensure Score is formatted correctly
        })
        .background_gradient(subset=['Weighted Score'], cmap='Blues')
        .set_properties(**{'text-align': 'center'})
        .set_table_styles([
            {'selector': 'th', 'props': [('text-align', 'center')]},
            {'selector': 'td', 'props': [('text-align', 'center')]}
        ]),
        use_container_width=True  # Ensure full width
    )

    # Add navigation buttons with unique keys
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back to Consultation", key="back_button"):
            st.session_state.consultation_step -= 1
            st.rerun()
    
    with col2:
        if st.button("Proceed to Valuation ➡️", key="proceed_button"):
            # Clear consultation state to exit consultation context
            st.session_state.consultation_step = 0
            st.session_state.responses = {}
            st.session_state.page = "Value Analysis"
            st.session_state.consultation_complete = True
            st.success("✅ Consultation completed! Redirecting to Value Analysis...")
            # Force a rerun to ensure navigation happens
            st.rerun()
    
    # Add PDF download option for consultation results
    st.markdown("---")
    st.subheader("📄 Download Consultation Report")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📥 Download Consultation PDF", key="consultation_pdf_button"):
            with st.spinner("Generating consultation report..."):
                try:
                    from src.utils.pdf_report_generator import PDFReportGenerator
                    from src.utils.report_collector import ReportCollector
                    
                    # Get the cleaned dataframe if available
                    df = st.session_state.get('cleaned_df', pd.DataFrame())
                    
                    # Collect consultation results
                    all_results = ReportCollector.collect_all_results(df)
                    
                    # Generate PDF report
                    pdf_generator = PDFReportGenerator()
                    pdf_bytes = pdf_generator.generate_report(
                        data_quality_results=all_results.get('data_quality'),
                        consultation_results=all_results.get('consultation'),
                        valuation_results=None,  # No valuation yet
                        dataset_info=all_results.get('dataset_info')
                    )
                    
                    # Create download button
                    st.download_button(
                        label="📥 Download Consultation PDF",
                        data=pdf_bytes,
                        file_name=f"consultation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf",
                        type="secondary",
                        use_container_width=True
                    )
                    
                    st.success("✅ Consultation report generated successfully!")
                    
                except Exception as e:
                    st.error(f"Error generating consultation report: {str(e)}") 