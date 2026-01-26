import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def get_weather(city):
    api_key = '8fc1087cbf520bc895ce4eabcc13575a'
    url = f"https://api.openweathermap.org/data/2.5/weather"
    query_params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
        "lang": "fr"
    }
    try:
        response = requests.get(url,params=query_params)
        data = response.json()
        return {
            "temp" : round(data["main"]["temp"]),
            "desc" : data["weather"][0]["description"].capitalize(),
            "icon" : data["weather"][0]["icon"]
        }
    except Exception as e:
        st.error(f"Erreur de connexion : {e}")
        return None