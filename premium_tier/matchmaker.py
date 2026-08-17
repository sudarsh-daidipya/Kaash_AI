import streamlit as st
import pandas as pd
import io
import plotly.express as px

# --- Step 1: Data Input Helpers ---
def load_data(file):
    """Loads CSV or Excel files into a DataFrame."""
    try:
        if file.name.endswith('.csv'):
            return pd.read_csv(file)
        elif file.name.endswith('.xlsx'):
            return pd.read_excel(file)
        else:
            return None
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

def load_dataframe(uploaded_file):
    """Reads the uploaded file into a Pandas DataFrame."""
    try:
        if uploaded_file.name.endswith('.csv'):
            return pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            return pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Error loading {uploaded_file.name}: {e}")
        return None

# --- Step 2: Similarity Engine ---
def analyze_schemas(base_df, target_df):
    """Analyzes schemas and returns matching, missing, and extra columns."""
    base_cols = set(base_df.columns)
    target_cols = set(target_df.columns)
    
    matching_cols = list(base_cols & target_cols)
    missing_in_target = list(base_cols - target_cols)
    extra_in_target = list(target_cols - base_cols)
    
    return matching_cols, missing_in_target, extra_in_target

# --- Step 3 & 4: Merge Logic ---
def execute_merge(base_df, target_df, join_key, join_type):
    """Executes the pandas merge operation with error handling."""
    try:
        # Ensure join keys are treated as strings to avoid dtype mismatch errors
        base_df[join_key] = base_df[join_key].astype(str)
        target_df[join_key] = target_df[join_key].astype(str)
        
        merged_df = pd.merge(base_df, target_df, on=join_key, how=join_type.lower())
        return merged_df, None
    except Exception as e:
        return None, str(e)

def get_download_buffer(df, file_type):
    """Generates a download buffer for CSV or Excel."""
    if file_type == 'csv':
        csv = df.to_csv(index=False).encode('utf-8')
        return csv
    elif file_type == 'excel':
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Merged_Data')
        return output.getvalue()

