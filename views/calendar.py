import streamlit as st
from datetime import datetime, date, timedelta
from src.database import get_db

st.set_page_config(layout="wide")
db = get_db()

# --- 1. CSS "FORCE BRUTE" POUR UN LOOK MOBILE COMPACT ---
st.markdown("""
    <style>
    /* On réduit les marges énormes de Streamlit en haut de page */
    .block-container {
        padding-top: 1rem !important;
        padding-left: 0.3rem !important;
        padding-right: 0.3rem !important;
    }

    /* On force les colonnes à rester sur une SEULE ligne (pas d'empilement) */
    [data-testid="stHorizontalBlock"] {
        flex-direction: row !important;
        overflow-x: auto !important; /* Défilement horizontal fluide */
        flex-wrap: nowrap !important;
        gap: 5px !important;
    }

    /* On définit une largeur fixe très étroite pour chaque colonne jour */
    [data-testid="column"] {
        min-width: 110px !important; /* Taille parfaite pour mobile */
        flex: 0 0 auto !important;
        padding: 0 !important;
    }

    /* RÉDUCTION DES TAILLES DE TEXTE SUR MOBILE */
    @media (max-width: 768px) {
        h1 { font-size: 1.2rem !important; margin-bottom: 0.5rem !important; }
        h3 { font-size: 0.85rem !important; margin: 0 !important; } /* Dates (Lun 2, etc.) */
        p, .stMarkdown { font-size: 0.75rem !important; }
        
        /* Boutons miniatures (Navigation et Suppression) */
        .stButton button {
            padding: 2px 4px !important;
            height: 26px !important;
            min-height: 26px !important;
            font-size: 0.7rem !important;
        }

        /* On réduit l'espace interne des cadres d'événements */
        [data-testid="stVerticalBlockBorderWrapper"] > div {
            padding: 4px !important;
            gap: 2px !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

st.title("📅 Planning")

# --- 2. NAVIGATION MINIATURE ---
if "week_start" not in st.session_state:
    st.session_state.week_start = date.today() - timedelta(days=date.today().weekday())

# Ratios très serrés pour que tout tienne sur une ligne
c1, c2, c3 = st.columns([0.4, 2, 0.4], vertical_alignment="center")
with c1:
    if st.button("⬅️", key="p"):
        st.session_state.week_start -= timedelta(days=7); st.rerun()
with c3:
    if st.button("➡️", key="n"):
        st.session_state.week_start += timedelta(days=7); st.rerun()
with c2:
    s, e = st.session_state.week_start, st.session_state.week_start + timedelta(days=6)
    st.markdown(f"<p style='text-align:center; margin:0; font-weight:bold;'>{s.strftime('%d/%m')} au {e.strftime('%d/%m')}</p>", unsafe_allow_html=True)

if st.button("Aujourd'hui", use_container_width=True):
    st.session_state.week_start = date.today() - timedelta(days=date.today().weekday()); st.rerun()

st.divider()

# --- 3. LA GRILLE DE SEMAINE ---
monday = st.session_state.week_start
events = db.get_calendar(monday.isoformat(), (monday + timedelta(days=6)).isoformat())
jours_fr = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]

cols = st.columns(7)

for i in range(7):
    day = monday + timedelta(days=i)
    with cols[i]:
        # En-tête compact
        is_today = day == date.today()
        label = f"{jours_fr[i]} {day.day}"
        if is_today:
            st.markdown(f"### :red[{label}]")
        else:
            st.markdown(f"### {label}")
        
        day_events = [ev for ev in events if ev['event_date'] == day.isoformat()]
        
        for ev in day_events:
            # On utilise une "carte" très serrée
            with st.container(border=True):
                # Titre en gras et petit
                t = ev['event_name'].strip()
                st.markdown(f"<div style='font-size:0.8rem; font-weight:bold; line-height:1;'>{t}</div>", unsafe_allow_html=True)
                
                # Heures et Membre en minuscule
                st.markdown(f"<div style='font-size:0.65rem; color:gray;'>🕒 {ev['start_time'][:5]} | {ev['member']}</div>", unsafe_allow_html=True)
                
                # Bouton de suppression discret
                if st.button("🗑️", key=f"d_{ev['calendar_id']}", use_container_width=True):
                    db.remove_calendar(ev['calendar_id'])
                    st.rerun()