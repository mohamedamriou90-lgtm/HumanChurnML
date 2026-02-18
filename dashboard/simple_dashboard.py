"""
Simple Streamlit Dashboard for HumanChurnML
Run with: streamlit run simple_dashboard.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
sys.path.append('..')
from src.production.churn_engine import ChurnEngine

# Page config
st.set_page_config(
    page_title="HumanChurnML",
    page_icon="🚀",
    layout="wide"
)

# Title
st.title("🚀 HumanChurnML - Customer Intelligence Dashboard")
st.markdown("Predict churn for ANY business using universal human patterns")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    company = st.text_input("Company Name", "MyBusiness")
    industry = st.selectbox(
        "Industry",
        ["ecommerce", "gaming", "saas", "music", "other"]
    )
    
    st.markdown("---")
    st.header("📤 Upload Data")
    
    customers_file = st.file_uploader("Customers CSV", type=['csv'])
    activities_file = st.file_uploader("Activities CSV", type=['csv'])
    
    analyze_btn = st.button("🚀 Run Analysis", type="primary")

# Initialize engine
engine = ChurnEngine(company_name=company, industry=industry)

# Main content
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Customers", "190K+", "from discovery")
with col2:
    st.metric("Universal Multiplier", "3.9x", "⬆️ 0.2")
with col3:
    st.metric("Industries", "2 → 5", "+3")
with col4:
    st.metric("Confidence", "95%", "⬆️")

# Two columns for charts
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📈 The Universal Pattern")
    
    # Data from our discovery
    levels = ['Tried Once', 'Casual', 'Regular', 'Loyal', 'Super Customer']
    gaming_values = [2, 18, 47, 70, 84]
    ecommerce_values = [161, 246, 389, 512, 630]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=levels, y=gaming_values,
        mode='lines+markers',
        name='Gaming (Retention %)',
        line=dict(color='#4CAF50', width=3)
    ))
    fig.add_trace(go.Scatter(
        x=levels, y=ecommerce_values,
        mode='lines+markers',
        name='E-commerce (Avg Spend R$)',
        line=dict(color='#FF5722', width=3)
    ))
    
    fig.update_layout(
        title="More Engagement = More Value",
        xaxis_title="Engagement Level",
        yaxis_title="Value",
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("🎯 How It Works")
    
    st.markdown("""
    1. **Upload your customer data** (any format)
    2. **Our engine detects patterns** using universal human behavior
    3. **Get predictions**:
       - Who will churn
       - What to do
       - How much they're worth
    4. **Export to your CRM** and take action!
    """)
    
    st.info("""
    💡 **Key Insight**
    
    Super Customers are worth **3.9x more** than one-time buyers.
    
    This pattern holds across industries!
    """)

# Analysis section
if analyze_btn and customers_file and activities_file:
    st.markdown("---")
    st.subheader("📊 Analysis Results")
    
    # Load data
    customers = pd.read_csv(customers_file)
    activities = pd.read_csv(activities_file)
    
    with st.spinner("Analyzing customer behavior..."):
        # Run analysis
        results = engine.analyze_customers(customers, activities)
        stats = engine.get_summary_stats(results)
    
    # Show metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Customers", stats['total_customers'])
    with m2:
        st.metric("At Risk", stats['at_risk_customers'], 
                  f"{stats['at_risk_customers']/stats['total_customers']*100:.0f}%")
    with m3:
        st.metric("Urgent", stats['urgent_customers'])
    with m4:
        st.metric("Potential Savings", f"R${stats['potential_savings']:,.0f}")
    
    # Show at-risk customers
    st.subheader("⚠️ At-Risk Customers - Take Action Now!")
    
    at_risk = results[results['churn_risk'] > 70].sort_values('churn_risk', ascending=False)
    
    if len(at_risk) > 0:
        st.dataframe(
            at_risk[['customer_id', 'engagement_level', 'churn_risk', 'recommended_action']],
            use_container_width=True
        )
        
        # Export button
        csv = at_risk.to_csv(index=False)
        st.download_button(
            "📥 Download At-Risk List",
            csv,
            "at_risk_customers.csv",
            "text/csv"
        )
    else:
        st.success("No customers at high risk! 🎉")
    
    # Export all results
    st.markdown("---")
    st.subheader("💾 Export All Results")
    
    all_results_csv = results.to_csv(index=False)
    st.download_button(
        "📥 Download Complete Analysis",
        all_results_csv,
        "churn_analysis.csv",
        "text/csv"
    )

# Footer
st.markdown("---")
st.markdown("🚀 **HumanChurnML** - Universal Customer Intelligence")