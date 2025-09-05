import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from typing import Dict, List
import json
import os
import re
from .visualization import show_results

class DataConsultation:
    def __init__(self):
        # Hardcoded questions and weights
        self.tabs = {
            "Data Uniqueness": [
                { "question": "Is the data unique within the industry?: Consider how exclusive your data is in the market.", "description": "1-3: The data is commonly available and easily replicated by competitors. <br>4-6: The data is moderately unique and somewhat difficult to replicate. <br>7-10: The data is highly unique or proprietary, offering significant exclusivity." },
                { "question": "How rare is this data compared to competitors?: Evaluate its uniqueness against industry standards.", "description": "1-3: The data is general and could apply to any similar organization. <br>4-6: The data is somewhat tailored but could still be applied by competitors. <br>7-10: The data is highly specific to your organization and difficult to use elsewhere without adaptation." },
                # ... (add all other questions from Data Uniqueness)
            ],
            "Data Volume": [
                { "question": "What is the size of the dataset?: Measure the total amount of data collected.", "description": "1-3: The dataset is small (e.g., a few thousand records or a few megabytes). <br>4-6: The dataset is moderate in size (e.g., hundreds of thousands of records or gigabytes). <br>7-10: The dataset is very large (e.g., millions of records or terabytes)." },
                # ... (add all other questions from Data Volume)
            ],
            "Data Accuracy and Quality": [
                { "question": "How accurate is the data?: Evaluate the correctness and precision of the data.", "description": "1-3: The data contains significant errors or inaccuracies. <br>4-6: The data is moderately accurate with some errors. <br>7-10: The data is highly accurate with minimal errors." },
                # ... (add all other questions from Data Accuracy and Quality)
            ],
            "Data Access and Usability": [
                { "question": "How easily can the data be accessed?: Consider technical barriers.", "description": "1-3: The data is difficult to access with significant barriers. <br>4-6: The data is moderately accessible. <br>7-10: The data is easily accessible with minimal barriers." },
                # ... (add all other questions from Data Access and Usability)
            ],
            "Data Governance": [
                { "question": "How well is the data managed?: Consider data governance practices.", "description": "1-3: Poor data management practices. <br>4-6: Basic data management in place. <br>7-10: Strong data governance framework exists." },
                # ... (add all other questions from Data Governance)
            ],
            "Data Security": [
                { "question": "How secure is the data?: Evaluate security measures.", "description": "1-3: Basic or minimal security measures. <br>4-6: Standard security measures in place. <br>7-10: Advanced security measures implemented." },
                # ... (add all other questions from Data Security)
            ],
            "Data Monetization Potential": [
                { "question": "Can the data be monetized?: Assess commercial potential.", "description": "1-3: Limited monetization potential. <br>4-6: Some monetization opportunities exist. <br>7-10: High monetization potential." },
                # ... (add all other questions from Data Monetization Potential)
            ],
            "Strategic Value of Data": [
                { "question": "How aligned is the data with business objectives?: Check strategic fit.", "description": "1-3: Poor alignment with objectives. <br>4-6: Moderate alignment exists. <br>7-10: Strong alignment with objectives." },
                # ... (add all other questions from Strategic Value of Data)
            ]
        }

        self.weights = {
            "Data Uniqueness": 0.20,
            "Data Volume": 0.10,
            "Data Accuracy and Quality": 0.15,
            "Data Access and Usability": 0.15,
            "Data Governance": 0.10,
            "Data Security": 0.10,
            "Data Monetization Potential": 0.15,
            "Strategic Value of Data": 0.05
        }

    def display_consultation(self):
        if 'consultation_step' not in st.session_state:
            st.session_state.consultation_step = 0
            st.session_state.responses = {}
        
        # Check if we're on the results page
        if st.session_state.consultation_step >= len(self.tabs):
            self.show_results()
            return
        
        current_tab = list(self.tabs.keys())[st.session_state.consultation_step]
        questions = self.tabs[current_tab]
        
        st.header(f"📊 {current_tab}")
        
        # Display progress
        progress = st.session_state.consultation_step / len(self.tabs)
        st.progress(progress)
        
        # Display current questions
        for i, question in enumerate(questions):
            st.subheader(question["question"])
            # Display description with proper HTML line breaks
            st.markdown(question["description"], unsafe_allow_html=True)
            response = st.slider(
                "Score",
                min_value=1,
                max_value=10,
                value=5,
                key=f"q_{current_tab}_{i}"
            )
            
            if current_tab not in st.session_state.responses:
                st.session_state.responses[current_tab] = []
            
            # Store response
            while len(st.session_state.responses[current_tab]) <= i:
                st.session_state.responses[current_tab].append(0)
            st.session_state.responses[current_tab][i] = response
        
        # Navigation buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.session_state.consultation_step > 0:
                if st.button("⬅️ Previous Section"):
                    st.session_state.consultation_step -= 1
                    st.rerun()
        
        with col2:
            if st.session_state.consultation_step < len(self.tabs) - 1:
                if st.button("Next Section ➡️"):
                    # Ensure all questions in the current section are answered
                    if len(st.session_state.responses[current_tab]) == len(questions):
                        st.session_state.consultation_step += 1
                        st.rerun()
                    else:
                        st.warning("Please answer all questions in this section before proceeding.")
            else:
                if st.button("View Results 📊"):
                    st.session_state.consultation_step = len(self.tabs)  # Set to results page
                    st.rerun() 

    def show_results(self):
        """Display the consultation results"""
        show_results(st.session_state.responses, self.weights) 