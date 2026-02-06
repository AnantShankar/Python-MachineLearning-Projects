import pandas as pd
from weather_utils import prepare_weather_data  # adjust import if needed


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
# Test Case 2: Heat Wave Detection
# -------------------------------
def test_heat_wave_detection():
    dates = pd.date_range("2024-06-01", periods=30)
    temps = [22] * 27 + [40, 41, 42]

    df = pd.DataFrame({
        "DATE": dates,
        "MIN_TEMP_CELSIUS": temps,
        "MAX_TEMP_CELSIUS": [t + 2 for t in temps]
    })

    df = prepare_weather_data(df)
    assert (df["anomaly"] == "Heat Wave").any()


# -------------------------------
# Test Case 3: Cold Snap Detection
# -------------------------------
def test_cold_snap_detection():
    dates = pd.date_range("2024-01-01", periods=30)
    temps = [5] * 27 + [-15, -16, -17]

    df = pd.DataFrame({
        "DATE": dates,
        "MIN_TEMP_CELSIUS": temps,
        "MAX_TEMP_CELSIUS": [t + 1 for t in temps]
    })

    df = prepare_weather_data(df)
    assert (df["anomaly"] == "Cold Snap").any()


# -------------------------------
# Test Case 4: Constant Temperature
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
# Test Case 5: Heat Streak
# -------------------------------
def test_heat_streak_detection():
    df = pd.DataFrame({
        "DATE": pd.date_range("2024-07-01", periods=5),
        "MIN_TEMP_CELSIUS": [32, 33, 34, 20, 21],
        "MAX_TEMP_CELSIUS": [36, 37, 38, 25, 26]
    })

    df = prepare_weather_data(df)
    assert df["HOT_STREAK"].max() >= 3


# -------------------------------
# Test Case 6: Small Dataset
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
    assert "HOT_STREAK" in df.columns
    assert "COLD_STREAK" in df.columns
