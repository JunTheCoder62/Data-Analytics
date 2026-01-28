import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np

st.title('Data Bike Sharing')
st.write('Nama : Juniyara Parisya Setiawan')
st.write('Email : parissajuniara@gmail.com')
st.write('ID Dicoding : juniyaraparisya')

day_df = pd.read_csv("https://raw.githubusercontent.com/AxelTheAxcelian/Data-by-data-Streamlit/main/Data/day.csv")
hour_df = pd.read_csv("https://raw.githubusercontent.com/AxelTheAxcelian/Data-by-data-Streamlit/main/Data/hour.csv")



with st.container():
    st.header("Sharing in a Year")
    
    def calculate_total_bike_usage_in_year(df):
        df['dteday'] = pd.to_datetime(df['dteday'])
        daily_rentals = df.resample('D', on='dteday')['cnt'].sum()
        return daily_rentals
    total_bike_usage_in_year = calculate_total_bike_usage_in_year(day_df)
    st.write("Total bike usage in one year:", total_bike_usage_in_year.sum())
    day_df['month'] = day_df['dteday'].dt.month
    
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.barplot(data=day_df, x='month', y='cnt', estimator=sum, palette=None)
    # plt.title('Total Bike Sharing by Month')
    ax.set_xlabel('Month')
    ax.set_ylabel('Total Bike Usage')
    st.pyplot(fig)

with st.container():
    st.header("Sharing in Working day")
    def calculate_daily_bike_usage_on_working_days(df):
        working_day_df = df[df['workingday'] == 1]
        daily_rentals = working_day_df.groupby('dteday')['cnt'].sum().reset_index()
        return daily_rentals
    daily_bike_usage_working_day = calculate_daily_bike_usage_on_working_days(day_df)
    day_counts = daily_bike_usage_working_day['dteday'].dt.day_name().value_counts()
    total_bike_usage_working_day = daily_bike_usage_working_day['cnt'].sum()
    st.write("Total bike usage on working days:", total_bike_usage_working_day)

    fig, ax = plt.subplots(figsize=(10, 7))
    sns.barplot(x=day_counts.index, y=day_counts.values, palette=None)
    ax.set_xlabel('Day of the Week')
    ax.set_ylabel('Frequency of Bike Sharing')
    ax.set_title('Bike Sharing Frequency on Working Days')
    st.pyplot(fig)

with st.sidebar:
    st.image("https://github.com/AxelTheAxcelian/Data-by-data-Streamlit/raw/main/download.jpg")
    min_date = day_df['dteday'].min()
    max_date = day_df['dteday'].max()
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
)
