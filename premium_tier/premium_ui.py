import streamlit as st
import importlib
from premium_tier import matchmaker

# Force reload to ensure latest code is used
importlib.reload(matchmaker)

def render_page():
    st.header("👑 Enterprise Data Matchmaker")
    st.markdown("Upload your Base dataset and Target dataset to begin the reconciliation and merge process.")
    st.markdown("---")
    
    # Step 1: Data Input Workflow
    st.subheader("📥 1. Data Sources Input")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("📊 **Base Data (Left Table)**")
        base_file = st.file_uploader("Upload Base Data (CSV/Excel)", type=["csv", "xlsx"], key="base_file")
        
    with col2:
        st.warning("📈 **Target Data (Right Table)**")
        target_file = st.file_uploader("Upload Target Data (CSV/Excel)", type=["csv", "xlsx"], key="target_file")
        
    # Check if both files are uploaded
    if base_file is not None and target_file is not None:
        st.success("Both datasets loaded successfully! Initializing Similarity Engine...")
        
        # Safety check: Ensure function exists
        if hasattr(matchmaker, 'initialize_similarity_engine'):
            # Trigger the Matchmaker Engine (Steps 2 & 3)
            matchmaker.initialize_similarity_engine(base_file, target_file)
        else:
            st.error("Critical Error: Matchmaker engine function not found. Please restart the application.")