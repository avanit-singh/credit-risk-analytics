import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. Page Configuration
st.set_page_config(page_title="Credit Risk Executive Dashboard", layout="wide")
st.title("🏦 Retail Credit Risk & ECL Dashboard")
st.markdown("### IND-AS 109 Portfolio Provisioning & Risk Segmentation")

# 2. Load Data
@st.cache_data
def load_data():
    # Assumes app is run from the root directory of the repository
    file_path = os.path.join('data', 'processed', 'portfolio_with_ecl.csv')
    return pd.read_csv(file_path)

try:
    df = load_data()
except FileNotFoundError:
    st.error("Data not found. Please ensure 'portfolio_with_ecl.csv' exists in the data/processed/ folder.")
    st.stop()

# 3. Sidebar - Interactive Policy Filters
st.sidebar.header("Policy Simulation Filters")
st.sidebar.markdown("Adjust parameters to simulate portfolio risk.")

min_cibil = st.sidebar.slider("Minimum CIBIL Score", min_value=300, max_value=900, value=650, step=10)
max_dti = st.sidebar.slider("Maximum DTI Ratio", min_value=0.1, max_value=1.0, value=0.55, step=0.05)

# Filter the dataset based on sidebar inputs
filtered_df = df[(df['cibil_score'] >= min_cibil) & (df['dti_ratio'] <= max_dti)]

# 4. Top-Line KPIs
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

total_exposure = filtered_df['EAD'].sum()
total_ecl = filtered_df['ECL_Amount'].sum()
avg_pd = filtered_df['PD'].mean() * 100
default_rate = (filtered_df['default_flag'].sum() / len(filtered_df)) * 100

col1.metric("Total Exposure (EAD)", f"₹{total_exposure / 10000000:.2f} Cr")
col2.metric("Total Provision (ECL)", f"₹{total_ecl / 10000000:.2f} Cr")
col3.metric("Average PD", f"{avg_pd:.2f}%")
col4.metric("90+ DPD (NPA %)", f"{default_rate:.2f}%")

st.markdown("---")

# 5. Visualizations
col_chart1, col_chart2 = st.columns(2)

# Chart 1: ECL by Risk Tier
# 5. Visualizations
col_chart1, col_chart2 = st.columns(2)

# Chart 1: ECL by Risk Tier
with col_chart1:
    st.subheader("Expected Credit Loss by Risk Tier")
    ecl_by_tier = filtered_df.groupby('risk_tier')['ECL_Amount'].sum().reset_index()
    
    # Changed text_auto to True to fix Pylance error
    fig1 = px.bar(ecl_by_tier, x='risk_tier', y='ECL_Amount', 
                  color='risk_tier', text_auto=True,
                  labels={'ECL_Amount': 'Total ECL (INR)', 'risk_tier': 'Risk Tier'},
                  color_discrete_sequence=px.colors.sequential.Blues_r)
    
    # Applied the .2s formatting via update_traces
    fig1.update_traces(texttemplate='%{y:.2s}', textposition='outside')
    fig1.update_layout(showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Default Rate by Loan Product
with col_chart2:
    st.subheader("90+ DPD Rate by Product")
    dr_by_product = filtered_df.groupby('loan_product').agg(
        default_rate=('default_flag', lambda x: x.mean() * 100)
    ).reset_index()
    
    # Changed text_auto to True to fix Pylance error
    fig2 = px.bar(dr_by_product, x='loan_product', y='default_rate',
                  color='loan_product', text_auto=True,
                  labels={'default_rate': 'Default Rate (%)', 'loan_product': 'Product'},
                  color_discrete_sequence=px.colors.sequential.Reds_r)
    
    # Applied the .2f formatting via update_traces
    fig2.update_traces(texttemplate='%{y:.2f}', textposition='outside')
    fig2.update_layout(showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)
