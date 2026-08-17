import streamlit as st
import pandas as pd

def load_data():
    """Handles file upload and reads it into a Pandas DataFrame."""
    st.subheader("📂 Upload Your Dataset")
    
    # Create a file uploader widget accepting only CSV and Excel files
    uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])
    
    if uploaded_file is not None:
        try:
            # Check the file extension and read the data accordingly
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            
            st.success(f"File '{uploaded_file.name}' successfully loaded!")
            return df
            
        except Exception as e:
            st.error(f"An error occurred while reading the file: {e}")
            return None
            
    return None