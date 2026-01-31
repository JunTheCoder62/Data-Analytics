import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


# 1. KONFIGURASI & MAPPING
st.set_page_config(layout="wide")

mapping_month = {
    1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
    7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'
}

mapping_season = {
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
}

mapping_weather = {
    1: 'Clear, Few clouds, Partly cloudy, Partly cloudy',
    2: 'Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist',
    3: 'Light Snow',
    4: 'Heavy Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds'
}

mapping_year = {0: 2011, 1: 2012}

month_order = list(mapping_month.values())

# 2. FUNGSI LOAD & CLEANING
@st.cache_data
def load_and_clean_data():
    day_df = pd.read_csv(
        'https://raw.githubusercontent.com/JunTheCoder62/Data-Analytics/refs/heads/main/Data/day.csv'
    )
    hour_df = pd.read_csv(
        'https://raw.githubusercontent.com/JunTheCoder62/Data-Analytics/refs/heads/main/Data/hour.csv'
    )

    # ---- Clean day_df ----
    day_df.rename(
        columns={
            'yr': 'year',
            'mnth': 'month',
            'weathersit': 'weather_condition',
            'hum': 'humidity',
            'cnt': 'count'
        },
        inplace=True
    )

    day_df['month'] = day_df['month'].map(mapping_month)
    day_df['season'] = day_df['season'].map(mapping_season)
    day_df['weather_condition'] = day_df['weather_condition'].map(mapping_weather)
    day_df['year'] = day_df['year'].map(mapping_year)

    day_df.drop(['windspeed', 'weekday'], axis=1, inplace=True)

    day_df['year'] = day_df['year'].astype('object')
    day_df['month'] = pd.Categorical(day_df['month'], categories=month_order, ordered=True)
    day_df['season'] = day_df['season'].astype('category')
    day_df['weather_condition'] = day_df['weather_condition'].astype('category')
    day_df['workingday'] = day_df['workingday'].astype('category')
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])

    # ---- Clean hour_df ----
    hour_df.rename(
        columns={
            'yr': 'year',
            'mnth': 'month',
            'weathersit': 'weather_condition',
            'hum': 'humidity',
            'cnt': 'count'
        },
        inplace=True
    )

    hour_df.drop(['windspeed', 'weekday'], axis=1, inplace=True)

    hour_df['season'] = hour_df['season'].map(mapping_season)
    hour_df['year'] = hour_df['year'].map(mapping_year)
    hour_df['weather_condition'] = hour_df['weather_condition'].map(mapping_weather)
    hour_df['month'] = hour_df['month'].map(mapping_month)
    hour_df['month'] = pd.Categorical(hour_df['month'], categories=month_order, ordered=True)

    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

    return day_df, hour_df

# 3. LOAD DATA
day_df, hour_df = load_and_clean_data()

# 5. SIDEBAR (DATE RANGE)
min_date = day_df['dteday'].min().date()
max_date = day_df['dteday'].max().date()

with st.sidebar:
    st.image("https://github.com/AxelTheAxcelian/Data-by-data-Streamlit/raw/main/download.jpg")
    date_range = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date)
    )

if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_date, end_date = date_range
elif isinstance(date_range, (list, tuple)) and len(date_range) == 1:
    start_date, end_date = date_range[0], date_range[0]
else:
    start_date, end_date = min_date, max_date

start_ts = pd.to_datetime(start_date)
end_ts = pd.to_datetime(end_date)

day_f = day_df[(day_df['dteday'] >= start_ts) & (day_df['dteday'] <= end_ts)]
hour_f = hour_df[(hour_df['dteday'] >= start_ts) & (hour_df['dteday'] <= end_ts)]

# 4. DASHBOARD
st.title('Bike Sharing Data Analysis Dashboard')

# 4.1 Jumlah Pengguna Rental Sepeda dalam 2 Tahun
st.header('1. Jumlah Pengguna Rental Sepeda dalam 2 Tahun')

