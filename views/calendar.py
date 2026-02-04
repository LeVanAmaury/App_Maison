import streamlit as st
from datetime import datetime, timedelta
from src.database import get_db

st.set_page_config(layout="wide")
st.title("📅 Planning de la Semaine")
db = get_db()

# --- 1. CALCUL DE LA SEMAINE ACTUELLE ---
today = datetime.now().date()
monday = today - timedelta(days=today.weekday())
sunday = monday + timedelta(days=6)

# --- 2. FORMULAIRE D'AJOUT (Dans un expander pour rester propre) ---
with st.expander("Ajouter un événement"):
    with st.form("add_event_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Titre", placeholder="Ex: Concert Amaury")
            e_date = st.date_input("Date", value=today)
        with col2:
            t_start = st.time_input("Début", value=datetime.strptime("19:00", "%H:%M"))
            t_end = st.time_input("Fin", value=datetime.strptime("22:00", "%H:%M"))
        
        member = st.selectbox("Pour qui ?", ["Amaury", "Thais", "Corentin", "Tous"])
        if st.form_submit_button("Enregistrer"):
            db.add_calendar(name, e_date.isoformat(), t_start.isoformat(), t_end.isoformat(), member)
            st.rerun()

st.divider()

# --- 3. AFFICHAGE DE LA GRILLE ---
events = db.get_calendar(monday.isoformat(), sunday.isoformat())
cols = st.columns(7)
jours_fr = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]

for i in range(7):
    current_day = monday + timedelta(days=i)
    with cols[i]:
        is_today = "🔴" if current_day == today else ""
        st.markdown(f"### {jours_fr[i]} {current_day.day}\n{is_today}")
        day_events = [e for e in events if e['event_date'] == current_day.isoformat()]
        if not day_events:
            st.caption("Libre")
        for ev in day_events:
            with st.container(border=True):
                st.markdown(f"**{ev['event_name']}**")
                st.caption(f"🕒 {ev['start_time'][:5]}")
                st.write(f"👤 {ev['member']}")
                if st.button("🗑️", key=f"del_{ev['calendar_id']}"):
                    db.remove_calendar(ev['calendar_id'])
                    st.rerun()