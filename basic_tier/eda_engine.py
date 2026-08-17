import streamlit as st
import pandas as pd

def run_eda(df):
    """Runs automated Exploratory Data Analysis on the uploaded DataFrame."""
    st.markdown("---")
    st.header("📊 Automated Exploratory Data Analysis (EDA)")

    # 1. Missing Values Analysis
    st.subheader("1. Missing Values Check")
    missing_data = df.isnull().sum()
    missing_data = missing_data[missing_data > 0] # Filter only columns that have missing values

    if not missing_data.empty:
        st.warning("We found some missing values in your dataset:")
        st.dataframe(missing_data.to_frame(name="Missing Count"))
    else:
        st.success("Great! No missing values found in the dataset.")

    col1, col2 = st.columns(2)
    
    # 2. Data Types
    with col1:
        st.subheader("2. Column Data Types")
        st.dataframe(df.dtypes.astype(str).to_frame(name="Data Type"), width="stretch")

    # 3. Statistical Summary
    with col2:
        st.subheader("3. Statistical Summary")
        # Generates summary stats (mean, min, max, etc.) for numerical columns
        st.dataframe(df.describe().fillna(""), width="stretch")
# Now adding the proper result in one word
st.header ("🟢 Basic Tier: Automated EDA & Reporting")
