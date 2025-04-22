import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from datetime import datetime, timedelta
import time
import json
import os
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from dotenv import load_dotenv
load_dotenv()

# Set page configuration with modern appearance
st.set_page_config(
    page_title="India Weather Analytics Dashboard",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Updated theme colors - More professional and consistent palette
COLORS = {
    "primary": "#3498db",
    "secondary": "#2c3e50",
    "accent": "#e74c3c",
    "light": "#ecf0f1",
    "dark": "#34495e",
    "success": "#2ecc71",
    "warning": "#f39c12",
    "danger": "#e74c3c",
    "info": "#3498db",
    "background": "#f5f7fa",
    "card": "#ffffff",
    "sidebar": "#2c3e50",
    "text": "#2c3e50",
    "text_light": "#7f8c8d"
}

# Custom CSS with updated theme
st.markdown(f"""
<style>
    .main {{
        background-color: {COLORS["background"]};
        color: {COLORS["text"]};
    }}
    .stApp {{
        background-color: {COLORS["background"]};
    }}
    .css-1d391kg {{
        background-color: {COLORS["sidebar"]};
    }}
    .weather-card {{
        background-color: {COLORS["card"]};
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        color: {COLORS["text"]};
    }}
    .metric-container {{
        background-color: {COLORS["card"]};
        border-radius: 12px;
        padding: 15px;
        margin: 5px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }}
    .big-temp {{
        font-size: 48px;
        font-weight: bold;
        color: {COLORS["primary"]};
    }}
    .location-header {{
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 5px;
        color: {COLORS["text"]};
    }}
    .weather-desc {{
        font-size: 18px;
        margin-bottom: 15px;
        color: {COLORS["text_light"]};
    }}
    .metric-label {{
        font-size: 14px;
        color: {COLORS["text_light"]};
        margin-bottom: 5px;
    }}
    .metric-value {{
        font-size: 22px;
        font-weight: bold;
        color: {COLORS["text"]};
    }}
    .forecast-card {{
        background-color: {COLORS["card"]};
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        margin: 5px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }}
    .tab-content {{
        padding: 20px 0;
    }}
    div[data-testid="stSidebarNav"] {{
        background-color: {COLORS["sidebar"]};
    }}
    div[data-testid="stSidebar"] {{
        background-color: {COLORS["sidebar"]};
        color: white;
    }}
    div[data-testid="stSidebar"] .sidebar-content {{
        color: white;
    }}
    div.stButton > button {{
        background-color: {COLORS["primary"]};
        color: white;
        border-radius: 8px;
        padding: 5px 15px;
        border: none;
        transition: all 0.3s ease;
    }}
    div.stButton > button:hover {{
        background-color: {COLORS["info"]};
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }}
    .stSlider > div > div {{
        background-color: {COLORS["primary"]};
    }}
    .metric-row {{
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
    }}
    .sunset-sunrise {{
        background-color: {COLORS["card"]};
        border-radius: 12px;
        padding: 15px;
        margin-top: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }}
    .air-quality-indicator {{
        display: flex;
        height: 8px;
        border-radius: 4px;
        overflow: hidden;
        margin: 10px 0;
    }}
    .air-quality-indicator div {{
        height: 100%;
    }}
    .air-quality-indicator .green {{
        background-color: #4caf50;
        flex: 1;
    }}
    .air-quality-indicator .yellow {{
        background-color: #ffeb3b;
        flex: 1;
    }}
    .air-quality-indicator .orange {{
        background-color: #ff9800;
        flex: 1;
    }}
    .air-quality-indicator .red {{
        background-color: #f44336;
        flex: 1;
    }}
    .air-quality-indicator .purple {{
        background-color: #9c27b0;
        flex: 1;
    }}
    .current-marker {{
        position: relative;
        width: 12px;
        height: 12px;
        background-color: {COLORS["primary"]};
        border-radius: 50%;
        margin-top: -15px;
        box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.3);
    }}
    .refresh-section {{
        display: flex;
        align-items: center;
        justify-content: flex-end;
        gap: 10px;
        margin-bottom: 15px;
    }}
    .refresh-btn {{
        padding: 5px 10px;
        border-radius: 5px;
        border: none;
        background-color: {COLORS["primary"]};
        color: white;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 5px;
        font-size: 14px;
    }}
    .refresh-status {{
        font-size: 12px;
        color: {COLORS["text_light"]};
    }}
    .alert-badge {{
        background-color: {COLORS["danger"]};
        color: white;
        border-radius: 50%;
        width: 22px;
        height: 22px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        margin-left: 8px;
    }}
    .sidebar-title {{
        color: white;
        padding: 20px 0 10px 0;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 20px;
    }}
    .sidebar-subtitle {{
        color: white;
        opacity: 0.8;
        font-size: 16px;
        font-weight: 600;
        margin: 20px 0 10px 0;
    }}
    .live-indicator {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 12px;
        padding: 3px 8px;
        border-radius: 20px;
        background-color: rgba(46, 204, 113, 0.15);
        color: #2ecc71;
    }}
    .live-indicator-dot {{
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background-color: #2ecc71;
        animation: pulse 1.5s infinite;
    }}
    @keyframes pulse {{
        0% {{
            transform: scale(0.95);
            box-shadow: 0 0 0 0 rgba(46, 204, 113, 0.7);
        }}
        70% {{
            transform: scale(1);
            box-shadow: 0 0 0 5px rgba(46, 204, 113, 0);
        }}
        100% {{
            transform: scale(0.95);
            box-shadow: 0 0 0 0 rgba(46, 204, 113, 0);
        }}
    }}
    .weather-icon-large {{
        width: 80px;
        height: 80px;
        object-fit: contain;
    }}
    .seasonal-tag {{
        display: inline-block;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 500;
        margin-left: 10px;
    }}
    .seasonal-tag.winter {{
        background-color: #a3dcef;
        color: #0c7fb0;
    }}
    .seasonal-tag.summer {{
        background-color: #ffcc80;
        color: #e65100;
    }}
    .seasonal-tag.monsoon {{
        background-color: #bbdefb;
        color: #1565c0;
    }}
    .seasonal-tag.post-monsoon {{
        background-color: #c8e6c9;
        color: #2e7d32;
    }}
    .day-mode {{
        background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
        color: #2c3e50;
    }}
    .night-mode {{
        background: linear-gradient(135deg, #4b6cb7 0%, #182848 100%);
        color: white;
    }}
    .header-card {{
        border-radius: 12px;
        padding: 15px 20px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
</style>
""", unsafe_allow_html=True)

api_key = os.getenv("Weather_Api")
if not api_key:
    api_key = st.secrets.get("Weather_Api", "")  # Fallback to Streamlit secrets

# Initialize session state variables
if 'user_locations' not in st.session_state:
    st.session_state.user_locations = []
if 'alert_thresholds' not in st.session_state:
    st.session_state.alert_thresholds = {'temp_max': 40, 'temp_min': 10, 'wind_speed': 15, 'humidity': 85, 'uv_index': 10}
if 'location_type' not in st.session_state:
    st.session_state.location_type = "City"
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = datetime.now()
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = False
if 'refresh_interval' not in st.session_state:
    st.session_state.refresh_interval = 15  # minutes
if 'theme_mode' not in st.session_state:
    current_hour = datetime.now().hour
    st.session_state.theme_mode = "day" if 6 <= current_hour < 18 else "night"

INDIAN_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", 
    "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", 
    "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", 
    "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", 
    "Uttarakhand", "West Bengal"
]