def initialize_similarity_engine(base_file, target_file):
    """Similarity Engine with Horizontal Tab Layout"""
    
    # Load DataFrames
    df_base = load_dataframe(base_file)
    df_target = load_dataframe(target_file)
    
    if df_base is not None and df_target is not None:
        
        # ==========================================
        # 🟢 CREATING HORIZONTAL TABS
        # ==========================================
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Similarity Analysis", 
            "⚙️ Merge Configuration", 
            "📈 Dashboard", 
            "📥 Export Data"
        ])
        
        # ------------------------------------------
        # TAB 1: Similarity Analysis
        # ------------------------------------------
        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                st.write("📌 **Base Data Characteristics:**")
                st.caption(f"Total Rows: {df_base.shape[0]} | Total Columns: {df_base.shape[1]}")
                
            with col2:
                st.write("📌 **Target Data Characteristics:**")
                st.caption(f"Total Rows: {df_target.shape[0]} | Total Columns: {df_target.shape[1]}")
                
            st.markdown("### 📊 Column Similarity Analysis")

            base_cols = set(df_base.columns)
            target_cols = set(df_target.columns)
            common_cols_set = base_cols.intersection(target_cols)
            missing_in_target = base_cols - target_cols
            missing_in_base = target_cols - base_cols

            if common_cols_set:
                st.success(f"✅ **Matching Columns ({len(common_cols_set)}):** {', '.join(common_cols_set)}")
            else:
                st.error("❌ **No Matching Columns:** There are no common columns between the two datasets.")

            if missing_in_target:
                st.warning(f"⚠️ **Missing in Target Data ({len(missing_in_target)}):** {', '.join(missing_in_target)}")

            if missing_in_base:
                st.info(f"ℹ️ **Extra in Target Data ({len(missing_in_base)}):** {', '.join(missing_in_base)}")

        # ------------------------------------------
        # TAB 2: Merge Configuration
        # ------------------------------------------
        with tab2:
            st.subheader("🛠️ User Configuration (Join Setup)")
            
            common_cols = list(common_cols_set)
            if common_cols:
                st.success(f"Similarity Engine detected {len(common_cols)} common column(s) for joining!")
            else:
                st.warning("No common column names detected. You may need to rename columns in your datasets.")
                
            config_col1, config_col2 = st.columns(2)
            
            with config_col1:
                join_key = st.selectbox("Select Join Key (Matching Column):", options=common_cols if common_cols else df_base.columns)
                
            with config_col2:
                join_type = st.selectbox("Select Join Type:", options=["Inner Join", "Left Join", "Right Join", "Outer Join"])
                
            if st.button("🚀 Execute Merge (Reconcile)"):
                with st.spinner("Merging datasets based on Enterprise Matchmaker Logic..."):
                    try:
                        join_mapping = {"Inner Join": "inner", "Left Join": "left", "Right Join": "right", "Outer Join": "outer"}
                        pd_join_type = join_mapping[join_type]
                        
                        merged_df = pd.merge(df_base, df_target, on=join_key, how=pd_join_type, suffixes=('_Base', '_Target'))
                        
                        st.success(f"Data successfully merged using {join_type} on key '{join_key}'!")
                        
                        st.info(f"**Merged Total Rows:** {merged_df.shape[0]} | **Merged Total Columns:** {merged_df.shape[1]}")
                        st.dataframe(merged_df.head(50), width="stretch") 
                        
                        st.session_state['merged_data'] = merged_df
                    except Exception as e:
                        st.error(f"An error occurred during the merge process: {e}")

        # ------------------------------------------
        # TAB 3: Dashboard
        # ------------------------------------------
        with tab3:
            st.subheader("📈 Reconciliation Dashboard")
            if 'merged_data' in st.session_state:
                merged_df = st.session_state['merged_data']
                col_chart1, col_chart2 = st.columns(2)
                
                total_rows = len(merged_df)
                incomplete_rows = merged_df.isnull().any(axis=1).sum()
                complete_rows = total_rows - incomplete_rows
                
                with col_chart1:
                    status_data = pd.DataFrame({'Status': ['Fully Matched', 'Has Missing Data'], 'Count': [complete_rows, incomplete_rows]})
                    fig_donut = px.pie(status_data, values='Count', names='Status', hole=0.45, title="📊 Match Completeness Overview", color='Status', color_discrete_map={'Fully Matched': '#00CC96', 'Has Missing Data': '#EF553B'})
                    fig_donut.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig_donut, use_container_width=True)
                    
                with col_chart2:
                    null_counts = merged_df.isnull().sum().reset_index()
                    null_counts.columns = ['Column Name', 'Missing Values']
                    null_counts = null_counts[null_counts['Missing Values'] > 0].sort_values(by='Missing Values', ascending=False).head(5)
                    
                    if not null_counts.empty:
                        fig_bar = px.bar(null_counts, x='Column Name', y='Missing Values', title="📉 Top Discrepancies by Column", text_auto=True, color='Missing Values', color_continuous_scale='Reds')
                        fig_bar.update_layout(xaxis_title="Columns", yaxis_title="Missing Values (Count)")
                        st.plotly_chart(fig_bar, use_container_width=True)
                    else:
                        st.success("🎉 No missing values found! 100% Data Population.")
            else:
                st.info("⚠️ Please execute the merge in the 'Merge Configuration' tab first to view the dashboard.")

        # ------------------------------------------
        # TAB 4: Export Data
        # ------------------------------------------
        with tab4:
            st.subheader("📥 Output Delivery (Export)")
            if 'merged_data' in st.session_state:
                export_df = st.session_state['merged_data']
                col_csv, col_excel = st.columns(2)
                
                csv_data = export_df.to_csv(index=False).encode('utf-8')
                with col_csv:
                    st.download_button("📄 Download as CSV", data=csv_data, file_name="Reconciled_Data.csv", mime="text/csv")
                    
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    export_df.to_excel(writer, index=False, sheet_name='Merged Data')
                    
                with col_excel:
                    st.download_button("📊 Download as Excel", data=buffer.getvalue(), file_name="Reconciled_Data.xlsx", mime="application/vnd.ms-excel")
            else:
                st.info("⚠️ Please execute the merge first to export data.")