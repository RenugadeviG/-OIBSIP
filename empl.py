import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Unemployment Analysis Dashboard",
    layout="wide"
)

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

# ---------------- LOAD DATASETS ----------------
df1 = pd.read_csv(r"C:\Users\LENOVO\Downloads\archive (31)\Unemployment in India.csv")
df2 = pd.read_csv(r"C:\Users\LENOVO\Downloads\archive (31)\Unemployment_Rate_upto_11_2020.csv")

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

# =========================================================
# BAR CHART 1: REGION-WISE UNEMPLOYMENT
# =========================================================
st.markdown("## 🏙 Region-wise Average Unemployment Rate")

region_avg = (
    filtered_df.groupby("Region")["Estimated Unemployment Rate (%)"]
    .mean()
    .sort_values(ascending=False)
)

fig1, ax1 = plt.subplots(figsize=(12,5))
ax1.bar(region_avg.index, region_avg.values, color="#38bdf8")
ax1.set_xticklabels(region_avg.index, rotation=90)
ax1.set_ylabel("Unemployment Rate (%)")
st.pyplot(fig1)

# =========================================================
# BAR CHART 2: COVID VS PRE-COVID COMPARISON
# =========================================================
st.markdown("## 🦠 Pre-Covid vs Covid Unemployment Comparison")

pre_covid = filtered_df[filtered_df["Date"] < "2020-03-01"]["Estimated Unemployment Rate (%)"].mean()
covid = filtered_df[filtered_df["Date"] >= "2020-03-01"]["Estimated Unemployment Rate (%)"].mean()

fig2, ax2 = plt.subplots(figsize=(6,5))
ax2.bar(
    ["Pre-Covid", "Covid Period"],
    [pre_covid, covid],
    color=["#60a5fa", "#2563eb"]
)
ax2.set_ylabel("Average Unemployment Rate (%)")
st.pyplot(fig2)

# =========================================================
# GROUPED BAR CHART: UNEMPLOYMENT vs LABOUR PARTICIPATION
# =========================================================
st.markdown("## 📊 Unemployment vs Labour Participation Comparison")

comparison_df = filtered_df.groupby("Region").mean(numeric_only=True)
x = range(len(comparison_df.index))

fig3, ax3 = plt.subplots(figsize=(14,6))

ax3.bar(
    x,
    comparison_df["Estimated Unemployment Rate (%)"],
    width=0.4,
    label="Unemployment Rate",
    color="#1d4ed8"
)

ax3.bar(
    [i + 0.4 for i in x],
    comparison_df["Estimated Labour Participation Rate (%)"],
    width=0.4,
    label="Labour Participation Rate",
    color="#7dd3fc"
)

ax3.set_xticks([i + 0.2 for i in x])
ax3.set_xticklabels(comparison_df.index, rotation=90)
ax3.set_ylabel("Percentage (%)")
ax3.legend()

st.pyplot(fig3)

# =========================================================
# BAR CHART 3: REGION-WISE LABOUR PARTICIPATION
# =========================================================
st.markdown("## 👥 Region-wise Labour Participation Rate")

labour_avg = (
    filtered_df.groupby("Region")["Estimated Labour Participation Rate (%)"]
    .mean()
    .sort_values(ascending=False)
)

fig4, ax4 = plt.subplots(figsize=(12,5))
ax4.bar(labour_avg.index, labour_avg.values, color="#93c5fd")
ax4.set_xticklabels(labour_avg.index, rotation=90)
ax4.set_ylabel("Labour Participation Rate (%)")
st.pyplot(fig4)

# ---------------- DATA PREVIEW ----------------
st.markdown("## 📄 Dataset Preview")
st.dataframe(filtered_df.head(20))

# ---------------- FOOTER ----------------
st.success("✅ Dashboard Loaded Successfully")