MAJOR_CITIES = {
    "Mumbai": {"state": "Maharashtra", "lat": 19.0760, "lon": 72.8777},
    "Delhi": {"state": "Delhi", "lat": 28.7041, "lon": 77.1025},
    "Bangalore": {"state": "Karnataka", "lat": 12.9716, "lon": 77.5946},
    "Hyderabad": {"state": "Telangana", "lat": 17.3850, "lon": 78.4867},
    "Chennai": {"state": "Tamil Nadu", "lat": 13.0827, "lon": 80.2707},
    "Kolkata": {"state": "West Bengal", "lat": 22.5726, "lon": 88.3639},
    "Ahmedabad": {"state": "Gujarat", "lat": 23.0225, "lon": 72.5714},
    "Pune": {"state": "Maharashtra", "lat": 18.5204, "lon": 73.8567},
    "Jaipur": {"state": "Rajasthan", "lat": 26.9124, "lon": 75.7873},
    "Lucknow": {"state": "Uttar Pradesh", "lat": 26.8467, "lon": 80.9462},
    "Mankhal": {"state": "Telangana", "lat": 17.2734, "lon": 78.5321},
    # Additional major cities
    "Chandigarh": {"state": "Punjab", "lat": 30.7333, "lon": 76.7794},
    "Coimbatore": {"state": "Tamil Nadu", "lat": 11.0168, "lon": 76.9558},
    "Kochi": {"state": "Kerala", "lat": 9.9312, "lon": 76.2673},
    "Bhopal": {"state": "Madhya Pradesh", "lat": 23.2599, "lon": 77.4126},
    "Patna": {"state": "Bihar", "lat": 25.5941, "lon": 85.1376},
    "Guwahati": {"state": "Assam", "lat": 26.1445, "lon": 91.7362},
    "Nagpur": {"state": "Maharashtra", "lat": 21.1458, "lon": 79.0882},
    "Surat": {"state": "Gujarat", "lat": 21.1702, "lon": 72.8311},
    "Visakhapatnam": {"state": "Andhra Pradesh", "lat": 17.6868, "lon": 83.2185},
}

INDIA_SEASONS = {
    (12, 1, 2): "Winter", 
    (3, 4, 5): "Summer", 
    (6, 7, 8, 9): "Monsoon", 
    (10, 11): "Post-Monsoon"
}

def get_current_season():
    """Get the current season based on month"""
    current_month = datetime.now().month
    for months, season in INDIA_SEASONS.items():
        if current_month in months:
            return season
    return "Unknown"

def get_season_style(season):
    """Get CSS class for the season"""
    season_lower = season.lower()
    if "winter" in season_lower:
        return "winter"
    elif "summer" in season_lower:
        return "summer"
    elif "monsoon" in season_lower:
        return "monsoon"
    else:
        return "post-monsoon"

def validate_city_name(city_name):
    """Validates and corrects common city name typos"""
    common_typos = {
        "hydearabad": "hyderabad",
        "mumbaii": "mumbai",
        "dilli": "delhi",
        "banglore": "bangalore",
        "bangaluru": "bangalore",
        "chenai": "chennai",
        "kolkatta": "kolkata",
        "calcutta": "kolkata",
        "puna": "pune",
        "jaipure": "jaipur",
        "lukhnow": "lucknow",
        "bombay": "mumbai",
        "madras": "chennai",
        "poona": "pune",
        "bengluru": "bangalore",
        "varansi": "varanasi",
        "agra": "agra",
        "baroda": "vadodara"
    }
    
    # Check for typos and correct them
    if city_name.lower() in common_typos:
        corrected = common_typos[city_name.lower()]
        return corrected, True
    
    # Check for partial matches in MAJOR_CITIES dictionary
    for city in MAJOR_CITIES:
        if city.lower().startswith(city_name.lower()):
            return city, True
    
    # No correction found
    return city_name, False

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_weather_data(location, api_key, by_coords=False, lat=None, lon=None):
    """Fetch current weather data from OpenWeatherMap API"""
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    if by_coords and lat is not None and lon is not None:
        params = {"lat": lat, "lon": lon, "appid": api_key, "units": "metric"}
    else:
        params = {"q": f"{location},in", "appid": api_key, "units": "metric"}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return data
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            st.error(f"Location '{location}' not found. Please check spelling or try another location.")
        else:
            st.error(f"Error fetching weather data: {e}")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching weather data: {e}")
        return None

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_forecast_data(location, api_key, by_coords=False, lat=None, lon=None):
    """Fetch 5-day forecast data from OpenWeatherMap API"""
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    if by_coords and lat is not None and lon is not None:
        params = {"lat": lat, "lon": lon, "appid": api_key, "units": "metric"}
    else:
        params = {"q": f"{location},in", "appid": api_key, "units": "metric"}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            # Error already displayed by get_weather_data
            pass
        else:
            st.error(f"Error fetching forecast data: {e}")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching forecast data: {e}")
        return None

