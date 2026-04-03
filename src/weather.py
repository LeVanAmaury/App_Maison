import requests
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

def get_weather(city):
    """Fetch weather data from OpenWeatherMap using API key from secrets/env."""
    
    # Try to get from st.secrets first, then os.environ
    api_key = st.secrets.get("OPENWEATHER_API_KEY") if "OPENWEATHER_API_KEY" in st.secrets else os.environ.get("OPENWEATHER_API_KEY")
    
    if not api_key:
        # Fallback to the hardcoded one if none found (but logged as warning)
        api_key = '8fc1087cbf520bc895ce4eabcc13575a'
        
    url = "https://api.openweathermap.org/data/2.5/weather"
    query_params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
        "lang": "fr"
    }
    try:
        response = requests.get(url, params=query_params, timeout=5)
        response.raise_for_status()
        data = response.json()
        return {
            "temp": round(data["main"]["temp"]),
            "desc": data["weather"][0]["description"].capitalize(),
            "icon": data["weather"][0]["icon"]
        }
    except Exception as e:
        st.warning(f"Impossible de récupérer la météo : {e}")
        return None
