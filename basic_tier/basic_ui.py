import streamlit as st
from basic_tier import data_loader
from basic_tier import eda_engine 
from basic_tier import pivot_engine # 👈 Naya import

def render_page():
    st.header("🟢 Basic Tier: Automated EDA & Reporting")
    st.markdown("Upload your dataset below to generate an automated Exploratory Data Analysis (EDA).")
    st.markdown("---")
    
    # Call the function from data_loader.py
    df = data_loader.load_data()
    
    # If a file is uploaded and successfully read into a DataFrame
    if df is not None:
        st.markdown("---")
        
        # ==========================================
        # 🟢 CREATING HORIZONTAL TABS
        # ==========================================
        tab1, tab2, tab3 = st.tabs([
            "👀 Data Preview", 
            "📊 Automated EDA", 
            "🧮 Pivot Builder"
        ])
        
        # ------------------------------------------
        # TAB 1: Data Preview
        # ------------------------------------------
        with tab1:
            st.subheader("👀 Data Preview")
            
            # Display basic shape of the dataset
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**Total Rows:** {df.shape[0]}")
            with col2:
                st.info(f"**Total Columns:** {df.shape[1]}")
                
            # Display the first 5 rows of the dataset
            st.dataframe(df.head(), width="stretch")
            
        # ------------------------------------------
        # TAB 2: Automated EDA
        # ------------------------------------------
        with tab2:
            st.subheader("📊 Exploratory Data Analysis")
            # 1. Run the Automated EDA engine
            eda_engine.run_eda(df)
            
        # ------------------------------------------
        # TAB 3: Pivot Table Builder
        # ------------------------------------------
        with tab3:
            st.subheader("🧮 Custom Pivot Tables")
            # 2. Run the Pivot Table Builder
            pivot_engine.render_pivot_builder(df)