import streamlit as st
from datetime import datetime, date, timedelta
from src.database import get_db

st.title("📅 Planning Familial")
st.markdown("""
    <style>
    div[data-testid="stHorizontalBlock"] {
        overflow-x: auto;
        flex-wrap: nowrap !important;
    }
    div[data-testid="column"] {
        min-width: 150px; /* Taille minimum d'une case de jour sur mobile */
    }
    </style>
""", unsafe_allow_html=True)
db = get_db()

# --- 1. GESTION DE LA NAVIGATION ---
if "week_start" not in st.session_state:
    today = date.today()
    st.session_state.week_start = today - timedelta(days=today.weekday())

# Navigation compacte pour mobile
col_prev, col_next = st.columns(2)
with col_prev:
    if st.button("⬅️ Précédente", use_container_width=True):
        st.session_state.week_start -= timedelta(days=7)
        st.rerun()
with col_next:
    if st.button("Suivante ➡️", use_container_width=True):
        st.session_state.week_start += timedelta(days=7)
        st.rerun()

start = st.session_state.week_start
end = start + timedelta(days=6)
st.markdown(f"<h4 style='text-align: center;'>Semaine du {start.strftime('%d/%m')} au {end.strftime('%d/%m')}</h4>", unsafe_allow_html=True)

if st.button("🏠 Revenir à Aujourd'hui", use_container_width=True):
    st.session_state.week_start = date.today() - timedelta(days=date.today().weekday())
    st.rerun()

with st.expander("➕ Ajouter un événement"):
    with st.form("add_event_form", clear_on_submit=True):
        name = st.text_input("Quoi ?", placeholder="Ex: Concert de Rock")
        e_date = st.date_input("Le jour", value=date.today())
        c1, c2 = st.columns(2)
        with c1:
            t_start = st.time_input("Début", value=datetime.strptime("18:00", "%H:%M").time())
        with c2:
            t_end = st.time_input("Fin", value=datetime.strptime("20:00", "%H:%M").time())
        
        # On utilise l'utilisateur connecté automatiquement
        member = st.session_state.get('user', 'Anonyme')
        if st.form_submit_button("Ajouter au calendrier", use_container_width=True):
            if name:
                db.add_calendar(name.strip(), e_date.isoformat(), t_start.isoformat(), t_end.isoformat(), member)
                st.success("Ajouté !")
                st.rerun()

st.divider()

# --- 2. AFFICHAGE EN ONGLETS (Optimisé Mobile) ---
monday = st.session_state.week_start
events = db.get_calendar(monday.isoformat(), (monday + timedelta(days=6)).isoformat())

jours_fr = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
# On prépare les noms des onglets avec la date
tab_titles = []
for i in range(7):
    d = monday + timedelta(days=i)
    prefix = "🔴 " if d == date.today() else ""
    tab_titles.append(f"{prefix}{jours_fr[i]} {d.day}")

# Création des onglets
tabs = st.tabs(tab_titles)

for i, tab in enumerate(tabs):
    current_day = monday + timedelta(days=i)
    with tab:
        day_str = current_day.isoformat()
        day_events = [e for e in events if e['event_date'] == day_str]
        
        if not day_events:
            st.info("Rien de prévu pour ce jour.")
        else:
            for ev in day_events:
                with st.container(border=True):
                    # Nettoyage .strip() pour éviter le bug des étoiles **
                    titre = ev['event_name'].strip()
                    st.markdown(f"### {titre}")
                    
                    debut = ev['start_time'][:5]
                    fin = ev['end_time'][:5]
                    st.caption(f"🕒 {debut} - {fin} | 👤 {ev['member']}")
                    
                    # Bouton de suppression (uniquement si c'est l'auteur ou admin)
                    if st.button("🗑️ Supprimer", key=f"del_{ev['calendar_id']}", use_container_width=True):
                        db.remove_calendar(ev['calendar_id'])
                        st.rerun()