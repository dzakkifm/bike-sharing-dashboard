import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Bike Sharing Analysis Dashboard",
    page_icon="🚲",
    layout="wide"
)

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

day_df = load_data()

# Header Dashboard
st.title("🚲 Bike Sharing Data Analytics Dashboard")
st.markdown("Dashboard interaktif untuk menganalisis tren penyewaan sepeda harian berdasarkan kondisi cuaca dan musim.")

# Sidebar Filter
st.sidebar.header("Filter Data")
min_date = day_df['dteday'].min()
max_date = day_df['dteday'].max()

start_date, end_date = st.sidebar.date_input(
    label="Rentang Waktu",
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

# Filter Dataframe
main_df = day_df[(day_df['dteday'] >= pd.to_datetime(start_date)) & (day_df['dteday'] <= pd.to_datetime(end_date))]

# Key Performance Indicators (KPIs)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Penyewaan", value=f"{main_df['cnt'].sum():,}")
with col2:
    st.metric("Rata-rata Penyewaan Harian", value=f"{int(main_df['cnt'].mean()):,}")
with col3:
    st.metric("Total Pengguna Registered", value=f"{main_df['registered'].sum():,}")

st.markdown("---")

# Visualisasi 1: Dampak Cuaca
st.subheader("📊 Rata-rata Penyewaan Sepeda Berdasarkan Cuaca")
weather_avg = main_df.groupby('weather_label')['cnt'].mean().reset_index()

fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(data=weather_avg, x='weather_label', y='cnt', palette='Blues_d', ax=ax)
ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Rata-rata Penyewaan")
st.pyplot(fig)

# Visualisasi 2: Perbandingan Pengguna
st.subheader("👥 Komposisi Pengguna (Casual vs Registered)")
casual_total = main_df['casual'].sum()
registered_total = main_df['registered'].sum()

fig2, ax2 = plt.subplots(figsize=(6, 4))
ax2.pie([casual_total, registered_total], labels=['Casual', 'Registered'], autopct='%1.1f%%', colors=['#ff9999','#66b3ff'], startangle=90)
st.pyplot(fig2)