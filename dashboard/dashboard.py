import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Bike Sharing Dashboard 2012", layout="wide")

# 1. Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

main_df = load_data()

# 2. Sidebar - Date Filter Default ke Tahun 2012
st.sidebar.header("Filter Data")

min_date = main_df['dteday'].min().date()
max_date = main_df['dteday'].max().date()

# Default awal: Tahun 2012
default_start = pd.to_datetime("2012-01-01").date()
default_end = pd.to_datetime("2012-12-31").date()

start_date, end_date = st.sidebar.date_input(
    label='Rentang Waktu',
    min_value=min_date,
    max_value=max_date,
    value=[default_start, default_end]
)

# Filter Dataframe berdasarkan Input Sidebar
filtered_df = main_df[(main_df['dteday'].dt.date >= start_date) & 
                      (main_df['dteday'].dt.date <= end_date)]

# Pesan Notifikasi Konsistensi Filter
if start_date.year != 2012 or end_date.year != 2012:
    st.info("ℹ️ **Catatan:** Anda sedang melihat rentang tanggal di luar cakupan utama pertanyaan bisnis (Tahun 2012). Tampilan ini berfungsi sebagai eksplorasi tambahan.")

# Main Title
st.title("🚲 Dashboard Analisis Penyewaan Sepeda (2012)")

# Metric Cards
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Penyewaan", value=f"{filtered_df['cnt'].sum():,}")
with col2:
    st.metric("Penyewaan Casual", value=f"{filtered_df['casual'].sum():,}")
with col3:
    st.metric("Penyewaan Registered", value=f"{filtered_df['registered'].sum():,}")

st.divider()

# --- VISUALISASI 1: Pengaruh Cuaca ---
st.subheader("1. Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca")

weather_df = filtered_df.groupby('weather_label')['cnt'].mean().reset_index()

fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(
    data=weather_df,
    x='weather_label',
    y='cnt',
    hue='weather_label',
    palette='Blues_d',
    ax=ax,
    legend=False
)
ax.set_title("Rata-rata Penyewaan per Kondisi Cuaca", fontsize=12)
ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Rata-rata Penyewaan")

for p in ax.patches:
    ax.annotate(f'{p.get_height():.0f}',
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='bottom', fontsize=10, xytext=(0, 3), textcoords='offset points')

st.pyplot(fig)

st.divider()

# --- VISUALISASI 2: Pola Per Jam Hari Kerja ---
st.subheader("2. Pola Penyewaan per Jam pada Hari Kerja (Casual vs Registered)")

# Filter Khusus Hari Kerja (workingday == 1)
working_df = filtered_df[filtered_df['workingday'] == 1]

if not working_df.empty:
    hourly_pattern = working_df.groupby('hr')[['casual', 'registered']].mean().reset_index()
    
    # Menentukan Jam Puncak (Peak Hours)
    peak_reg_hr = hourly_pattern.loc[hourly_pattern['registered'].idxmax(), 'hr']
    peak_reg_val = hourly_pattern['registered'].max()
    
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.plot(hourly_pattern['hr'], hourly_pattern['casual'], marker='o', label='Casual', color='orange')
    ax2.plot(hourly_pattern['hr'], hourly_pattern['registered'], marker='o', label='Registered', color='blue')
    
    # Highlight Jam Puncak
    ax2.axvline(x=peak_reg_hr, color='red', linestyle='--', alpha=0.7, label=f'Jam Puncak ({int(peak_reg_hr)}:00)')
    
    ax2.set_title("Rata-rata Penyewaan per Jam (Hari Kerja)", fontsize=12)
    ax2.set_xlabel("Jam (0-23)")
    ax2.set_ylabel("Rata-rata Penyewaan")
    ax2.set_xticks(range(0, 24))
    ax2.grid(True, linestyle='--', alpha=0.5)
    ax2.legend()
    
    st.pyplot(fig2)
    
    # Info Highlight
    st.success(f"📌 **Insight Jam Puncak:** Pada hari kerja, tingkat penyewaan pengguna **Registered** mencapai puncaknya pada **pukul {int(peak_reg_hr)}:00 WIB** dengan rata-rata **{int(peak_reg_val)} unit/jam**.")
else:
    st.warning("Tidak ada data hari kerja pada rentang tanggal yang dipilih.")