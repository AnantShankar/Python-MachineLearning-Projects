import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# -------------------------------
# Load data
# -------------------------------
df = pd.read_csv("Local_Weather.csv", encoding="latin1")
df["DATE"] = pd.to_datetime(df["DATE"], dayfirst=True)
df["MEAN_TEMP"] = (df["MIN_TEMP_CELSIUS"] + df["MAX_TEMP_CELSIUS"]) / 2
df["month"] = df["DATE"].dt.month
df["year"] = df["DATE"].dt.year

# Monthly normals
monthly_normals = df.groupby("month")["MEAN TEMPERATURE(C)"].agg(mean="mean", std="std").reset_index()
df = df.merge(monthly_normals, on="month", how="left")

# Z-score
df["z_score"] = (df["MEAN_TEMP"] - df["mean"]) / df["std"]

# Anomalies
df["anomaly"] = "Normal"
df.loc[df["z_score"] > 2, "anomaly"] = "Heat Wave"
df.loc[df["z_score"] < -2, "anomaly"] = "Cold Snap"

# Streaks
df["HOT_DAY"] = (df["MEAN_TEMP"] > 30).fillna(False)
df["COLD_DAY"] = (df["MEAN_TEMP"] < 0).fillna(False)
df["HOT_STREAK"] = df.groupby((df["HOT_DAY"] != df["HOT_DAY"].shift()).cumsum())["HOT_DAY"].transform(lambda x: x.cumsum() if x.iloc[0] else 0)
df["COLD_STREAK"] = df.groupby((df["COLD_DAY"] != df["COLD_DAY"].shift()).cumsum())["COLD_DAY"].transform(lambda x: x.cumsum() if x.iloc[0] else 0)

# -------------------------------
# Streamlit app
# -------------------------------
st.title("Local Weather Anomalies Explorer 🌡️")

# Sidebar filters
st.sidebar.header("Filter by Date")
selected_years = st.sidebar.multiselect("Select Year(s)", options=sorted(df["year"].unique()), default=sorted(df["year"].unique()))
selected_month = st.sidebar.selectbox("Select Month (Optional)", options=[0] + list(range(1,13)), index=0)
selected_day = st.sidebar.number_input("Select Day (Optional)", min_value=0, max_value=31, value=0)

# Apply filters
filtered_df = df[df["year"].isin(selected_years)]
if selected_month != 0:
    filtered_df = filtered_df[filtered_df["month"] == selected_month]
if selected_day != 0:
    filtered_df = filtered_df[filtered_df["DATE"].dt.day == selected_day]

st.subheader(f"Showing {len(filtered_df)} record(s) for selected date(s)")

# Show anomalies
st.dataframe(filtered_df[["DATE","MEAN_TEMP","anomaly","HOT_STREAK","COLD_STREAK"]])

# -------------------------------
# Visualization: Scatter of anomalies
# -------------------------------
st.subheader("Anomalies Visualization")
fig, ax = plt.subplots(figsize=(12,5))
ax.plot(filtered_df["DATE"], filtered_df["MEAN_TEMP"], label="Mean Temp", color="gray")
ax.scatter(filtered_df[filtered_df["anomaly"]=="Heat Wave"]["DATE"], filtered_df[filtered_df["anomaly"]=="Heat Wave"]["MEAN_TEMP"], color="red", label="Heat Waves")
ax.scatter(filtered_df[filtered_df["anomaly"]=="Cold Snap"]["DATE"], filtered_df[filtered_df["anomaly"]=="Cold Snap"]["MEAN_TEMP"], color="blue", label="Cold Snaps")
ax.legend()
ax.set_xlabel("Date")
ax.set_ylabel("Temperature (°C)")
ax.set_title("Temperature Anomalies")
st.pyplot(fig)

# -------------------------------
# Heatmap for Z-scores if multiple years selected
# -------------------------------
if len(selected_years) > 1:
    st.subheader("Daily Temperature Z-Scores Heatmap")
    pivot_table = filtered_df.pivot_table(index="DATE", columns="year", values="z_score")
    fig2, ax2 = plt.subplots(figsize=(14,6))
    sns.heatmap(pivot_table, cmap="coolwarm", center=0, ax=ax2)
    st.pyplot(fig2)
