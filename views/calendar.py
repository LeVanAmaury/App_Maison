import streamlit as st
from datetime import datetime, date, timedelta
from src.database import get_db

st.set_page_config(layout="wide")
st.title("📅 Planning Familial")
db = get_db()

# --- CSS POUR LE LOOK "CALENDRIER" ---
st.markdown("""
    <style>
    div[data-testid="stHorizontalBlock"] { overflow-x: auto; flex-wrap: nowrap !important; }
    div[data-testid="column"] { min-width: 180px; } /* Ajuste la largeur des colonnes */
    .event-card { border-left: 5px solid #ff4b4b; padding-left: 10px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- NAVIGATION ---
if "week_start" not in st.session_state:
    st.session_state.week_start = date.today() - timedelta(days=date.today().weekday())

c_prev, c_center, c_next = st.columns([1, 2, 1])
with c_prev:
    if st.button("⬅️"): st.session_state.week_start -= timedelta(days=7); st.rerun()
with c_next:
    if st.button("➡️"): st.session_state.week_start += timedelta(days=7); st.rerun()
with c_center:
    start, end = st.session_state.week_start, st.session_state.week_start + timedelta(days=6)
    st.markdown(f"<p style='text-align:center'>Semaine du {start.strftime('%d/%m')} au {end.strftime('%d/%m')}</p>", unsafe_allow_html=True)

# --- AFFICHAGE DE LA SEMAINE ---
monday = st.session_state.week_start
events = db.get_calendar(monday.isoformat(), (monday + timedelta(days=6)).isoformat())
jours_fr = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]

# On définit des couleurs pour la vision immédiate
colors = {"Amaury": "#3498db", "Thais": "#9b59b6", "Corentin": "#2ecc71", "Tous": "#e67e22"}

cols = st.columns(7)

for i in range(7):
    current_day = monday + timedelta(days=i)
    with cols[i]:
        # En-tête compact
        color = "red" if current_day == date.today() else "white"
        st.markdown(f"**:{color}[{jours_fr[i]} {current_day.day}]**")
        
        day_events = [e for e in events if e['event_date'] == current_day.isoformat()]
        
        for ev in day_events:
            # On récupère la couleur du membre
            m_color = colors.get(ev['member'], "#7f8c8d")
            
            # Création d'une "carte" visuelle compacte
            with st.container(border=True):
                st.markdown(f"<div style='border-left: 4px solid {m_color}; padding-left:5px'>"
                            f"<b>{ev['event_name'].strip()}</b><br>"
                            f"<small>🕒 {ev['start_time'][:5]}</small></div>", unsafe_allow_html=True)
                
                # Petit bouton de suppression discret
                if st.button("🗑️", key=f"del_{ev['calendar_id']}"):
                    db.remove_calendar(ev['calendar_id'])
                    st.rerun()