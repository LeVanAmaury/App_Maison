import streamlit as st
from datetime import datetime, date, timedelta
from src.database import get_db

st.set_page_config(layout="wide")
db = get_db()

# --- CSS "FORCE BRUTE" POUR RÉDUIRE LA TAILLE SUR MOBILE ---
st.markdown("""
    <style>
    /* 1. On réduit les marges du conteneur principal */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
    }

    /* 2. On force les colonnes à rester serrées */
    div[data-testid="stHorizontalBlock"] {
        gap: 0.3rem !important;
        overflow-x: auto;
        flex-wrap: nowrap !important;
    }

    /* 3. TAILLES SPÉCIFIQUES MOBILE */
    @media (max-width: 768px) {
        /* On réduit la taille de base de TOUTE la page */
        html { font-size: 13px; }
        
        /* On réduit la largeur minimum des jours pour en voir + */
        div[data-testid="column"] { min-width: 110px !important; }
        
        /* On réduit drastiquement les boutons */
        .stButton button {
            padding: 0px 5px !important;
            height: 28px !important;
            min-height: 28px !important;
            line-height: 1 !important;
        }

        /* On réduit les titres h3 (Lun 4...) */
        h3 { font-size: 1rem !important; margin: 0 !important; }
        
        /* On réduit l'espace dans les cadres d'événements */
        div[data-testid="stVerticalBlockBorderWrapper"] > div {
            padding: 0.3rem !important;
            gap: 0.1rem !important;
        }
        
        /* On cache les labels trop longs ou on les réduit */
        .stCaption { font-size: 0.7rem !important; }
    }
    </style>
""", unsafe_allow_html=True)

st.title("📅 Planning")

# --- NAVIGATION ---
if "week_start" not in st.session_state:
    st.session_state.week_start = date.today() - timedelta(days=date.today().weekday())

# On utilise des colonnes très serrées pour les flèches
c_prev, c_center, c_next = st.columns([0.4, 2, 0.4], vertical_alignment="center")

with c_prev:
    if st.button("⬅️", key="prev"):
        st.session_state.week_start -= timedelta(days=7)
        st.rerun()

with c_center:
    start, end = st.session_state.week_start, st.session_state.week_start + timedelta(days=6)
    st.markdown(f"<p style='text-align: center; font-size: 0.9rem; margin:0;'>{start.strftime('%d/%m')} - {end.strftime('%d/%m')}</p>", unsafe_allow_html=True)
    if st.button("Aujourd'hui", use_container_width=True):
        st.session_state.week_start = date.today() - timedelta(days=date.today().weekday())
        st.rerun()

with c_next:
    if st.button("➡️", key="next"):
        st.session_state.week_start += timedelta(days=7)
        st.rerun()

st.divider()

# --- GRILLE DE 7 JOURS ---
monday = st.session_state.week_start
events = db.get_calendar(monday.isoformat(), (monday + timedelta(days=6)).isoformat())
jours_fr = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]

cols = st.columns(7)

for i in range(7):
    current_day = monday + timedelta(days=i)
    with cols[i]:
        is_today = current_day == date.today()
        # Titre de jour très compact
        label = f"{jours_fr[i]} {current_day.day}"
        if is_today:
            st.markdown(f"**:red[{label}]**")
        else:
            st.markdown(f"**{label}**")
        
        day_events = [e for e in events if e['event_date'] == current_day.isoformat()]
        
        for ev in day_events:
            with st.container(border=True):
                # Texte compacté avec .strip()
                st.markdown(f"<div style='font-size:0.85rem; line-height:1.1; font-weight:bold;'>{ev['event_name'].strip()}</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='font-size:0.75rem;'>🕒 {ev['start_time'][:5]}</div>", unsafe_allow_html=True)
                
                if st.button("🗑️", key=f"del_{ev['calendar_id']}", use_container_width=True):
                    db.remove_calendar(ev['calendar_id'])
                    st.rerun()