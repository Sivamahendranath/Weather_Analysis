# Weather_Analysis
Weather Analytics
🌦️ India Weather Analytics Dashboard
A modern, interactive, and insightful weather analytics web app built with Streamlit, offering real-time weather updates, 5-day forecasts, air quality analysis, and historical weather trend visualizations across major Indian cities.

🚀 Features
Real-Time Weather Data: Get up-to-date temperature, humidity, pressure, dew point, wind speed, sunrise/sunset times, and descriptive weather info.

5-Day Forecast: View detailed daily and hourly weather forecasts using Plotly visualizations.

Air Quality Index (AQI): Analyze PM2.5, PM10, O₃, and NO₂ values along with health impact recommendations.

Weather Alerts: Get notified when your custom thresholds for temperature, humidity, or wind are crossed.

Location Support: Search by city/state, save frequently checked locations, and handle common misspellings.

Historical Trends: Simulated visualizations of average/min/max temperature and rainfall trends over the past year.

Seasonal Context: Dynamically adjusts styling and recommendations based on India's seasonal cycles.

Auto-Refresh & Live Indicators: Enable auto-updates of data at your preferred interval.

Customizable UI: Dark/day modes, seasonal badges, and a modern CSS-enhanced theme.

🛠️ Tech Stack
Frontend: Streamlit, HTML/CSS (custom theming)

Backend: Python

Visualization: Plotly, Matplotlib, Seaborn

API: OpenWeatherMap (for weather, forecast, air quality)

Environment Management: dotenv, Streamlit secrets

📦 Installation
Clone the repository:

bash
Copy
Edit
git clone https://github.com/your-username/india-weather-dashboard.git
cd india-weather-dashboard
Create a virtual environment (optional but recommended):

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Set up environment variables:

Create a .env file or use Streamlit's secrets to store your API key:

ini
Copy
Edit
Weather_Api=your_openweathermap_api_key
▶️ Running the App
bash
Copy
Edit
streamlit run graph.txt
Note: Although the file is named graph.txt, it's a valid Python script. You can rename it to app.py for clarity.

🌍 Supported Locations
All Indian states and 20+ major cities (e.g., Mumbai, Delhi, Bangalore, Chennai, Hyderabad).

Smart typo correction and fallback search logic for improved usability.

📊 Visuals & Components
Weather Cards: Clean layouts with large temperature icons and real-time data.

Forecast Charts: Line plots for temperature and bar charts for rain predictions.

AQI Meter: Color-coded air quality strip with current marker and explanations.

Historical Trends: Temperature and rainfall line charts with seasonal anomalies.

🧠 Smart Features
Live Indicators: See live update status with animated indicators.

Auto-Refresh Controls: Toggleable auto-refresh with interval settings.

Custom Alerts: Set personalized thresholds for weather alerts.

📁 Project Structure (recommended)
bash
Copy
Edit
.
├── app.py                  # (originally graph.txt)
├── .env                   # contains Weather_Api
├── requirements.txt
└── README.md
📃 License
MIT License — feel free to fork, modify, and use!
