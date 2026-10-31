import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Bike Sharing Data Analytics Dashboard",
    page_icon="🚲",
    layout="wide"
)

# Jalur absolut file main_data.csv
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SCRIPT_DIR, "main_data.csv")

# Memuat data
@st.cache_data
def load_data():
    if not os.path.exists(DATA_PATH):
        st.error(f"File 'main_data.csv' tidak ditemukan di lokasi: {DATA_PATH}")
        return None
    df = pd.read_csv(DATA_PATH)
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

df = load_data()

if df is None:
    st.stop()

# Header
st.title("🚲 Bike Sharing Data Analytics Dashboard")
st.markdown("Dashboard interaktif untuk menganalisis tren penyewaan sepeda harian berdasarkan kondisi cuaca dan pola jam sibuk.")

# Sidebar Filter
st.sidebar.header("Filter Data")
min_date = df['dteday'].min().date()
max_date = df['dteday'].max().date()

# Penanganan filter tanggal yang lebih aman
date_range = st.sidebar.date_input(
    label="Rentang Waktu",
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

if isinstance(date_range, list) or isinstance(date_range, tuple):
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = date_range[0]
        end_date = max_date
else:
    start_date = date_range
    end_date = max_date

# Filter Dataframe berdasarkan rentang tanggal
main_df = df[(df['dteday'].dt.date >= start_date) & (df['dteday'].dt.date <= end_date)]

# Ringkasan Metrik (KPIs)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Penyewaan", value=f"{main_df['cnt'].sum():,}")
with col2:
    st.metric("Total Pengguna Registered", value=f"{main_df['registered'].sum():,}")
with col3:
    st.metric("Total Pengguna Casual", value=f"{main_df['casual'].sum():,}")

st.markdown("---")

# Visualisasi 1: Jawaban Pertanyaan 1 (Pengaruh Cuaca)
st.subheader("📊 Visualisasi 1: Rata-rata Penyewaan Sepeda Berdasarkan Cuaca")
weather_avg = main_df.groupby('weather_label')['cnt'].mean().reset_index().sort_values(by='cnt', ascending=False)

fig1, ax1 = plt.subplots(figsize=(8, 4))
# Menambahkan hue dan legend=False untuk mencegah deprecation warning
sns.barplot(
    data=weather_avg, 
    x='weather_label', 
    y='cnt', 
    hue='weather_label', 
    palette='Blues_d', 
    legend=False, 
    ax=ax1
)
ax1.set_xlabel("Kondisi Cuaca")
ax1.set_ylabel("Rata-rata Penyewaan")
for p in ax1.patches:
    ax1.annotate(
        f'{p.get_height():.0f}',
        (p.get_x() + p.get_width() / 2., p.get_height()),
        ha='center', va='bottom', fontsize=9, xytext=(0, 3), textcoords='offset points'
    )
st.pyplot(fig1)

# Visualisasi 2: Jawaban Pertanyaan 2 (Pola per Jam pada Hari Kerja)
st.subheader("⏰ Visualisasi 2: Pola Rata-Rata Penyewaan per Jam pada Hari Kerja")
workingday_df = main_df[main_df['workingday'] == 1].groupby('hr')[['casual', 'registered']].mean().reset_index()

fig2, ax2 = plt.subplots(figsize=(10, 4.5))
ax2.plot(workingday_df['hr'], workingday_df['registered'], label='Registered Users', color='#1f77b4', marker='o', linewidth=2)
ax2.plot(workingday_df['hr'], workingday_df['casual'], label='Casual Users', color='#ff7f0e', marker='s', linewidth=2)
ax2.set_xlabel("Jam (00:00 - 23:00)")
ax2.set_ylabel("Rata-rata Penyewaan")
ax2.set_xticks(range(0, 24))
ax2.legend(title='Tipe Pengguna')
ax2.grid(True, linestyle='--', alpha=0.5)
st.pyplot(fig2)