@st.cache_data(ttl=1800)  # Cache for 30 minutes
def get_air_quality_data(lat, lon, api_key):
    """Fetch air quality data from OpenWeatherMap API"""
    base_url = "https://api.openweathermap.org/data/2.5/air_pollution"
    params = {"lat": lat, "lon": lon, "appid": api_key}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching air quality data: {e}")
        return None

def refresh_data():
    """Force refresh of all cached data"""
    st.cache_data.clear()
    st.session_state.last_refresh = datetime.now()
    st.rerun()

def calculate_dew_point(temp, humidity):
    """Calculate dew point from temperature and humidity"""
    a = 17.27
    b = 237.7
    alpha = ((a * temp) / (b + temp)) + np.log(humidity / 100.0)
    return (b * alpha) / (a - alpha)

def process_forecast_data(forecast_data):
    """Process forecast data into a pandas DataFrame"""
    if not forecast_data or 'list' not in forecast_data:
        return pd.DataFrame()
    processed_data = []
    for item in forecast_data['list']:
        dt = datetime.fromtimestamp(item['dt'])
        temp = item['main']['temp']
        feels_like = item['main']['feels_like']
        humidity = item['main']['humidity']
        pressure = item['main']['pressure']
        wind_speed = item['wind']['speed']
        description = item['weather'][0]['description']
        icon = item['weather'][0]['icon']
        
        # Add precipitation probability if available, default to 0 if not present
        precipitation = item.get('pop', 0) * 100  # Convert to percentage
        
        processed_data.append({
            'datetime': dt,
            'date': dt.date(),
            'time': dt.time(),
            'temperature': temp,
            'feels_like': feels_like,
            'humidity': humidity,
            'pressure': pressure,
            'wind_speed': wind_speed,
            'description': description,
            'icon': icon,
            'precipitation': precipitation
        })
    df = pd.DataFrame(processed_data)
    return df
def search_indian_location(query, location_type):
    """Search for a location in India"""
    # First validate and correct any typos
    corrected_query, was_corrected = validate_city_name(query)
    
    if was_corrected:
        st.info(f"Showing results for '{corrected_query}' instead of '{query}'")
    
    if location_type == "City":
        for city, details in MAJOR_CITIES.items():
            if corrected_query.lower() in city.lower():
                return {"name": city, "state": details["state"], "lat": details["lat"], "lon": details["lon"]}
        return {"name": corrected_query, "state": None, "lat": None, "lon": None}
    elif location_type == "State":
        for state in INDIAN_STATES:
            if corrected_query.lower() in state.lower():
                return {"name": state, "state": state, "lat": None, "lon": None}
        return {"name": corrected_query, "state": None, "lat": None, "lon": None}
    return {"name": corrected_query, "state": None, "lat": None, "lon": None}

def get_weather_recommendations(weather_data, season, forecast_df=None):
    """Generate weather recommendations based on current conditions and season"""
    if not weather_data:
        return []
    recommendations = []
    temp = weather_data['main']['temp']
    humidity = weather_data['main']['humidity']
    wind_speed = weather_data['wind']['speed']
    
    # Temperature-based recommendations
    if temp > 35:
        recommendations.append("Stay hydrated and avoid outdoor activities during peak hours (12-4 PM).")
        recommendations.append("Use protective clothing and sunscreen when going outside.")
    elif temp > 30:
        recommendations.append("Stay hydrated and try to limit exposure during the hottest part of the day.")
    elif temp < 10:
        recommendations.append("Dress in layers and protect extremities in cold conditions.")
    
    # Humidity-based recommendations
    if humidity > 80:
        recommendations.append("High humidity can make heat feel worse. Use fans or AC to improve comfort.")
    
    # Season-specific recommendations
    if season == "Monsoon":
        recommendations.append("Carry an umbrella and wear water-resistant footwear.")
        recommendations.append("Be cautious of waterlogging and potential flooding in low-lying areas.")
    elif season == "Summer":
        recommendations.append("Avoid peak sun exposure between 12-4 PM.")
        recommendations.append("Drink plenty of water and consume seasonal fruits to stay hydrated.")
    elif season == "Winter":
        recommendations.append("Morning fog may reduce visibility - take precautions if traveling.")
    
    # Weather condition-based recommendations
    if 'weather' in weather_data and weather_data['weather']:
        main_weather = weather_data['weather'][0]['main'].lower()
        if 'rain' in main_weather:
            recommendations.append("Carry an umbrella and wear appropriate footwear.")
        elif 'thunderstorm' in main_weather:
            recommendations.append("Seek shelter indoors and avoid open areas or tall trees.")
        elif 'clear' in main_weather and temp > 30:
            recommendations.append("Use sunscreen and stay hydrated when outdoors.")
    
    # Add forecast-based recommendations
    if forecast_df is not None and not forecast_df.empty:
        next_12h = forecast_df.iloc[:4].copy()  # Next 12 hours (4 x 3-hour intervals)
        
        # Check for precipitation in next 12 hours
        if (next_12h['precipitation'] > 50).any():
            recommendations.append("Rain expected in the next 12 hours. Plan indoor activities or carry rain gear.")
        
        # Check for temperature change
        if (next_12h['temperature'].max() - next_12h['temperature'].min()) > 8:
            recommendations.append("Significant temperature changes expected. Dress in layers for comfort throughout the day.")
    
    return recommendations

