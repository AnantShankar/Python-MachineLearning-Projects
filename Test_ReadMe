🧪 Application & Anomaly Detection Tests

This folder contains automated test files used to validate the functionality of the main application and weather anomaly analysis modules. The tests ensure that core logic such as temperature calculations, anomaly detection, and streak identification works correctly under normal and edge-case scenarios.

📂 Test Files Overview
1️⃣ Test_app.py

This file tests the App.py module, which is responsible for the main application logic (such as data flow, integration, and user-facing processing).
It verifies that the app behaves correctly when provided with valid weather data and that outputs are generated without errors.

2️⃣ Test_weather_anomalies.py

This file tests the WeatherAnomalies.py module.
It focuses on:

Mean temperature calculation

Heat wave and cold snap detection

Handling of constant temperatures

Detection of heat and cold streaks

Edge cases such as very small datasets

⚙️ Requirements

Before running the tests, ensure the following are installed:

pip install pandas numpy pytest


Make sure all files (App.py, WeatherAnomalies.py, weather_utils.py, and the test files) are in the same project or correctly linked via imports.

▶️ How to Run the Tests
🔹 Option 1: Running Tests in PyCharm (Recommended)

Open the project folder in PyCharm

Set the correct Python interpreter

Install missing packages if prompted

Locate the test file:

Test_app.py or

Test_weather_anomalies.py

Right-click the file

Select Run pytest in Test_app or Run pytest in Test_weather_anomalies

PyCharm will show a detailed test report indicating pass/fail status.

🔹 Option 2: Running Tests via Terminal / Command Line

Navigate to the project directory and run:

pytest


To run individual test files:

pytest Test_app.py
pytest Test_weather_anomalies.py

✅ Expected Results

All test cases should pass successfully

Failures (if any) will highlight logic or data issues

Confirms that both the application and anomaly detection logic are working as intended

📌 Notes

Tests are written using pytest for clarity and maintainability

Baseline data is included to ensure statistical calculations behave correctly

These tests support reliable development and future code changes
