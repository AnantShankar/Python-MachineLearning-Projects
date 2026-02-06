import pandas as pd
import numpy as np


def prepare_weather_data(df):
    df["MEAN_TEMP"] = (df["MIN_TEMP_CELSIUS"] + df["MAX_TEMP_CELSIUS"]) / 2
    df["month"] = df["DATE"].dt.month

    monthly_normals = df.groupby("month")["MEAN_TEMP"].agg(
        mean="mean",
        std="std"
    ).reset_index()

    df = df.merge(monthly_normals, on="month", how="left")
    df["z_score"] = (df["MEAN_TEMP"] - df["mean"]) / df["std"]

    df["anomaly"] = "Normal"
    df.loc[df["z_score"] > 2, "anomaly"] = "Heat Wave"
    df.loc[df["z_score"] < -2, "anomaly"] = "Cold Snap"

    df["HOT_DAY"] = (df["MEAN_TEMP"] > 30).fillna(False)
    df["COLD_DAY"] = (df["MEAN_TEMP"] < 0).fillna(False)

    df["HOT_STREAK"] = df.groupby(
        (df["HOT_DAY"] != df["HOT_DAY"].shift()).cumsum()
    )["HOT_DAY"].transform(lambda x: x.cumsum() if x.iloc[0] else 0)

    df["COLD_STREAK"] = df.groupby(
        (df["COLD_DAY"] != df["COLD_DAY"].shift()).cumsum()
    )["COLD_DAY"].transform(lambda x: x.cumsum() if x.iloc[0] else 0)

    return df


# -------------------------------
# Test Case 1: Mean Temperature
# -------------------------------
def test_mean_temperature():
    df = pd.DataFrame({
        "DATE": pd.to_datetime(["2024-01-01"]),
        "MIN_TEMP_CELSIUS": [10],
        "MAX_TEMP_CELSIUS": [20]
    })
    df = prepare_weather_data(df)
    assert df["MEAN_TEMP"].iloc[0] == 15


# -------------------------------
# Test Case 2: Heat Wave Detection (WITH BASELINE)
# -------------------------------
def test_heat_wave_detection():
    dates = pd.date_range("2024-06-01", periods=30)

    # 27 normal days + 3 extreme days
    normal = [22] * 27
    extreme = [40, 41, 42]
    temps = normal + extreme

    df = pd.DataFrame({
        "DATE": dates,
        "MIN_TEMP_CELSIUS": temps,
        "MAX_TEMP_CELSIUS": [t + 2 for t in temps]
    })

    df = prepare_weather_data(df)
    assert (df["anomaly"] == "Heat Wave").any()


# -------------------------------
# Test Case 3: Cold Snap Detection (WITH BASELINE)
# -------------------------------
def test_cold_snap_detection():
    dates = pd.date_range("2024-01-01", periods=30)

    normal = [5] * 27
    extreme = [-15, -16, -17]
    temps = normal + extreme

    df = pd.DataFrame({
        "DATE": dates,
        "MIN_TEMP_CELSIUS": temps,
        "MAX_TEMP_CELSIUS": [t + 1 for t in temps]
    })

    df = prepare_weather_data(df)
    assert (df["anomaly"] == "Cold Snap").any()


# -------------------------------
# Test Case 4: Constant Temperature (Edge Case)
# -------------------------------
def test_constant_temperature():
    df = pd.DataFrame({
        "DATE": pd.date_range("2024-03-01", periods=10),
        "MIN_TEMP_CELSIUS": [10] * 10,
        "MAX_TEMP_CELSIUS": [10] * 10
    })

    df = prepare_weather_data(df)
    assert df["anomaly"].eq("Normal").all()


# -------------------------------
# Test Case 5: Heat Streak Detection
# -------------------------------
def test_heat_streak():
    df = pd.DataFrame({
        "DATE": pd.date_range("2024-07-01", periods=5),
        "MIN_TEMP_CELSIUS": [32, 33, 34, 20, 21],
        "MAX_TEMP_CELSIUS": [36, 37, 38, 25, 26]
    })

    df = prepare_weather_data(df)
    assert df["HOT_STREAK"].max() >= 3


# -------------------------------
# Test Case 6: Small Dataset (Edge Case)
# -------------------------------
def test_small_dataset():
    df = pd.DataFrame({
        "DATE": pd.to_datetime(["2024-01-01"]),
        "MIN_TEMP_CELSIUS": [5],
        "MAX_TEMP_CELSIUS": [10]
    })

    df = prepare_weather_data(df)
    assert len(df) == 1
    assert "anomaly" in df.columns
