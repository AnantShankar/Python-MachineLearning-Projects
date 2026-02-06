# Python-MachineLearning-Projects
Machine learning projects

🌡️ Local Weather Anomalies Analysis

This project analyses historical local weather data to detect temperature anomalies such as heat waves and cold snaps. It uses statistical techniques (monthly normals and Z-scores) to identify extreme events and visualise trends. The project includes both a data analysis script and an interactive Streamlit dashboard for exploration.

📂 Project Files
1️⃣ WeatherAnomalies.py (Data Analysis & Visualisation)

This script performs statistical analysis and generates multiple plots:

Calculates mean daily temperature

Detects heat waves, cold snaps, and temperature streaks

Produces time-series plots, monthly averages, boxplots, and heatmaps

2️⃣ App.py (Interactive Dashboard)

This file launches an interactive web app using Streamlit:

Filter weather data by year, month, and day

View detected anomalies and streaks

Interactive plots and heatmap visualisations

3️⃣ Local_Weather.csv

The dataset containing daily weather records used by both scripts.

⚙️ Requirements

Make sure the following Python libraries are installed:

pip install pandas numpy matplotlib seaborn streamlit

▶️ How to Run the Project
🔹 Option 1: Using PyCharm (Recommended)

Open PyCharm

Click Open and select the project folder

Ensure your Python interpreter is set (File → Settings → Python Interpreter)

Install missing packages if prompted

Run the analysis script:

Right-click WeatherAnomalies.py

Click Run

Run the Streamlit app:

Open PyCharm Terminal

Run:

streamlit run App.py


The app will open automatically in your browser

🔹 Option 2: Using Any IDE or Command Line

Navigate to the project folder

Run the analysis script:

python WeatherAnomalies.py


Run the Streamlit dashboard:

streamlit run App.py

📊 Output

Console summaries of extreme temperature events

Static visualisations for trend analysis

An interactive dashboard for exploring anomalies across dates and years
