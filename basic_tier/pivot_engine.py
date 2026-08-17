import streamlit as st
import pandas as pd

def render_pivot_builder(df):
    st.markdown("---")
    st.header("🧮 Interactive Pivot Table Builder")
    st.markdown("Create custom pivot tables dynamically by selecting rows, columns, and values.")

    # Get column types to help users select appropriate fields
    all_columns = df.columns.tolist()
    # Only allow numeric columns for 'Values' calculation
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()

    if not numeric_columns:
        st.warning("No numeric columns found in the dataset to calculate values.")
        return

    # UI setup for Pivot Table Configuration
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        pivot_index = st.multiselect("Rows (Index):", options=all_columns, help="Select columns to group by (Rows).")
        
    with col2:
        pivot_columns = st.multiselect("Columns (Optional):", options=all_columns, help="Select columns to create pivot columns.")
        
    with col3:
        pivot_values = st.multiselect("Values:", options=numeric_columns, help="Select numeric columns to calculate.")
        
    with col4:
        agg_func = st.selectbox("Aggregation:", options=["sum", "mean", "count", "min", "max"])

    # Generate Button
    if st.button("🔄 Generate Pivot Table"):
        if not pivot_index:
            st.warning("Please select at least one column for 'Rows (Index)'.")
        elif not pivot_values:
            st.warning("Please select at least one column for 'Values'.")
        else:
            try:
                with st.spinner("Generating Pivot Table..."):
                    # Execute Pandas Pivot Table Logic
                    pivot_df = pd.pivot_table(
                        df,
                        index=pivot_index,
                        columns=pivot_columns if pivot_columns else None,
                        values=pivot_values,
                        aggfunc=agg_func
                    )
                    
                    st.success("Pivot Table generated successfully!")
                    # Using width="stretch" to avoid the warning we saw earlier
                    st.dataframe(pivot_df, width="stretch")
                    
            except Exception as e:
                st.error(f"Error generating pivot table. It might be due to incompatible data combinations. Error: {e}")