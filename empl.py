import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Unemployment Analysis Dashboard",
    layout="wide"
)

# ---------------- PATH SETUP (VERY IMPORTANT) ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CSV1_PATH = os.path.join(BASE_DIR, "Unemployment in India.csv")
CSV2_PATH = os.path.join(BASE_DIR, "Unemployment_Rate_upto_11_2020.csv")

# ---------------- LOAD DATASETS ----------------
df1 = pd.read_csv(CSV1_PATH)
df2 = pd.read_csv(CSV2_PATH)

# ---------------- LITE BLUE BACKGROUND & THEME ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #e0f2fe, #bae6fd, #7dd3fc);
    color: #0f172a;
}
section[data-testid="stSidebar"] {
    background-color: #dbeafe;
}
h1, h2, h3, h4 {
    color: #0f172a;
}
p, label {
    color: #1e293b;
}
div[data-testid="metric-container"] {
    background-color: #eff6ff;
    border-radius: 12px;
    padding: 18px;
    color: #0f172a;
    border: 1px solid #93c5fd;
}
.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("📉 Unemployment Rate Analysis Dashboard")
st.markdown("### Impact of Covid-19 on Unemployment in India")

# ---------------- DATA CLEANING ----------------
df1.columns = df1.columns.str.strip()
df2.columns = df2.columns.str.strip()

df1["Date"] = pd.to_datetime(df1["Date"])
df2["Date"] = pd.to_datetime(df2["Date"])

# ---------------- COMBINE DATA ----------------
df = pd.concat([df1, df2], axis=0)

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔍 Dashboard Filters")

region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

date_range = st.sidebar.date_input(
    "Select Date Range",
    [df["Date"].min(), df["Date"].max()]
)

# ---------------- APPLY FILTERS ----------------
filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Date"] >= pd.to_datetime(date_range[0])) &
    (df["Date"] <= pd.to_datetime(date_range[1]))
]

# ---------------- KPI METRICS ----------------
st.markdown("## 📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric(
    "📈 Average Unemployment Rate",
    f"{filtered_df['Estimated Unemployment Rate (%)'].mean():.2f}%"
)

col2.metric(
    "🔺 Highest Unemployment Rate",
    f"{filtered_df['Estimated Unemployment Rate (%)'].max():.2f}%"
)

col3.metric(
    "👥 Avg Labour Participation",
    f"{filtered_df['Estimated Labour Participation Rate (%)'].mean():.2f}%"
)

# ---------------- CHARTS ----------------
st.markdown("## 🏙 Region-wise Average Unemployment Rate")
region_avg = filtered_df.groupby("Region")["Estimated Unemployment Rate (%)"].mean().sort_values(ascending=False)

fig1, ax1 = plt.subplots(figsize=(12,5))
ax1.bar(region_avg.index, region_avg.values)
ax1.set_xticklabels(region_avg.index, rotation=90)
st.pyplot(fig1)

st.markdown("## 📄 Dataset Preview")
st.dataframe(filtered_df.head(20))

st.success("✅ Dashboard Loaded Successfully")
