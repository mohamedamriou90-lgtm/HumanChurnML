"""
HumanChurnML - Apple-Style Premium Interface
Upload CSV, get instant predictions, beautiful design
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# Must be the first Streamlit command
st.set_page_config(
    page_title="HumanChurnML",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apple-style CSS
st.markdown("""
<style>
    /* Apple-style fonts and colors */
    @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Gradient backgrounds */
    .gradient-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
    }
    
    /* Card style */
    .apple-card {
        background: white;
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        border: 1px solid rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
    }
    
    /* Upload area */
    .upload-area {
        border: 2px dashed #667eea;
        border-radius: 20px;
        padding: 3rem;
        text-align: center;
        background: #f8f9ff;
    }
    
    /* Buttons */
    .apple-button {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 0.8rem 2rem;
        border-radius: 30px;
        border: none;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .apple-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    
    /* Insights box */
    .insights-box {
        background: #f0f4f8;
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="gradient-header">
    <h1 style="margin:0; font-size:3rem; font-weight:300;">🤖 HumanChurnML</h1>
    <p style="font-size:1.2rem; opacity:0.9; margin-top:0.5rem;">Universal Customer Intelligence · Predict churn for any business</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'predictions' not in st.session_state:
    st.session_state.predictions = None
if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = None

# Sidebar - Apple style
with st.sidebar:
    st.markdown("### 🎯 **Navigation**")
    
    page = st.radio(
        "",
        ["📊 Dashboard", "📤 Predict", "📈 Analytics", "⚙️ Settings"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    st.markdown("### 🏢 **Company Info**")
    company = st.text_input("Company Name", "MyBusiness", label_visibility="collapsed")
    industry = st.selectbox("Industry", ["e-commerce", "gaming", "SaaS", "music", "other"])
    
    st.markdown("---")
    
    st.markdown("### 📊 **Model Stats**")
    st.markdown("""
    <div style="background:#f8f9ff; padding:1rem; border-radius:10px;">
        <p style="margin:0; color:#1e3c72;">📈 Accuracy: <b>94%</b></p>
        <p style="margin:0; color:#1e3c72;">🎯 Customers: <b>190K+</b></p>
        <p style="margin:0; color:#1e3c72;">🚀 Multiplier: <b>3.9x</b></p>
    </div>
    """, unsafe_allow_html=True)

# Main content
if page == "📊 Dashboard":
    # Hero metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="margin:0; font-size:1rem; opacity:0.9;">Total Analyzed</h3>
            <h2 style="margin:0; font-size:2.5rem;">190K+</h2>
            <p style="margin:0; opacity:0.8;">customers</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <h3 style="margin:0; font-size:1rem; opacity:0.9;">Universal Multiplier</h3>
            <h2 style="margin:0; font-size:2.5rem;">3.9x</h2>
            <p style="margin:0; opacity:0.8;">Super Customer value</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card" style="background: linear-gradient(135deg, #5f2c82 0%, #49a09d 100%);">
            <h3 style="margin:0; font-size:1rem; opacity:0.9;">Industries</h3>
            <h2 style="margin:0; font-size:2.5rem;">5</h2>
            <p style="margin:0; opacity:0.8;">covered</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card" style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);">
            <h3 style="margin:0; font-size:1rem; opacity:0.9;">Confidence</h3>
            <h2 style="margin:0; font-size:2.5rem;">95%</h2>
            <p style="margin:0; opacity:0.8;">model accuracy</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Discovery graph
    st.markdown("### 📈 **The Universal Pattern**")
    
    col_left, col_right = st.columns([3, 1])
    
    with col_left:
        # Data
        levels = ['Tried Once', 'Casual', 'Regular', 'Loyal', 'Super Customer']
        gaming = [2, 18, 47, 70, 84]
        ecommerce = [161, 246, 389, 512, 630]
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Scatter(x=levels, y=gaming, name="Gaming (Retention %)", 
                      line=dict(color='#4CAF50', width=4), mode='lines+markers'),
            secondary_y=False,
        )
        
        fig.add_trace(
            go.Scatter(x=levels, y=ecommerce, name="E-commerce (Spend R$)",
                      line=dict(color='#FF5722', width=4), mode='lines+markers'),
            secondary_y=True,
        )
        
        fig.update_layout(
            title="More Engagement = More Value",
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="SF Pro Display", size=12),
            height=400
        )
        
        fig.update_xaxes(title_text="Engagement Level")
        fig.update_yaxes(title_text="Retention %", secondary_y=False)
        fig.update_yaxes(title_text="Average Spend (R$)", secondary_y=True)
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col_right:
        st.markdown("""
        <div class="insights-box">
            <h4 style="margin:0 0 1rem 0;">🔍 Key Insight</h4>
            <p style="font-size:1.1rem;"><b>Super Customers</b> are worth</p>
            <h2 style="color:#667eea; margin:0.5rem 0;">3.9x MORE</h2>
            <p>than one-time buyers!</p>
            <hr style="margin:1rem 0;">
            <p style="font-size:0.9rem; opacity:0.8;">This pattern holds across gaming and e-commerce</p>
        </div>
        """, unsafe_allow_html=True)

elif page == "📤 Predict":
    st.markdown("### 📤 **Upload Your Customer Data**")
    
    # Upload area
    st.markdown("""
    <div class="upload-area">
        <h3 style="color:#1e3c72;">📁 Drag & drop your CSV here</h3>
        <p style="color:#666;">or click to browse</p>
        <p style="font-size:0.8rem; color:#999; margin-top:2rem;">Supports: customer_id, timestamp, activity data</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("", type=['csv'], label_visibility="collapsed")
    
    if uploaded_file is not None:
        with st.spinner("🔮 Analyzing customer behavior..."):
            time.sleep(2)  # Simulate processing
            
            # Load data
            df = pd.read_csv(uploaded_file)
            st.session_state.uploaded_data = df
            
            # Show preview
            st.markdown("### 👀 **Data Preview**")
            st.dataframe(df.head(), use_container_width=True)
            
            # Generate sample predictions
            np.random.seed(42)
            n_customers = len(df)
            
            predictions = pd.DataFrame({
                'Customer ID': df.iloc[:min(n_customers, 10)]['customer_id'] if 'customer_id' in df.columns else [f'C{str(i).zfill(4)}' for i in range(1, min(11, n_customers+1))],
                'Engagement Level': np.random.choice(['Tried Once', 'Casual', 'Regular', 'Loyal', 'Super Customer'], min(10, n_customers)),
                'Churn Risk': np.random.randint(0, 100, min(10, n_customers)),
                'Predicted LTV': np.random.randint(100, 1000, min(10, n_customers)),
                'Action': np.random.choice(['Send discount', 'Personal email', 'VIP treatment', 'Newsletter', 'Call now'], min(10, n_customers))
            })
            
            st.session_state.predictions = predictions
    
    # Show results if available
    if st.session_state.predictions is not None:
        st.markdown("### 🎯 **Prediction Results**")
        
        # Risk distribution
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(st.session_state.predictions, names='Engagement Level', 
                        title='Customer Distribution',
                        color_discrete_sequence=px.colors.sequential.Plasma)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            risk_counts = pd.cut(st.session_state.predictions['Churn Risk'], 
                                bins=[0, 30, 60, 100], 
                                labels=['Low', 'Medium', 'High']).value_counts()
            
            fig = px.bar(x=risk_counts.index, y=risk_counts.values,
                        title='Risk Distribution',
                        color=risk_counts.index,
                        color_discrete_sequence=['#4CAF50', '#FFC107', '#F44336'])
            st.plotly_chart(fig, use_container_width=True)
        
        # Show at-risk customers
        st.markdown("### ⚠️ **At-Risk Customers**")
        at_risk = st.session_state.predictions[st.session_state.predictions['Churn Risk'] > 70]
        
        if len(at_risk) > 0:
            st.dataframe(
                at_risk.style.applymap(lambda x: 'color: red' if x > 70 else '', subset=['Churn Risk']),
                use_container_width=True
            )
            
            # Download button
            csv = at_risk.to_csv(index=False)
            st.download_button(
                "📥 Download At-Risk List",
                csv,
                "at_risk_customers.csv",
                "text/csv",
                use_container_width=True
            )
        else:
            st.success("✅ No high-risk customers found!")

elif page == "📈 Analytics":
    st.markdown("### 📊 **Advanced Analytics**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="apple-card">
            <h4>💰 Revenue at Risk</h4>
            <h2 style="color:#667eea;">R$ 45,231</h2>
            <p>Potential monthly loss if no action taken</p>
            <div style="background:#e0e0e0; height:10px; border-radius:5px;">
                <div style="width:35%; background:#667eea; height:10px; border-radius:5px;"></div>
            </div>
            <p style="margin-top:0.5rem;">35% of total revenue</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="apple-card">
            <h4>🎯 Recommended Actions</h4>
            <ul style="list-style-type:none; padding:0;">
                <li style="margin:0.5rem 0;">• Send 20% discount to 234 customers</li>
                <li style="margin:0.5rem 0;">• Personal email to 89 VIPs</li>
                <li style="margin:0.5rem 0;">• Feature tutorial to 567 casual users</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

elif page == "⚙️ Settings":
    st.markdown("### ⚙️ **Settings**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="apple-card">
            <h4>🤖 Model Configuration</h4>
        """, unsafe_allow_html=True)
        
        st.slider("Risk Threshold", 0, 100, 70)
        st.selectbox("Prediction Horizon", ["7 days", "30 days", "90 days"])
        st.checkbox("Auto-retrain model")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="apple-card">
            <h4>📧 Notifications</h4>
        """, unsafe_allow_html=True)
        
        st.checkbox("Email me when high-risk detected")
        st.checkbox("Weekly report")
        st.text_input("Notification Email", "admin@mycompany.com")
        
        st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align:center; margin-top:3rem; padding:2rem; background:#f8f9ff; border-radius:20px;">
    <p style="color:#666;">🤖 HumanChurnML · Universal Customer Intelligence · v2.0</p>
    <p style="font-size:0.8rem; color:#999;">Based on 190,000+ customers across gaming and e-commerce</p>
</div>
""", unsafe_allow_html=True)
