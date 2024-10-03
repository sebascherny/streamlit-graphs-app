# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import os
from datetime import datetime

# Set up paths for timeseries data
DATA_DIR = "timeseries_data"
files = [f for f in os.listdir(DATA_DIR) if f.endswith('.json')]

# Function to load and process JSON file into a DataFrame
def load_timeseries(file_path):
    with open(file_path) as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])  # Ensure 'date' column is datetime type
    return df

# Sidebar: File selectors for two JSON files
st.sidebar.header("Select Timeseries Files")
file1 = st.sidebar.selectbox("Choose the first timeseries file:", files)
file2 = st.sidebar.selectbox("Choose the second timeseries file:", files)

# Load both selected files
df1 = load_timeseries(os.path.join(DATA_DIR, file1))
df2 = load_timeseries(os.path.join(DATA_DIR, file2))

# Date range selector
min_date = max(df1['date'].min(), df2['date'].min())
max_date = min(df1['date'].max(), df2['date'].max())
dates_pair = st.sidebar.date_input("Select date range:", [min_date, max_date])

# Plotting the data
st.title("Timeseries Data Comparison")

fig, ax = plt.subplots()
ax.set_xlabel("Date")
ax.set_ylabel("Value")
ax.set_title("Line Chart of Timeseries Data")
ax.legend()

if len(dates_pair) == 2:
    start_date, end_date = dates_pair

    # Filter both DataFrames based on selected date range
    df1_filtered = df1[(df1['date'] >= pd.to_datetime(start_date)) & (df1['date'] <= pd.to_datetime(end_date))]
    df2_filtered = df2[(df2['date'] >= pd.to_datetime(start_date)) & (df2['date'] <= pd.to_datetime(end_date))]


    ax.plot(df1_filtered['date'], df1_filtered['value'], label=file1)
    ax.plot(df2_filtered['date'], df2_filtered['value'], label=file2)


    st.pyplot(fig)
