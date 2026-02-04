import streamlit as st
from datetime import datetime, date, timedelta
from src.database import get_db

st.set_page_config(layout="wide")
st.title("📅 Planning Familial")
db = get_db()

# --- 1. CSS RESPONSIVE (DÉTECTION DE LA TAILLE D'ÉCRAN) ---
# Ce bloc réduit tout automatiquement sur petit écran
st.markdown("""
    <style>
    /* 1. Gestion du défilement horizontal */
    div[data-testid="stHorizontalBlock"] {
        overflow-x: auto;
        flex-wrap: nowrap !important;
        gap: 5px; /* On réduit l'espace entre les jours */
    }

    /* 2. Taille par défaut des colonnes */
    div[data-testid="column"] {
        min-width: 200px;
    }

    /* 3. ADAPTATION MOBILE (Écrans < 768px) */
    @media (max-width: 768px) {
        /* On réduit la largeur des colonnes jours */
        div[data-testid="column"] { min-width: 140px !important; }
        
        /* On réduit les titres (Lun 4, Mar 5...) */
        .stMarkdown h3 { font-size: 1.1rem !important; margin-bottom: 0 !important; }
        .stMarkdown h4 { font-size: 0.9rem !important; }
        
        /* On réduit la taille des boutons (Flèches et Supprimer) */
        button { 
            padding: 2px 5px !important; 
            min-height: 30px !important; 
            font-size: 0.8rem !important; 
        }
        
        /* On compacte les cartes d'événements */
        div[data-testid="stExpander"], div[data-testid="stForm"] { padding: 0.5rem !important; }
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. GESTION DE LA NAVIGATION ---
if "week_start" not in st.session_state:
    today = date.today()
    st.session_state.week_start = today - timedelta(days=today.weekday())

# Alignement vertical centré
col_prev, col_center, col_next = st.columns([0.5, 3, 0.5], vertical_alignment="center")

with col_prev:
    if st.button("⬅️", key="prev_week", use_container_width=True):
        st.session_state.week_start -= timedelta(days=7)
        st.rerun()

with col_center:
    start = st.session_state.week_start
    end = start + timedelta(days=6)
    st.markdown(f"<h4 style='text-align: center; margin: 0;'>{start.strftime('%d/%m')} au {end.strftime('%d/%m')}</h4>", unsafe_allow_html=True)
    if st.button("Aujourd'hui", use_container_width=True):
        st.session_state.week_start = date.today() - timedelta(days=date.today().weekday())
        st.rerun()

with col_next:
    if st.button("➡️", key="next_week", use_container_width=True):
        st.session_state.week_start += timedelta(days=7)
        st.rerun()

# --- 3. FORMULAIRE D'AJOUT COMPACT ---
with st.expander("➕ Ajouter"):
    with st.form("add_event_form", clear_on_submit=True):
        name = st.text_input("Quoi ?", placeholder="Concert...")
        e_date = st.date_input("Le jour", value=date.today())
        c1, c2 = st.columns(2)
        with c1: t_start = st.time_input("Début", value=datetime.strptime("18:00", "%H:%M").time())
        with c2: t_end = st.time_input("Fin", value=datetime.strptime("20:00", "%H:%M").time())
        
        member = st.session_state.get('user', 'Anonyme')
        if st.form_submit_button("Ajouter", use_container_width=True):
            if name:
                db.add_calendar(name.strip(), e_date.isoformat(), t_start.isoformat(), t_end.isoformat(), member)
                st.rerun()

st.divider()

# --- 4. AFFICHAGE DE LA GRILLE ---
monday = st.session_state.week_start
events = db.get_calendar(monday.isoformat(), (monday + timedelta(days=6)).isoformat())
jours_fr = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]

cols = st.columns(7)

for i in range(7):
    current_day = monday + timedelta(days=i)
    with cols[i]:
        is_today = current_day == date.today()
        # On utilise une taille de titre plus petite pour mobile via le CSS
        if is_today:
            st.markdown(f"### :red[{jours_fr[i]} {current_day.day}]")
        else:
            st.markdown(f"### {jours_fr[i]} {current_day.day}")
        
        day_events = [e for e in events if e['event_date'] == current_day.isoformat()]
        
        for ev in day_events:
            with st.container(border=True):
                # .strip() pour éviter le bug des étoiles **
                titre = ev['event_name'].strip()
                st.markdown(f"**{titre}**")
                
                # Heure et membre en plus petit
                debut = ev['start_time'][:5]
                st.caption(f"{debut} | {ev['member']}")
                
                # Bouton de suppression compact
                if st.button("🗑️", key=f"del_{ev['calendar_id']}", use_container_width=True):
                    db.remove_calendar(ev['calendar_id'])
                    st.rerun()