def get_aqi_label(aqi):
    """Get label for Air Quality Index"""
    if aqi == 1:
        return "Good"
    elif aqi == 2:
        return "Fair" 
    elif aqi == 3:
        return "Moderate"
    elif aqi == 4:
        return "Poor"
    elif aqi == 5:
        return "Very Poor"
    else:
        return "Unknown"

def get_aqi_message(aqi):
    """Get health message for Air Quality Index"""
    if aqi <= 2:
        return "Air quality is acceptable. Enjoy outdoor activities."
    elif aqi == 3:
        return "Air quality is acceptable. However, unusually sensitive people should consider reducing outdoor activity."
    elif aqi == 4:
        return "May cause breathing discomfort to people with lung disease, children and older adults."
    else:
        return "May cause respiratory illness to people on prolonged exposure. Avoid outdoor activities."

def visualize_current_weather_modern(weather_data, location_info, season, air_quality_data=None, forecast_df=None):
    """Display current weather data in a modern UI"""
    if not weather_data:
        st.warning("No current weather data available.")
        return
    
    city_name = weather_data['name']
    if 'sys' in weather_data and 'country' in weather_data['sys']:
        country = weather_data['sys']['country']
    else:
        country = "IN"
    
    temp = weather_data['main']['temp']
    feels_like = weather_data['main']['feels_like']
    humidity = weather_data['main']['humidity']
    pressure = weather_data['main']['pressure']
    wind_speed = weather_data['wind']['speed']
    wind_deg = weather_data['wind']['deg'] if 'deg' in weather_data['wind'] else 0
    description = weather_data['weather'][0]['description']
    icon_code = weather_data['weather'][0]['icon']
    
    # Convert pressure from hPa to inHg for matching the UI
    pressure_inhg = pressure * 0.02953
    
    # Calculate dew point
    dew_point = calculate_dew_point(temp, humidity)
    
    # Format sunrise/sunset
    if 'sys' in weather_data and 'sunrise' in weather_data['sys'] and 'sunset' in weather_data['sys']:
        sunrise_dt = datetime.fromtimestamp(weather_data['sys']['sunrise'])
        sunset_dt = datetime.fromtimestamp(weather_data['sys']['sunset'])
        sunrise = sunrise_dt.strftime('%H:%M')
        sunset = sunset_dt.strftime('%H:%M')
        
        # Determine if it's currently day or night for theming
        current_time = datetime.now()
        is_daytime = sunrise_dt <= current_time <= sunset_dt
        
        # Update theme mode
        st.session_state.theme_mode = "day" if is_daytime else "night"
    else:
        sunrise = "N/A"
        sunset = "N/A"
    
    # Main weather card with modern design
    season_style = get_season_style(season)
    
    # Dynamic header based on day/night
    mode_class = "day-mode" if st.session_state.theme_mode == "day" else "night-mode"
    st.markdown(f"""
    <div class="header-card {mode_class}">
        <div>
            <h2>India Weather Analytics</h2>
            <div class="seasonal-tag {season_style}">{season} Season</div>
        </div>
        <div class="live-indicator">
            <div class="live-indicator-dot"></div>
            LIVE
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Add refresh controls
    col1, col2 = st.columns([3, 1])
    with col1:
        last_update = st.session_state.last_refresh.strftime("%H:%M:%S")
        st.markdown(f"""
        <div class="refresh-status">
            Last updated: {last_update}
        </div>
        """, unsafe_allow_html=True)
    with col2:
        refresh_col1, refresh_col2 = st.columns([1, 1])
        with refresh_col1:
            if st.button("🔄 Refresh"):
                refresh_data()
        with refresh_col2:
            auto_refresh = st.toggle("Auto", value=st.session_state.auto_refresh)
            if auto_refresh != st.session_state.auto_refresh:
                st.session_state.auto_refresh = auto_refresh
                st.rerun()
    
    # Auto refresh timer
    if st.session_state.auto_refresh:
        time_since_refresh = (datetime.now() - st.session_state.last_refresh).total_seconds() / 60
        if time_since_refresh >= st.session_state.refresh_interval:
            refresh_data()
        
        # Continue the auto-refresh countdown display
        minutes_left = max(0, int(st.session_state.refresh_interval - time_since_refresh))
        seconds_left = max(0, int(60 * (st.session_state.refresh_interval - time_since_refresh) % 60))
        st.markdown(f"""
        <div class="refresh-status">
            Next refresh in: {minutes_left}m {seconds_left}s
        </div>
        """, unsafe_allow_html=True)
    
    # Weather data display with columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div class="weather-card">
            <div class="location-header">{city_name}, {location_info['state'] or country}</div>
            <div class="weather-desc">{description.title()}</div>
            <div style="display: flex; align-items: center;">
                <img src="https://openweathermap.org/img/wn/{icon_code}@2x.png" class="weather-icon-large" alt="{description}">
                <div class="big-temp">{temp:.1f}°C</div>
                <div style="margin-left: 20px;">
                    <div class="metric-label">Feels Like</div>
                    <div class="metric-value">{feels_like:.1f}°C</div>
                </div>
            </div>
            <div class="metric-row">
                <div class="metric-container">
                    <div class="metric-label">Humidity</div>
                    <div class="metric-value">{humidity}%</div>
                </div>
                <div class="metric-container">
                    <div class="metric-label">Wind</div>
                    <div class="metric-value">{wind_speed} m/s</div>
                </div>
                <div class="metric-container">
                    <div class="metric-label">Pressure</div>
                    <div class="metric-value">{pressure_inhg:.2f} inHg</div>
                </div>
                <div class="metric-container">
                    <div class="metric-label">Dew Point</div>
                    <div class="metric-value">{dew_point:.1f}°C</div>
                </div>
            </div>
            <div class="sunset-sunrise">
                <div class="metric-row">
                    <div>
                        <div class="metric-label">Sunrise</div>
                        <div class="metric-value">{sunrise}</div>
                    </div>
                    <div>
                        <div class="metric-label">Sunset</div>
                        <div class="metric-value">{sunset}</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Air Quality section if data is available
        if air_quality_data and 'list' in air_quality_data and air_quality_data['list']:
            aqi = air_quality_data['list'][0]['main']['aqi']
            aqi_label = get_aqi_label(aqi)
            aqi_message = get_aqi_message(aqi)
            
            # Air quality details
            co = air_quality_data['list'][0]['components']['co']
            no2 = air_quality_data['list'][0]['components']['no2']
            o3 = air_quality_data['list'][0]['components']['o3']
            pm2_5 = air_quality_data['list'][0]['components']['pm2_5']
            pm10 = air_quality_data['list'][0]['components']['pm10']
            
            st.markdown(f"""
            <div class="weather-card">
                <div class="location-header">Air Quality</div>
                <div class="weather-desc">{aqi_label} - AQI: {aqi}</div>
                <div class="air-quality-indicator">
                    <div class="green"></div>
                    <div class="yellow"></div>
                    <div class="orange"></div>
                    <div class="red"></div>
                    <div class="purple"></div>
                </div>
                <div class="current-marker" style="margin-left: {(aqi-1) * 20}%;"></div>
                <div class="metric-label" style="margin-top: 10px;">{aqi_message}</div>
                <div class="metric-row">
                    <div class="metric-container">
                        <div class="metric-label">PM2.5</div>
                        <div class="metric-value">{pm2_5:.1f}</div>
                    </div>
                    <div class="metric-container">
                        <div class="metric-label">PM10</div>
                        <div class="metric-value">{pm10:.1f}</div>
                    </div>
                    <div class="metric-container">
                        <div class="metric-label">O₃</div>
                        <div class="metric-value">{o3:.1f}</div>
                    </div>
                    <div class="metric-container">
                        <div class="metric-label">NO₂</div>
                        <div class="metric-value">{no2:.1f}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        # Recommendations card
        recommendations = get_weather_recommendations(weather_data, season, forecast_df)
        rec_html = ""
        for rec in recommendations:
            rec_html += f"<li>{rec}</li>"
        
        st.markdown(f"""
        <div class="weather-card">
            <div class="location-header">Weather Recommendations</div>
            <ul>
                {rec_html}
            </ul>
        </div>
        """, unsafe_allow_html=True)

def visualize_forecast_data(forecast_df):
    """Visualize forecast data using plotly"""
    if forecast_df.empty:
        st.warning("No forecast data available.")
        return
    
    st.markdown(f"""
    <div class="weather-card">
        <div class="location-header">5-Day Weather Forecast</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Group by date and select key metrics
    daily_forecast = forecast_df.groupby('date').agg({
        'temperature': ['min', 'max', 'mean'],
        'humidity': 'mean',
        'precipitation': 'max',
        'wind_speed': 'mean',
        'icon': lambda x: x.iloc[0] if not x.empty else "01d"  # Use first icon instead of mode
    }).reset_index()
    
    # Flatten the column multi-index
    daily_forecast.columns = ['_'.join(col).strip('_') for col in daily_forecast.columns.values]
    
    # Format date for display
    daily_forecast['display_date'] = daily_forecast['date'].apply(lambda x: x.strftime('%a, %b %d'))
    
    # Display daily forecast cards
    cols = st.columns(len(daily_forecast))
    for i, (idx, day) in enumerate(daily_forecast.iterrows()):
        with cols[i]:
            # Ensure icon is accessible before using it
            icon = day.get('icon', '01d')  # Default to '01d' if missing
            
            # Use precipitation_max instead of precipitation
            precipitation_value = day.get('precipitation_max', 0)  # Use the correctly named column with fallback
            
            st.markdown(f"""
            <div class="forecast-card">
                <div style="font-weight: bold;">{day['display_date']}</div>
                <img src="https://openweathermap.org/img/wn/{icon}@2x.png" style="width: 50px;" alt="Weather Icon">
                <div style="font-size: 16px;">{day['temperature_max']:.1f}° / {day['temperature_min']:.1f}°</div>
                <div style="font-size: 12px; color: {COLORS['text_light']};">
                    <span title="Precipitation chance">{precipitation_value:.0f}% </span> |
                    <span title="Humidity">{day['humidity_mean']:.0f}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True) 
    # Create hourly temperature and precipitation forecast charts
    first_two_days = forecast_df[forecast_df['datetime'] < (datetime.now() + timedelta(days=2))]
    
    if not first_two_days.empty:
        # Temperature chart
        temp_fig = px.line(
            first_two_days, 
            x='datetime', 
            y=['temperature', 'feels_like'], 
            title='Temperature Forecast (48h)',
            labels={'value': 'Temperature (°C)', 'datetime': 'Date & Time', 'variable': 'Metric'},
            color_discrete_map={'temperature': COLORS['primary'], 'feels_like': COLORS['secondary']}
        )
        temp_fig.update_layout(
            legend_title_text='',
            hovermode="x unified",
            plot_bgcolor=COLORS['background'],
            paper_bgcolor=COLORS['background'],
            font_color=COLORS['text'],
            margin=dict(l=10, r=10, t=40, b=10)
        )
        st.plotly_chart(temp_fig, use_container_width=True)
        
        # Precipitation chart
        precip_fig = px.bar(
            first_two_days, 
            x='datetime', 
            y='precipitation', 
            title='Precipitation Probability (48h)',
            labels={'precipitation': 'Probability (%)', 'datetime': 'Date & Time'},
            color_discrete_sequence=[COLORS['info']]
        )
        precip_fig.update_layout(
            hovermode="x unified",
            plot_bgcolor=COLORS['background'],
            paper_bgcolor=COLORS['background'],
            font_color=COLORS['text'],
            margin=dict(l=10, r=10, t=40, b=10)
        )
        st.plotly_chart(precip_fig, use_container_width=True)

def visualize_historical_trends(selected_location):
    """Visualize historical weather trends for the selected location"""
    st.markdown(f"""
    <div class="weather-card">
        <div class="location-header">Historical Weather Trends</div>
        <div class="weather-desc">Showing simulated historical data for demonstration purposes</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Simulate historical data
    np.random.seed(42)  # For reproducibility
    dates = pd.date_range(end=datetime.now(), periods=365, freq='D')
    
    # Generate seasonal temperature data with some randomness
    seasonal_component = 10 * np.sin(np.linspace(0, 2*np.pi, 365))  # Seasonal cycle
    trend_component = np.linspace(0, 2, 365)  # Slight warming trend
    random_component = np.random.normal(0, 3, 365)  # Random variations
    
    # Generate different patterns based on location
    location_hash = hash(selected_location) % 100
    temp_offset = (location_hash % 10) - 5  # Between -5 and 4
    
    avg_temps = 25 + temp_offset + seasonal_component + trend_component + random_component
    max_temps = avg_temps + np.random.uniform(3, 8, 365)
    min_temps = avg_temps - np.random.uniform(3, 8, 365)
    
    # Rainfall data - more during monsoon season
    monsoon_component = 15 * np.sin(np.linspace(-np.pi/2, 3*np.pi/2, 365))
    rainfall = np.maximum(0, monsoon_component + np.random.normal(0, 5, 365))
    
    # Create dataframe
    historical_df = pd.DataFrame({
        'date': dates,
        'avg_temp': avg_temps,
        'max_temp': max_temps,
        'min_temp': min_temps,
        'rainfall': rainfall
    })
    
    # Add month for grouping
    historical_df['month'] = historical_df['date'].dt.month
    historical_df['month_name'] = historical_df['date'].dt.strftime('%b')
    
    # Monthly aggregations
    monthly_data = historical_df.groupby('month').agg({
        'avg_temp': 'mean',
        'max_temp': 'mean',
        'min_temp': 'mean',
        'rainfall': 'sum',
        'month_name': 'first'
    }).reset_index()
    
    # Sort by month
    monthly_data = monthly_data.sort_values('month')
    
    # Create temperature chart
    temp_fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add temperature lines
    temp_fig.add_trace(
        go.Scatter(
            x=monthly_data['month_name'], 
            y=monthly_data['avg_temp'],
            name="Avg Temp",
            line=dict(color=COLORS['primary'], width=3),
            mode='lines+markers'
        )
    )
    
    temp_fig.add_trace(
        go.Scatter(
            x=monthly_data['month_name'], 
            y=monthly_data['max_temp'],
            name="Max Temp",
            line=dict(color=COLORS['danger'], width=2, dash='dot'),
            mode='lines+markers'
        )
    )
    
    temp_fig.add_trace(
        go.Scatter(
            x=monthly_data['month_name'], 
            y=monthly_data['min_temp'],
            name="Min Temp",
            line=dict(color=COLORS['info'], width=2, dash='dot'),
            mode='lines+markers'
        )
    )
    
    # Add rainfall bars on secondary y-axis
    temp_fig.add_trace(
        go.Bar(
            x=monthly_data['month_name'],
            y=monthly_data['rainfall'],
            name="Rainfall",
            marker_color=COLORS['secondary'],
            opacity=0.3
        ),
        secondary_y=True
    )
    
    # Update layout
    temp_fig.update_layout(
        title="Monthly Average Temperature and Rainfall (Last 12 Months)",
        xaxis_title="Month",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font_color=COLORS['text'],
        margin=dict(l=10, r=10, t=40, b=10)
    )
    
    # Update y-axes
    temp_fig.update_yaxes(title_text="Temperature (°C)", secondary_y=False)
    temp_fig.update_yaxes(title_text="Rainfall (mm)", secondary_y=True)
    
    st.plotly_chart(temp_fig, use_container_width=True)
    
    # Temperature anomaly chart - deviation from the average
    annual_avg = historical_df['avg_temp'].mean()
    historical_df['temp_anomaly'] = historical_df['avg_temp'] - annual_avg
    
    # Calculate monthly anomalies
    monthly_anomalies = historical_df.groupby('month').agg({
        'temp_anomaly': 'mean',
        'month_name': 'first'
    }).reset_index()
    monthly_anomalies = monthly_anomalies.sort_values('month')
    
    # Create anomaly chart
    colors = [COLORS['danger'] if x > 0 else COLORS['info'] for x in monthly_anomalies['temp_anomaly']]
    
    anomaly_fig = go.Figure(go.Bar(
        x=monthly_anomalies['month_name'],
        y=monthly_anomalies['temp_anomaly'],
        marker_color=colors
    ))
    
    anomaly_fig.update_layout(
        title="Monthly Temperature Anomalies (Deviation from Annual Average)",
        xaxis_title="Month",
        yaxis_title="Temperature Anomaly (°C)",
        hovermode="x unified",
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font_color=COLORS['text'],
        margin=dict(l=10, r=10, t=40, b=10)
    )
    
    # Add a reference line at zero
    anomaly_fig.add_shape(
        type="line",
        x0=-0.5,
        x1=11.5,
        y0=0,
        y1=0,
        line=dict(color=COLORS['text_light'], width=1, dash="dash")
    )
    
    st.plotly_chart(anomaly_fig, use_container_width=True)

def alert_check(location, weather_data, forecast_df):
    """Check for weather alerts based on user thresholds"""
    if not weather_data:
        return []
    
    alerts = []
    thresholds = st.session_state.alert_thresholds
    
    # Current weather alerts
    if weather_data['main']['temp'] > thresholds['temp_max']:
        alerts.append(f"High temperature alert: {weather_data['main']['temp']:.1f}°C exceeds your {thresholds['temp_max']}°C threshold")
    
    if weather_data['main']['temp'] < thresholds['temp_min']:
        alerts.append(f"Low temperature alert: {weather_data['main']['temp']:.1f}°C is below your {thresholds['temp_min']}°C threshold")
    
    if weather_data['main']['humidity'] > thresholds['humidity']:
        alerts.append(f"High humidity alert: {weather_data['main']['humidity']}% exceeds your {thresholds['humidity']}% threshold")
    
    if weather_data['wind']['speed'] > thresholds['wind_speed']:
        alerts.append(f"High wind alert: {weather_data['wind']['speed']} m/s exceeds your {thresholds['wind_speed']} m/s threshold")
    
    # Forecast alerts
    if not forecast_df.empty and 'precipitation' in forecast_df.columns:
        next_24h = forecast_df.iloc[:8]  # Next 24 hours (8 x 3-hour intervals)
        
        if (next_24h['precipitation'] >= 70).any():
            alerts.append(f"Heavy rain expected in the next 24 hours in {location}")
        
        if (next_24h['temperature'] > thresholds['temp_max']).any():
            alerts.append(f"High temperatures expected in the next 24 hours in {location}")
            
        if (next_24h['temperature'] < thresholds['temp_min']).any():
            alerts.append(f"Low temperatures expected in the next 24 hours in {location}")
            
        if (next_24h['wind_speed'] > thresholds['wind_speed']).any():
            alerts.append(f"Strong winds expected in the next 24 hours in {location}")
    
    return alerts
def settings_page():
    """Display and handle settings page"""
    st.title("Settings")
    
    # Refresh settings
    st.header("Auto-Refresh Settings")
    auto_refresh = st.toggle("Enable Auto-Refresh", value=st.session_state.auto_refresh)
    refresh_interval = st.slider("Refresh Interval (minutes)", 
                                min_value=5, 
                                max_value=60, 
                                value=st.session_state.refresh_interval,
                                step=5)
    
    if auto_refresh != st.session_state.auto_refresh or refresh_interval != st.session_state.refresh_interval:
        st.session_state.auto_refresh = auto_refresh
        st.session_state.refresh_interval = refresh_interval
        st.success("Auto-refresh settings updated!")
    
    # Weather alerts thresholds
    st.header("Weather Alert Thresholds")
    col1, col2 = st.columns(2)
    
    with col1:
        temp_max = st.number_input("High Temperature Alert (°C)", 
                                 min_value=25, 
                                 max_value=50, 
                                 value=st.session_state.alert_thresholds['temp_max'])
        
        temp_min = st.number_input("Low Temperature Alert (°C)", 
                                 min_value=-10, 
                                 max_value=20, 
                                 value=st.session_state.alert_thresholds['temp_min'])
    
    with col2:
        humidity = st.number_input("High Humidity Alert (%)", 
                                 min_value=50, 
                                 max_value=100, 
                                 value=st.session_state.alert_thresholds['humidity'])
        
        wind_speed = st.number_input("High Wind Alert (m/s)", 
                                   min_value=5, 
                                   max_value=30, 
                                   value=st.session_state.alert_thresholds['wind_speed'])
    
    if (temp_max != st.session_state.alert_thresholds['temp_max'] or
        temp_min != st.session_state.alert_thresholds['temp_min'] or
        humidity != st.session_state.alert_thresholds['humidity'] or
        wind_speed != st.session_state.alert_thresholds['wind_speed']):
        
        st.session_state.alert_thresholds = {
            'temp_max': temp_max,
            'temp_min': temp_min,
            'humidity': humidity,
            'wind_speed': wind_speed,
            'uv_index': st.session_state.alert_thresholds['uv_index']
        }
        st.success("Alert thresholds updated!")
    
    # Location settings
    st.header("Default Location")
    locations = list(MAJOR_CITIES.keys())
    default_location = st.selectbox("Select Default Location", options=locations)
    
    if st.button("Set as Default"):
        if default_location not in st.session_state.user_locations:
            st.session_state.user_locations.insert(0, default_location)
        else:
            # Move to the front of the list
            st.session_state.user_locations.remove(default_location)
            st.session_state.user_locations.insert(0, default_location)
        st.success(f"{default_location} set as your default location!")
    
    # API settings
    st.header("API Settings")
    
    # This is just for display, not actually changing the API key for security reasons
    api_key_display = "••••••••" + api_key[-4:] if api_key else ""
    st.text_input("API Key", value=api_key_display, disabled=True, 
                help="For security reasons, API keys can only be set via environment variables or secrets.")

def main():
    """Main function to run the Streamlit app"""
    # Sidebar
    st.sidebar.markdown(f"""
    <div class="sidebar-title">
        <h2>India Weather Analytics</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    st.sidebar.markdown("<div class='sidebar-subtitle'>Navigation</div>", unsafe_allow_html=True)
    page = st.sidebar.radio("", ["Dashboard", "Settings"])
    
    # Location search section in sidebar
    st.sidebar.markdown("<div class='sidebar-subtitle'>Location</div>", unsafe_allow_html=True)
    
    # Location search options
    location_type = st.sidebar.radio("Search by:", ["City", "State"], horizontal=True)
    st.session_state.location_type = location_type
    
    # Quick location selection
    if st.session_state.user_locations:
        locations_with_add = st.session_state.user_locations + ["+ Add New Location"]
        selected_quick_location = st.sidebar.selectbox("Saved Locations", options=locations_with_add)
        
        if selected_quick_location == "+ Add New Location":
            show_search = True
        else:
            show_search = False
            selected_location = selected_quick_location
    else:
        show_search = True
    
    # Search field
    if show_search:
        search_query = st.sidebar.text_input("Search location", placeholder="Enter city or state name")
        search_button = st.sidebar.button("Search")
        
        if search_button and search_query:
            location_info = search_indian_location(search_query, location_type)
            selected_location = location_info['name']
            
            # Add to recent locations if not already present
            if selected_location and selected_location not in st.session_state.user_locations:
                st.session_state.user_locations.append(selected_location)
    
    # Weather alerts section in sidebar
    st.sidebar.markdown("<div class='sidebar-subtitle'>Weather Alerts</div>", unsafe_allow_html=True)
    
    alerts_container = st.sidebar.container()
    
    # Refresh interval selector in sidebar when auto-refresh is on
    if st.session_state.auto_refresh:
        st.sidebar.markdown("<div class='sidebar-subtitle'>Auto-Refresh</div>", unsafe_allow_html=True)
        new_interval = st.sidebar.slider("Interval (minutes)", 
                                        min_value=5, 
                                        max_value=60, 
                                        value=st.session_state.refresh_interval,
                                        step=5)
        if new_interval != st.session_state.refresh_interval:
            st.session_state.refresh_interval = new_interval
    
    # Main content
    if page == "Dashboard":
        if 'selected_location' in locals():
            # Determine if we should use coordinates
            use_coords = False
            lat, lon = None, None
            
            # Check if location is in our predefined cities
            if selected_location in MAJOR_CITIES:
                use_coords = True
                lat = MAJOR_CITIES[selected_location]["lat"]
                lon = MAJOR_CITIES[selected_location]["lon"]
                location_info = {
                    "name": selected_location,
                    "state": MAJOR_CITIES[selected_location]["state"],
                    "lat": lat,
                    "lon": lon
                }
            else:
                location_info = search_indian_location(selected_location, location_type)
                if location_info["lat"] and location_info["lon"]:
                    use_coords = True
                    lat = location_info["lat"]
                    lon = location_info["lon"]
            
            # Fetch weather data
            if use_coords:
                weather_data = get_weather_data(selected_location, api_key, by_coords=True, lat=lat, lon=lon)
                forecast_data = get_forecast_data(selected_location, api_key, by_coords=True, lat=lat, lon=lon)
                air_quality_data = get_air_quality_data(lat, lon, api_key)
            else:
                weather_data = get_weather_data(selected_location, api_key)
                forecast_data = get_forecast_data(selected_location, api_key)
                if weather_data and 'coord' in weather_data:
                    air_quality_data = get_air_quality_data(weather_data['coord']['lat'], weather_data['coord']['lon'], api_key)
                else:
                    air_quality_data = None
            
            # Process forecast data
            forecast_df = process_forecast_data(forecast_data)
            
            # Check for alerts
            alerts = alert_check(selected_location, weather_data, forecast_df)
            
            # Display alerts in sidebar
            with alerts_container:
                if alerts:
                    st.markdown(f"""
                    <div style="display: flex; align-items: center;">
                        <span style="font-weight: bold; color: {COLORS['danger']};">Active Alerts</span>
                        <div class="alert-badge">{len(alerts)}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    for alert in alerts:
                        st.warning(alert)
                else:
                    st.info("No weather alerts")
            
            # Get current season
            current_season = get_current_season()
            
            # Display current weather data
            visualize_current_weather_modern(weather_data, location_info, current_season, air_quality_data, forecast_df)
            
            # Display forecast data
            visualize_forecast_data(forecast_df)
            
            # Display historical trends
            visualize_historical_trends(selected_location)
            
        else:
            # Welcome message when no location is selected
            st.markdown(f"""
            <div class="weather-card" style="text-align: center; padding: 40px;">
                <h2>Welcome to India Weather Analytics Dashboard</h2>
                <p>Search for a city or state in the sidebar to start exploring weather data.</p>
                <p>This dashboard provides comprehensive weather information, forecasts, and historical trends for locations across India.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Display a map of India with major cities
            st.markdown(f"""
            <div class="weather-card">
                <div class="location-header">Popular Cities</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Create dataframe for map
            cities_data = []
            for city, details in MAJOR_CITIES.items():
                cities_data.append({
                    'city': city,
                    'state': details['state'],
                    'lat': details['lat'],
                    'lon': details['lon']
                })
            
            cities_df = pd.DataFrame(cities_data)
            
            # Create map
            india_center = {'lat': 22.5937, 'lon': 78.9629}
            fig = px.scatter_mapbox(
                cities_df,
                lat="lat",
                lon="lon",
                hover_name="city",
                hover_data=["state"],
                color_discrete_sequence=[COLORS["primary"]],
                zoom=4,
                center=india_center,
                height=500
            )
            
            fig.update_layout(
                mapbox_style="carto-positron",
                margin={"r":0,"t":0,"l":0,"b":0}
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
    elif page == "Settings":
        settings_page()

if __name__ == "__main__":
    main()
