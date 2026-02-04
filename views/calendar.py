import streamlit as st
from datetime import datetime, timedelta
from src.database import get_db

st.set_page_config(layout="wide")
st.title("📅 Planning Familial")
db = get_db()

# --- 1. GESTION DE LA NAVIGATION ---
if "week_start" not in st.session_state:
    today = datetime.now().date()
    st.session_state.week_start = today - timedelta(days=today.weekday())

col_prev, col_center, col_next = st.columns([1, 2, 1])

with col_prev:
    if st.button("⬅️ Semaine précédente"):
        st.session_state.week_start -= timedelta(days=7)
        st.rerun()

with col_center:
    start = st.session_state.week_start
    end = start + timedelta(days=6)
    st.markdown(f"<h3 style='text-align: center;'>Du {start.strftime('%d/%m')} au {end.strftime('%d/%m')}</h3>", unsafe_allow_html=True)
    if st.button("Aujourd'hui", use_container_width=True):
        today = datetime.now().date()
        st.session_state.week_start = today - timedelta(days=today.weekday())
        st.rerun()

with col_next:
    if st.button("Semaine suivante ➡️"):
        st.session_state.week_start += timedelta(days=7)
        st.rerun()

st.divider()

# --- 2. RÉCUPÉRATION ET AFFICHAGE ---
monday = st.session_state.week_start
sunday = monday + timedelta(days=6)

events = db.get_calendar(monday.isoformat(), sunday.isoformat())
cols = st.columns(7)
jours_fr = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]

for i in range(7):
    current_day = monday + timedelta(days=i)
    with cols[i]:
        is_today = current_day == datetime.now().date()
        title_color = "red" if is_today else "white"
        st.markdown(f"### :{title_color}[{jours_fr[i]} {current_day.day}]")        
        day_events = [e for e in events if e['event_date'] == current_day.isoformat()]
        
        for ev in day_events:
            with st.container(border=True):
                st.markdown(f"**{ev['event_name']}**")
                st.caption(f"🕒 {ev['start_time'][:5]} - {ev['member']}")
                if st.button("🗑️", key=f"del_{ev['calendar_id']}"):
                    db.remove_calendar(ev['calendar_id'])
                    st.rerun()