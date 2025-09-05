"""
VisioValor Data Valuation App
Main entry point for Streamlit Cloud deployment
"""

import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).parent / "src"))

# Import and run the main application
from src.frontend.app import main

if __name__ == "__main__":
    main()
