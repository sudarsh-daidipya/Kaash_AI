import streamlit as st
from premium_tier import matchmaker # Importing our new matchmaker logic
from premium_tier import ai_integration # Importing AI integration module

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
        
        # Create main tabs for Matchmaker and AI Analysis
        main_tab1, main_tab2 = st.tabs(["🔗 Data Matchmaker", "🤖 AI-Powered Analysis"])
        
        with main_tab1:
            # Trigger the Matchmaker Engine (Steps 2 & 3)
            matchmaker.initialize_similarity_engine(base_file, target_file)
        
        with main_tab2:
            # Load dataframes for AI analysis
            df_base = matchmaker.load_dataframe(base_file)
            df_target = matchmaker.load_dataframe(target_file)
            
            if df_base is not None and df_target is not None:
                st.markdown("### 🧠 AI Analysis on Your Datasets")
                
                # Let user choose which dataset to analyze
                dataset_choice = st.radio(
                    "Select Dataset for AI Analysis:",
                    ["Base Data Only", "Target Data Only", "Combined Preview"],
                    horizontal=True
                )
                
                if dataset_choice == "Base Data Only":
                    df_to_analyze = df_base
                    st.caption("Analyzing Base Dataset")
                elif dataset_choice == "Target Data Only":
                    df_to_analyze = df_target
                    st.caption("Analyzing Target Dataset")
                else:
                    # Show combined preview info
                    st.info(f"📊 **Base:** {df_base.shape[0]} rows × {df_base.shape[1]} cols | **Target:** {df_target.shape[0]} rows × {df_target.shape[1]} cols")
                    df_to_analyze = df_base  # Default to base for analysis
                
                # Render AI Analysis Section
                ai_integration.render_ai_analysis_tab(df_to_analyze)
            else:
                st.error("Failed to load datasets for AI analysis.")
    else:
        st.info("👆 Please upload both Base and Target datasets to proceed.")