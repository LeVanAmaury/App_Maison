import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime, timedelta
from src.database import get_db

# 1. Fonction pour ajouter un événement (Fenêtre modale) 
@st.dialog("Ajouter un événement")
def add_event_dialog(selected_date=None):
    db = get_db()
    
    # Pré-remplissage si une date a été cliquée
    default_date = datetime.fromisoformat(selected_date) if selected_date else datetime.now()
    
    with st.form("form_add_event", clear_on_submit=True):
        name = st.text_input("Nom de l'événement", placeholder="Ex: Dentiste, Sport...")
        member = st.selectbox("Qui?", ["Papa", "Maman", "Enfant 1", "Enfant 2"])
        date = st.date_input("Date", value=default_date)
        
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            start = st.time_input("Début", value=default_date.time())
        with col_t2:
            end = st.time_input("Fin", value=(default_date + timedelta(hours=1)).time())
            
        if st.form_submit_button("Enregistrer", use_container_width=True):
            if name:
                db.add_calendar(name, str(date), str(start), str(end), member)
                st.success("Ajouté!")
                st.rerun()
            else:
                st.error("Le nom est obligatoire")

# 2. Fonction pour supprimer un événement (Confirmation) [2]
@st.dialog("Détails de l'événement")
def event_details_dialog(event_info):
    db = get_db()
    event_id = event_info['id']
    title = event_info['title']
    
    st.write(f"Souhaitez-vous supprimer cet événement?")
    st.info(f"**{title}**")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("❌ Supprimer", variant="primary", use_container_width=True):
            db.remove_calendar(event_id)
            st.rerun()
    with col2:
        if st.button("Annuler", use_container_width=True):
            st.rerun()

def show_calendar():
    db = get_db()

    # Style CSS optimisé [3, 4]
    st.markdown("""
        <style>
            [data-testid="block-container"] { padding-top: 1rem; padding-left: 0.5rem; padding-right: 0.5rem; }
            section[tabindex="0"] { overflow-x: hidden; }
           .stButton>button { border-radius: 12px; height: 3em; }
        </style>
    """, unsafe_allow_html=True)

    # État de navigation
    if 'current_date' not in st.session_state:
        st.session_state.current_date = datetime.now()

    def change_week(delta):
        st.session_state.current_date += timedelta(days=delta)

    # Barre de navigation
    c1, c2, c3 = st.columns([1, 2, 1])
    with c1: st.button("⬅️", on_click=change_week, args=(-7,), use_container_width=True)
    with c3: st.button("➡️", on_click=change_week, args=(7,), use_container_width=True)
    with c2:
        st.markdown(f"<h3 style='text-align: center; margin-top: 5px;'>{st.session_state.current_date.strftime('%b %Y')}</h3>", unsafe_allow_html=True)

    # Récupération des données
    start_w = st.session_state.current_date - timedelta(days=st.session_state.current_date.weekday())
    end_w = start_w + timedelta(days=6)
    raw_events = db.get_calendar(start_w.strftime("%Y-%m-%d"), end_w.strftime("%Y-%m-%d"))
    
    formatted_events = []
    for ev in raw_events:
        formatted_events.append({
            "id": ev.get("calendar_id"),
            "title": f"{ev.get('event_name')} ({ev.get('member')})",
            "start": f"{ev.get('event_date')}T{ev.get('start_time')}",
            "end": f"{ev.get('event_date')}T{ev.get('end_time')}",
            "backgroundColor": "#3D9DF3" if ev.get('member') == "Papa" else "#FF6C6C",
            "borderColor": "transparent"
        })

    # Options du calendrier [5, 6, 7]
    calendar_options = {
        "initialView": "timeGridWeek",
        "initialDate": st.session_state.current_date.strftime("%Y-%m-%d"),
        "headerToolbar": False,
        "firstDay": 1,
        "slotMinTime": "07:00:00",
        "slotMaxTime": "22:30:00",
        "allDaySlot": False,
        "locale": "fr",
        "height": "auto",
        "selectable": True,
    }

    # Affichage du calendrier
    state = calendar(
        events=formatted_events,
        options=calendar_options,
        custom_css=".fc-event { border-radius: 6px; padding: 2px; }",
        key=f"cal_{st.session_state.current_date.strftime('%Y%W')}"
    )

    # Bouton flottant (optionnel) ou gestion des clics
    st.button("➕ Ajouter un événement", on_click=add_event_dialog, use_container_width=True)

    # Logique des interactions [8, 9]
    if state.get("callback") == "dateClick":
        add_event_dialog(state["dateClick"]["date"])
    
    if state.get("callback") == "eventClick":
        event_info = state["eventClick"]["event"]
        event_details_dialog(event_info)

if __name__ == "__main__":
    show_calendar()