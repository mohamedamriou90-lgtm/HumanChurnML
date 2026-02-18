import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Page config
st.set_page_config(page_title="HumanChurnML", page_icon="🚀")

# Title
st.title("🚀 HumanChurnML - Customer Intelligence")
st.write("If you can see this, Streamlit is working!")

# Simple data
data = pd.DataFrame({
    'Customer Type': ['Tried Once', 'Casual', 'Regular', 'Loyal', 'Super Customer'],
    'Value': [161, 246, 389, 512, 630]
})

# Simple chart
fig = px.bar(data, x='Customer Type', y='Value', title='The Universal Pattern')
st.plotly_chart(fig)

# Success message
st.success("✅ Dashboard loaded successfully!")
