import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------
# Load data
# -------------------------------
df = pd.read_csv("Local_Weather.csv",encoding="latin1")
print(df.columns)
df["DATE"] = pd.to_datetime(df["DATE"],dayfirst=True)

# Calculate mean daily temperature
df["MEAN_TEMP"] = (df["MIN_TEMP_CELSIUS"] + df["MAX_TEMP_CELSIUS"]) / 2

# Extract month and year
df["month"] = df["DATE"].dt.month
df["year"] = df["DATE"].dt.year

# -------------------------------
# Calculate monthly normals
# -------------------------------
monthly_normals = df.groupby("month")["MEAN TEMPERATURE(C)"].agg(
    mean="mean",
    std="std"
).reset_index()

# Merge monthly normals back to daily data
df = df.merge(monthly_normals, on="month", how="left")

# -------------------------------
# Z-score calculation
# -------------------------------
df["z_score"] = (df["MEAN_TEMP"] - df["mean"]) / df["std"]

# -------------------------------
# Detect anomalies
# -------------------------------
df["anomaly"] = "Normal"
df.loc[df["z_score"] > 2, "anomaly"] = "Heat Wave"
df.loc[df["z_score"] < -2, "anomaly"] = "Cold Snap"

# -------------------------------
# Summary counts
# -------------------------------
heat_waves = df[df["anomaly"] == "Heat Wave"]
cold_snaps = df[df["anomaly"] == "Cold Snap"]

print("Total heat waves detected:", len(heat_waves))
print("Total cold snaps detected:", len(cold_snaps))

# -------------------------------
# Record-breaking days
# -------------------------------
record_hot = df[df["MEAN_TEMP"] == df["MEAN_TEMP"].max()]
record_cold = df[df["MEAN_TEMP"] == df["MEAN_TEMP"].min()]

print("Record hottest day:", record_hot["DATE"].values[0])
print("Record coldest day:", record_cold["DATE"].values[0])

# -------------------------------
# Record-breaking days
# -------------------------------
record_hot = df[df["MEAN_TEMP"] == df["MEAN_TEMP"].max()]
record_cold = df[df["MEAN_TEMP"] == df["MEAN_TEMP"].min()]

print("Record hottest day:", record_hot["DATE"].values[0])
print("Record coldest day:", record_cold["DATE"].values[0])

# -------------------------------
# Consecutive heat and cold detection (fixed)
# -------------------------------

# Make boolean columns and handle NaN
df["HOT_DAY"] = (df["MEAN_TEMP"] > 30).fillna(False)
df["COLD_DAY"] = (df["MEAN_TEMP"] < 0).fillna(False)

# Calculate streaks safely
df["HOT_STREAK"] = df.groupby((df["HOT_DAY"] != df["HOT_DAY"].shift()).cumsum())["HOT_DAY"].transform(lambda x: x.cumsum() if x.iloc[0] else 0)
df["COLD_STREAK"] = df.groupby((df["COLD_DAY"] != df["COLD_DAY"].shift()).cumsum())["COLD_DAY"].transform(lambda x: x.cumsum() if x.iloc[0] else 0)

# Filter unusual streaks
unusual_heat_streaks = df[df["HOT_STREAK"] >= 3]
unusual_cold_streaks = df[df["COLD_STREAK"] >= 3]

print("Unusual heat streaks:")
print(unusual_heat_streaks[["DATE", "MEAN_TEMP"]])
print("Unusual cold streaks:")
print(unusual_cold_streaks[["DATE", "MEAN_TEMP"]])

# -------------------------------
# Visualization 1
# -------------------------------
plt.figure(figsize=(12,5))
plt.plot(df["DATE"], df["MEAN_TEMP"], label="Mean Temp", color="gray")
plt.scatter(heat_waves["DATE"], heat_waves["MEAN_TEMP"], color="red", label="Heat Waves")
plt.scatter(cold_snaps["DATE"], cold_snaps["MEAN_TEMP"], color="blue", label="Cold Snaps")
plt.scatter(unusual_heat_streaks["DATE"], unusual_heat_streaks["MEAN_TEMP"], color="orange", label="Heat Streaks")
plt.legend()
plt.title("Temperature Anomalies Over Time")
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.show()

# -------------------------------
# Visualization 2: Daily temperatures with anomalies
# -------------------------------
plt.figure(figsize=(14,6))
plt.plot(df["DATE"], df["MEAN_TEMP"], label="Mean Temp", color="gray")
plt.scatter(heat_waves["DATE"], heat_waves["MEAN_TEMP"], color="red", label="Heat Waves")
plt.scatter(cold_snaps["DATE"], cold_snaps["MEAN_TEMP"], color="blue", label="Cold Snaps")
plt.scatter(unusual_heat_streaks["DATE"], unusual_heat_streaks["MEAN_TEMP"], color="orange", label="Heat Streaks")
plt.scatter(unusual_cold_streaks["DATE"], unusual_cold_streaks["MEAN_TEMP"], color="cyan", label="Cold Streaks")
plt.legend()
plt.title("Daily Mean Temperatures and Anomalies")
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.show()

# -------------------------------
# Visualization 3: Monthly average temperature
# -------------------------------
monthly_avg = df.groupby("month")["MEAN_TEMP"].mean()
plt.figure(figsize=(10,5))
plt.bar(monthly_avg.index, monthly_avg.values, color="skyblue")
plt.title("Average Monthly Temperature")
plt.xlabel("Month")
plt.ylabel("Temperature (°C)")
plt.xticks(range(1,13))
plt.show()

# -------------------------------
# Visualization 4: Monthly anomalies count
# -------------------------------
monthly_anomalies = df.groupby(["month","anomaly"]).size().unstack(fill_value=0)
monthly_anomalies.plot(kind="bar", stacked=True, figsize=(10,5), color=["gray","red","blue"])
plt.title("Monthly Anomalies Count")
plt.xlabel("Month")
plt.ylabel("Number of Days")
plt.show()

# -------------------------------
# Visualization 5: Distribution of streak lengths
# -------------------------------
plt.figure(figsize=(10,5))
plt.hist(df["HOT_STREAK"][df["HOT_STREAK"]>0], bins=range(1, df["HOT_STREAK"].max()+2), color="orange", alpha=0.7, label="Heat Streaks")
plt.hist(df["COLD_STREAK"][df["COLD_STREAK"]>0], bins=range(1, df["COLD_STREAK"].max()+2), color="cyan", alpha=0.7, label="Cold Streaks")
plt.title("Distribution of Extreme Temperature Streaks")
plt.xlabel("Streak Length (days)")
plt.ylabel("Frequency")
plt.legend()
plt.show()

# -------------------------------
# Visualization 6: Monthly temperature boxplot
# -------------------------------
plt.figure(figsize=(12,6))
df.boxplot(column="MEAN_TEMP", by="month", grid=False)
plt.title("Monthly Temperature Distribution")
plt.suptitle("")
plt.xlabel("Month")
plt.ylabel("Mean Temperature (°C)")
plt.show()

# -------------------------------
# Visualization 7: Heatmap of Z-scores
# -------------------------------
# Pivot table for heatmap (dates vs year)
pivot_table = df.pivot_table(index="DATE", columns="year", values="z_score")
plt.figure(figsize=(14,6))
sns.heatmap(pivot_table, cmap="coolwarm", center=0)
plt.title("Daily Temperature Z-Scores Heatmap")
plt.show()
