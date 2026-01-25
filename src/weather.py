import requests
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

def get_weather(city="Saint-Sulpice"):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q{city}&appid={api_key}&units=metric&lang=fr"

    try:
        response = requests.get(url)
        data = response.json()
        return {
            "temp" : round(data["main"]["temp"]),
            "desc" : data["weather"][0]["description"].capitalize(),
            "icon" : data["weather"][0]["icon"]
        }
    except Exception as e:
        st.error(f"Erreur de connexion : {e}")
        return None