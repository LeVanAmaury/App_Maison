import streamlit as st
from datetime import datetime, date, timedelta
from src.database import get_db

st.set_page_config(layout="wide")
db = get_db()

# --- CSS AGRESSIF POUR ÉCRAN MOBILE ---
st.markdown("""
    <style>
    /* 1. On force les colonnes à rester sur une SEULE ligne, même sur mobile */
    [data-testid="stHorizontalBlock"] {
        flex-direction: row !important;
        overflow-x: auto !important;
        flex-wrap: nowrap !important;
        gap: 0.3rem !important;
    }

    /* 2. On empêche les colonnes de prendre toute la largeur */
    [data-testid="column"] {
        width: 120px !important; /* Largeur fixe pour garder le look grille */
        flex: 0 0 auto !important;
        min-width: 120px !important;
    }

    /* 3. Réduction drastique de la taille des textes et marges sur mobile */
    @media (max-width: 768px) {
        .block-container { padding: 0.5rem !important; }
        h3 { font-size: 0.8rem !important; margin: 0 !important; }
        .stMarkdown p, .stCaption { font-size: 0.75rem !important; line-height: 1.1 !important; }
        
        /* Boutons miniatures */
        .stButton button {
            padding: 0px 4px !important;
            height: 24px !important;
            min-height: 24px !important;
            font-size: 0.7rem !important;
        }

        /* On réduit l'espace interne des cadres (containers) */
        [data-testid="stVerticalBlockBorderWrapper"] > div {
            padding: 0.2rem !important;
            gap: 0px !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

st.title("📅 Planning")

# --- NAVIGATION COMPACTE ---
if "week_start" not in st.session_state:
    st.session_state.week_start = date.today() - timedelta(days=date.today().weekday())

# Alignement centré avec ratios serrés
c1, c2, c3 = st.columns([0.5, 3, 0.5], vertical_alignment="center")
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
    st.markdown(f"<p style='text-align:center; margin:0; font-size:0.8rem;'>{s.strftime('%d/%m')} - {e.strftime('%d/%m')}</p>", unsafe_allow_html=True)

# Bouton Aujourd'hui plus petit
if st.button("Aujourd'hui", use_container_width=True):
    st.session_state.week_start = date.today() - timedelta(days=date.today().weekday())
    st.rerun()

st.divider()

# --- GRILLE DE 7 JOURS ---
monday = st.session_state.week_start
events = db.get_calendar(monday.isoformat(), (monday + timedelta(days=6)).isoformat())
jours_fr = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]

# On utilise gap="small" pour coller les jours
cols = st.columns(7, gap="small")

for i in range(7):
    day = monday + timedelta(days=i)
    with cols[i]:
        is_today = day == date.today()
        label = f"{jours_fr[i]} {day.day}"
        if is_today:
            st.markdown(f"### :red[{label}]")
        else:
            st.markdown(f"### {label}")
        
        day_events = [ev for ev in events if ev['event_date'] == day.isoformat()]
        
        for ev in day_events:
            with st.container(border=True):
                # On force le texte en tout petit via HTML
                t = ev['event_name'].strip()
                st.markdown(f"<div style='font-size:0.75rem; font-weight:bold; line-height:1;'>{t}</div>", unsafe_allow_html=True)
                
                # Heures compactes sans caption (qui prend trop de place)
                debut = ev['start_time'][:5]
                st.markdown(f"<div style='font-size:0.65rem; color:gray;'>{debut} | {ev['member']}</div>", unsafe_allow_html=True)
                
                if st.button("🗑️", key=f"d_{ev['calendar_id']}", use_container_width=True):
                    db.remove_calendar(ev['calendar_id'])
                    st.rerun()