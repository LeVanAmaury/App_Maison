import streamlit as st
from main import get_db
from datetime import datetime
from src.weather import get_weather

db = get_db()
st.title("📊 Tableau de bord familial")

w = get_weather("Saint Sulpice")
col1, col2 = st.columns(2)

with col1:
    if w:
        st.metric(label=f"Météo à Paris", value=f"{w['temp']}°C", delta=w['desc'])
    else:
        st.warning("Météo indisponible (vérifie ta clé API)")

with col2:
    st.info(f"Aujourd'hui nous sommes le **{datetime.now().strftime('%d %B %Y')}**")

st.divider()

c1, c2 = st.columns(2)
with c1:
    st.write("### 🛒 À acheter d'urgence")
    for item in db.get_shopping_list()[:5]:
        st.write(f"- {item[1]}")

with c2:
    st.write("### ⚠️ Tâches prioritaires")
    for task in db.get_tasks()[:5]:
        st.write(f"- **{task[2]}** : {task[1]}")