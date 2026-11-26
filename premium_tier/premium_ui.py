import streamlit as st
from premium_tier import matchmaker
from premium_tier import ai_integration  # <-- Naya Import add kiya

def render_page():
    st.header("👑 Enterprise Data Matchmaker & AI Suite")
    st.markdown("Premium Features: Advanced Reconciliation & Generative AI Insights")
    st.markdown("---")
    
    # Step 1: Data Input Workflow (Global for both tabs)
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
        st.success("Both datasets loaded successfully! Initializing Engine...")
        
        # Initialize Matchmaker Data (for Tab 1)
        matchmaker.initialize_similarity_engine(base_file, target_file)
        
        # Create Tabs for different Premium Features
        tab1, tab2 = st.tabs(["🔗 Data Matchmaker", "🤖 AI-Powered Analysis"])
        
        # --- TAB 1: Existing Matchmaker Logic ---
        with tab1:
            matchmaker.render_matchmaker_ui()
            
        # --- TAB 2: New AI Integration Logic ---
        with tab2:
            ai_integration.render_ai_analysis(base_file, target_file)
            
    else:
        st.warning("⬆️ Please upload both Base and Target datasets to access Premium Tools.")
        st.info("💡 Once uploaded, you will see options for 'Data Matchmaker' and 'AI-Powered Analysis'.")