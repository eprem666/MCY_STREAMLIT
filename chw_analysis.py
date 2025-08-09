import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os  # added to check file existence

# Configure page settings
st.set_page_config(
    page_title="CHW Data Average Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f0f0;
    }
    .header {
        color: #003366;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    .stButton>button {
        background-color: #003366 !important;
        color: white !important;
        border-radius: 5px;
        padding: 8px 16px;
    }
    .stTextInput>div>div>input {
        background-color: #ffffcc !important;
    }
    .result-box {
        background-color: white;
        padding: 15px;
        border-radius: 5px;
        border: 1px solid #ddd;
        margin-top: 20px;
        color: black;
    }
    </style>
    """, unsafe_allow_html=True)

# Load data function with caching
@st.cache_data
def load_data():
    # Use relative path to CSV inside repo
    file_path = 'East_Final.csv'  # <-- Make sure this CSV is in your repo root folder
    if not os.path.exists(file_path):
        st.error(f"File not found: {file_path}. Please add the CSV file to your repo.")
        return pd.DataFrame()
    try:
        df = pd.read_csv(file_path)
        # Ensure proper datetime columns if needed
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Load the data
df = load_data()

# Check if data loaded successfully
if df.empty:
    st.error("No data loaded. Please check the file path or CSV content.")
    st.stop()

# Create sidebar filters
with st.sidebar:
    st.markdown("### Filters")
    
    # Get unique values for filters
    years = sorted(df['Year'].unique()) if 'Year' in df.columns else []
    months = sorted(df['Month'].unique()) if 'Month' in df.columns else []
    days = sorted(df['Day'].unique()) if 'Day' in df.columns else []
    times = sorted(df['Time'].unique()) if 'Time' in df.columns else []
    buildings = sorted(df['Building'].unique()) if 'Building' in df.columns else []
    
    # Create filter widgets with yellow background
    selected_year = st.selectbox("Year", [""] + years, key="year")
    selected_month = st.selectbox("Month", [""] + months, key="month")
    selected_day = st.selectbox("Day", [""] + days, key="day")
    selected_time = st.selectbox("Time", [""] + times, key="time")
    selected_building = st.selectbox("Building", [""] + buildings, key="building")

# Main content area
st.markdown('<div class="header">CHW Data Average Analysis</div>', unsafe_allow_html=True)

# Create button row
col1, col2, col3 = st.columns(3)
with col1:
    search_btn = st.button("Search", key="search")
with col2:
    reset_btn = st.button("Reset", key="reset")
with col3:
    average_btn = st.button("Average", key="average")

# Function to filter data based on selections
def filter_data():
    filtered = df.copy()
    if selected_year and selected_year != "":
        filtered = filtered[filtered['Year'] == selected_year]
    if selected_month and selected_month != "":
        filtered = filtered[filtered['Month'] == selected_month]
    if selected_day and selected_day != "":
        filtered = filtered[filtered['Day'] == selected_day]
    if selected_time and selected_time != "":
        filtered = filtered[filtered['Time'] == selected_time]
    if selected_building and selected_building != "":
        filtered = filtered[filtered['Building'] == selected_building]
    return filtered

# Function to calculate averages
def calculate_averages(filtered_df):
    # Select columns F to U (adjust column names as needed)
    columns_to_avg = filtered_df.columns[5:20]  # Assuming F is column 5 and U is column 20
    return filtered_df[columns_to_avg].mean()

# Handle button clicks
if search_btn:
    filtered_data = filter_data()
    if not filtered_data.empty:
        # Select columns F to U (adjust as needed)
        result_data = filtered_data.iloc[:, 5:20]
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.dataframe(result_data)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("No data found with the selected filters")

elif reset_btn:
    # Reset all selections by rerunning the app
    st.experimental_rerun()

elif average_btn:
    filtered_data = filter_data()
    if not filtered_data.empty:
        averages = calculate_averages(filtered_data)
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.write("### Averages for Selected Filters")
        st.write(averages)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("No data found to calculate averages")

# Display data summary
with st.expander("Data Summary"):
    st.write(f"Total records: {len(df)}")
    st.write("Columns available:", df.columns.tolist())
    st.write("First 5 rows:", df.head())