plot_month_day_df = day_f['month'].astype(str)
plot_years_day_df = day_f['year'].astype(str)
day_f = day_f.copy()
day_f['month_year'] = plot_month_day_df + ' ' + plot_years_day_df

day_df_total_sum = (
    day_f
    .groupby(['year', 'month'], sort=False)['count']
    .sum()
    .reset_index()
    .sort_values(['year', 'month'])
)

day_df_total_sum['month_year'] = (
    day_df_total_sum['month'].astype(str) + ' ' + day_df_total_sum['year'].astype(str)
)

fig1, ax1 = plt.subplots(figsize=(15, 6))
sns.lineplot(
    data=day_df_total_sum,
    x='month_year',
    y='count',
    marker='o',
    ax=ax1
)
ax1.set_title("Jumlah Rental Sepeda per Bulan dalam 2 Tahun Terakhir")
ax1.set_xlabel(None)
ax1.set_ylabel("Jumlah Total Rental")
ax1.tick_params(axis='x', rotation=45)
st.pyplot(fig1)

st.subheader("Ringkasan Data Rental Sepeda per Bulan")
st.dataframe(day_df_total_sum[['month_year', 'count']])

st.subheader("Total Rental Sepeda per Tahun")
st.dataframe(
    day_f.groupby(by='year')['count'].sum().reset_index()
)

st.write(
    "**Insight:** Dalam tabel dan grafik di atas, terlihat bahwa penyewaan sepeda "
    "tertinggi terjadi pada bulan September 2012, setelah peningkatan signifikan dari "
    "Februari 2012. Penurunan jumlah rental konsisten terjadi pada bulan Oktober hingga "
    "Desember, diikuti oleh peningkatan kembali pada Februari tahun berikutnya."
)

st.markdown('---')

# 4.2 Durasi Rental Sepeda selama Hari Kerja dan Hari Libur per Jam
st.header('2. Durasi Rental Sepeda selama Hari Kerja dan Hari Libur per Jam')

hour_df_workingday = hour_f[hour_f['workingday'] == 1]
hour_df_holiday = hour_f[hour_f['holiday'] == 1]

plot_hr_workingday_df = (
    hour_df_workingday
    .groupby('hr')['count']
    .sum()
    .reset_index()
)
plot_hr_holiday_df = (
    hour_df_holiday
    .groupby('hr')['count']
    .sum()
    .reset_index()
)

fig2, ax2 = plt.subplots(figsize=(12, 6))
ax2.plot(
    plot_hr_workingday_df['hr'],
    plot_hr_workingday_df['count'],
    marker='o',
    label='Hari Kerja'
)
ax2.plot(
    plot_hr_holiday_df['hr'],
    plot_hr_holiday_df['count'],
    marker='o',
    label='Hari Libur'
)
ax2.set_title('Jumlah Rental Sepeda per Jam pada Hari Kerja dan Hari Libur')
ax2.set_xlabel('Jam')
ax2.set_ylabel('Jumlah Rental Sepeda')
ax2.legend()
ax2.grid(True)
st.pyplot(fig2)

st.subheader("Ringkasan Rental Sepeda per Jam (Hari Kerja)")
st.dataframe(
    hour_df_workingday
    .groupby('hr')['count']
    .agg(['sum', 'mean', 'min', 'max'])
    .sort_values(by='sum', ascending=False)
)

st.subheader("Ringkasan Rental Sepeda per Jam (Hari Libur)")
st.dataframe(
    hour_df_holiday
    .groupby('hr')['count']
    .agg(['sum', 'mean', 'min', 'max'])
    .sort_values(by='sum', ascending=False)
)

st.write(
    "**Insight:** Grafik menunjukkan dua puncak penggunaan sepeda: pagi hari "
    "(sekitar pukul 07.00 - 08.00) dan sore hari (pukul 17.00 - 18.00). "
    "Pada hari libur, jumlah penggunaan cenderung lebih tinggi dibandingkan "
    "hari kerja pada jam-jam puncak tersebut, menunjukkan pola penggunaan "
    "untuk rekreasi atau aktivitas non-komuter."
)
