import streamlit as st
from datetime import datetime, date, timedelta
from src.database import get_db

st.set_page_config(layout="wide")
db = get_db()

# --- CSS RADICAL POUR MOBILE (Fini le "Enorme") ---
st.markdown("""
    <style>
    /* 1. On réduit la taille de TOUTE la page sur mobile */
    @media (max-width: 768px) {
        html, body, [data-testid="stAppViewContainer"] {
            font-size: 12px !important;
        }
        /* On réduit les marges de l'application */
        .block-container {
            padding: 0.5rem 0.5rem !important;
        }
        /* On force les colonnes du calendrier à être très serrées */
        div[data-testid="column"] {
            min-width: 100px !important;
            padding: 0px 2px !important;
        }
        /* On réduit la taille des boutons */
        .stButton button {
            padding: 0px 2px !important;
            height: 24px !important;
            min-height: 24px !important;
            font-size: 11px !important;
        }
        /* On réduit les titres h3 (Lun 2, etc) */
        h3 { font-size: 0.9rem !important; margin: 0 !important; padding: 0 !important; }
        /* On réduit l'espace entre les éléments */
        [data-testid="stVerticalBlock"] { gap: 0.2rem !important; }
    }
    
    /* 2. Scroll horizontal pour voir la semaine */
    div[data-testid="stHorizontalBlock"] {
        overflow-x: auto;
        flex-wrap: nowrap !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📅 Planning")

# --- NAVIGATION ULTRA COMPACTE ---
if "week_start" not in st.session_state:
    st.session_state.week_start = date.today() - timedelta(days=date.today().weekday())

# On utilise des ratios très serrés pour que les flèches collent au texte
c1, c2, c3 = st.columns([0.3, 2, 0.3], vertical_alignment="center")
with c1:
    if st.button("⬅️", key="p"):
        st.session_state.week_start -= timedelta(days=7)
        st.rerun()
with c3:
    if st.button("➡️", key="n"):
        st.session_state.week_start += timedelta(days=7)
        st.rerun()
with c2:
    s = st.session_state.week_start
    e = s + timedelta(days=6)
    st.markdown(f"<p style='text-align:center; margin:0; font-weight:bold;'>{s.strftime('%d/%m')} - {e.strftime('%d/%m')}</p>", unsafe_allow_html=True)
    if st.button("Aujourd'hui", use_container_width=True):
        st.session_state.week_start = date.today() - timedelta(days=date.today().weekday())
        st.rerun()

st.divider()

# --- GRILLE DE 7 JOURS ---
monday = st.session_state.week_start
events = db.get_calendar(monday.isoformat(), (monday + timedelta(days=6)).isoformat())
jours_fr = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]

cols = st.columns(7)

for i in range(7):
    day = monday + timedelta(days=i)
    with cols[i]:
        # FIX : On retire le ":white" qui n'existe pas
        is_today = day == date.today()
        label = f"{jours_fr[i]} {day.day}"
        if is_today:
            st.markdown(f"**:red[{label}]**")
        else:
            # Texte normal sans balise de couleur buggée
            st.markdown(f"**{label}**")
        
        day_events = [ev for ev in events if ev['event_date'] == day.isoformat()]
        
        for ev in day_events:
            with st.container(border=True):
                # FIX : .strip() contre le bug des étoiles **
                t = ev['event_name'].strip()
                st.markdown(f"<div style='font-size:0.8rem; line-height:1; font-weight:bold;'>{t}</div>", unsafe_allow_html=True)
                
                # Heures compactes
                st.caption(f"{ev['start_time'][:5]}-{ev['end_time'][:5]} | {ev['member']}")
                
                # FIX KeyError : On utilise calendar_id comme dans ta base
                if st.button("🗑️", key=f"d_{ev['calendar_id']}", use_container_width=True):
                    db.remove_calendar(ev['calendar_id'])
                    st.rerun()