import streamlit as st
from datetime import datetime, date, timedelta
from src.database import get_db

st.set_page_config(layout="wide")
st.title("📅 Planning Familial")
db = get_db()

# --- 1. CSS POUR LE SCROLL HORIZONTAL (Version Mobile) ---
# Ce style force les 7 colonnes à rester côte à côte sur mobile
st.markdown("""
    <style>
    div[data-testid="stHorizontalBlock"] {
        overflow-x: auto;
        flex-wrap: nowrap !important;
        gap: 10px;
        padding-bottom: 10px;
    }
    div[data-testid="column"] {
        min-width: 200px; /* Largeur de chaque jour sur mobile */
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. GESTION DE LA NAVIGATION ---
if "week_start" not in st.session_state:
    today = date.today()
    st.session_state.week_start = today - timedelta(days=today.weekday())

# Alignement vertical centre pour que flèches et texte soient sur la même ligne
col_prev, col_center, col_next = st.columns([1, 3, 1], vertical_alignment="center")

with col_prev:
    if st.button("⬅️", key="prev_week", use_container_width=True):
        st.session_state.week_start -= timedelta(days=7)
        st.rerun()

with col_center:
    start = st.session_state.week_start
    end = start + timedelta(days=6)
    # margin:0 pour supprimer l'espace vide au-dessus/en-dessous du titre
    st.markdown(f"<h4 style='text-align: center; margin: 0;'>Semaine du {start.strftime('%d/%m')} au {end.strftime('%d/%m')}</h4>", unsafe_allow_html=True)
    if st.button("Aujourd'hui", use_container_width=True):
        st.session_state.week_start = date.today() - timedelta(days=date.today().weekday())
        st.rerun()

with col_next:
    if st.button("➡️", key="next_week", use_container_width=True):
        st.session_state.week_start += timedelta(days=7)
        st.rerun()

# --- 3. FORMULAIRE D'AJOUT ---
with st.expander("➕ Ajouter un événement"):
    with st.form("add_event_form", clear_on_submit=True):
        name = st.text_input("Quoi ?", placeholder="Ex: Concert de Rock")
        e_date = st.date_input("Le jour", value=date.today())
        c1, c2 = st.columns(2)
        with c1:
            t_start = st.time_input("Début", value=datetime.strptime("18:00", "%H:%M").time())
        with c2:
            t_end = st.time_input("Fin", value=datetime.strptime("20:00", "%H:%M").time())
        
        member = st.session_state.get('user', 'Anonyme')
        if st.form_submit_button("Épingler au planning", use_container_width=True):
            if name:
                db.add_calendar(name.strip(), e_date.isoformat(), t_start.isoformat(), t_end.isoformat(), member)
                st.rerun()

st.divider()

# --- 4. AFFICHAGE DE LA GRILLE (7 COLONNES) ---
monday = st.session_state.week_start
events = db.get_calendar(monday.isoformat(), (monday + timedelta(days=6)).isoformat())
jours_fr = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]

cols = st.columns(7)

for i in range(7):
    current_day = monday + timedelta(days=i)
    with cols[i]:
        # Mise en évidence d'aujourd'hui
        is_today = current_day == date.today()
        if is_today:
            st.markdown(f"### :red[{jours_fr[i]} {current_day.day}]")
            st.caption("🔴 Aujourd'hui")
        else:
            st.markdown(f"### {jours_fr[i]} {current_day.day}")
        
        # Filtrage des événements
        day_events = [e for e in events if e['event_date'] == current_day.isoformat()]
        
        for ev in day_events:
            with st.container(border=True):
                # .strip() pour éviter le bug des étoiles **
                titre = ev['event_name'].strip()
                st.markdown(f"**{titre}**")
                
                debut = ev['start_time'][:5]
                fin = ev['end_time'][:5]
                st.caption(f"🕒 {debut} - {fin} | 👤 {ev['member']}")
                
                # Utilisation de calendar_id pour la suppression
                if st.button("🗑️", key=f"del_{ev['calendar_id']}", use_container_width=True):
                    db.remove_calendar(ev['calendar_id'])
                    st.rerun()