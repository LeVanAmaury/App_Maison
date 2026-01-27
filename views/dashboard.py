import streamlit as st
from src.database import get_db
from datetime import datetime
from src.weather import get_weather

db = get_db()
st.title("📊 Tableau de bord familial")

city_weather = 'Saint-Sulpice'
w = get_weather(city_weather)
col1, col2 = st.columns(2)

with col1:
    if w:
        col_icon, col_temp = st.columns([0.2,0.8])
        with col_icon:
            icon_url = f"https://openweathermap.org/img/wn/{w['icon']}@2x.png"
            st.image(icon_url, width=100)
        with col_temp:
            st.metric(label=f"Météo à {city_weather}", value=f"{w['temp']}°C", delta=w['desc'])
    else:
        st.error("Météo indisponible")

with col2:
    st.info(f"Aujourd'hui nous sommes le **{datetime.now().strftime('%d %B %Y')}**")

st.divider()

st.write("### Le mur de la famille")
with st.expander("Laisser un petit mot sur le mur"):
    with st.form("note_form", clear_on_submit=True):
        note_text = st.text_area("Ton message :", placeholder="Met ce que tu veux")
        if st.form_submit_button("Epingler au mur") and note_text:
            db.add_note(note_text)
            st.success("Note ajoutée !")
            st.rerun()

notes = db.get_notes()
if notes:
    cols = st.columns(3)
    for i, (n_id, n_content, n_date) in enumerate(notes):
        with cols[i % 3]:
            st.info(f"{n_content}\n\n*Posté le {n_date[:10]}*")
            if st.button("Supprimer", key=f"note_{n_id}"):
                db.delete_note(n_id)
                st.rerun()
else:
    st.info("Aucune notes pour le moment. Ajoute en une !")

st.divider()

c1, c2 = st.columns(2)
with c1:
    st.write("### Dernières choses ajoutée au courses")
    if db.get_shopping_list():
        for item in db.get_shopping_list()[:5]:
            st.write(f"- {item[1]}")
    else:
        st.info("Aucune courses pour le moment")

with c2:
    st.write("### ⚠️ Dernières tâches ajoutée")
    if db.get_tasks():
        for task in db.get_tasks()[:5]:
            st.write(f"- **{task[2]}** : {task[1]}")
    else:
        st.info("Aucune tâches pour le moment")