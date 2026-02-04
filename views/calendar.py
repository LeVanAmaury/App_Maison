import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime, timedelta
from src.database import get_db

# 1. Fenêtre pour ajouter un événement (Modal) [13, 14]
@st.dialog("Ajouter un événement")
def add_event_dialog(selected_date=None):
    db = get_db()
    # Gestion du format de date ISO de FullCalendar
    try:
        default_date = datetime.fromisoformat(selected_date.replace('Z', '')) if selected_date else datetime.now()
    except:
        default_date = datetime.now()
    
    with st.form("form_add_event", clear_on_submit=True):
        name = st.text_input("Nom de l'événement", placeholder="Ex: Dentiste, Foot...")
        member = st.selectbox("Qui?", ["Papa", "Maman", "Enfants"])
        date = st.date_input("Date", value=default_date)
        
        c1, c2 = st.columns(2)
        with c1: start = st.time_input("Début", value=default_date.time())
        with c2: end = st.time_input("Fin", value=(default_date + timedelta(hours=1)).time())
            
        if st.form_submit_button("Enregistrer", use_container_width=True):
            if name:
                db.add_calendar(name, str(date), str(start), str(end), member)
                st.rerun()

# 2. Fenêtre pour supprimer un événement [14]
@st.dialog("Supprimer l'événement")
def event_details_dialog(event_info):
    db = get_db()
    st.warning(f"Supprimer : {event_info['title']}?")
    if st.button("🗑️ Confirmer la suppression", variant="primary", use_container_width=True):
        db.remove_calendar(event_info['id'])
        st.rerun()

def show_calendar():
    db = get_db()

    # --- CSS HACK : FORCE LE LAYOUT HORIZONTAL SUR MOBILE --- [7, 8, 12]
    st.markdown("""
        <style>
            /* Force les colonnes à rester sur une seule ligne (Pas d'empilement mobile) */
            {
                display: flex!important;
                flex-direction: row!important;
                flex-wrap: nowrap!important;
                align-items: center!important;
                gap: 0.5rem!important;
            }
            /* Style des boutons de navigation arrondis */
            button {
                border-radius: 50%!important;
                width: 45px!important;
                height: 45px!important;
                padding: 0px!important;
                margin: auto!important;
            }
            /* Supprime les marges de page pour mobile */
            [data-testid="block-container"] { padding-top: 1rem; padding-left: 0.5rem; padding-right: 0.5rem; }
            section[tabindex="0"] { overflow-x: hidden; }
           .month-label { text-align: center; font-weight: bold; font-size: 1.1rem; margin: 0; }
        </style>
    """, unsafe_allow_html=True)

    if 'current_date' not in st.session_state:
        st.session_state.current_date = datetime.now()

    def change_week(delta):
        st.session_state.current_date += timedelta(days=delta)

    # --- BARRE DE NAVIGATION (Garantie à 3 colonnes horizontales) ---
    nav_col1, nav_col2, nav_col3 = st.columns([1, 4, 1])
    with nav_col1:
        st.button("◀", on_click=change_week, args=(-7,), key="btn_prev")
    with nav_col2:
        month_str = st.session_state.current_date.strftime('%B %Y')
        st.markdown(f"<p class='month-label'>{month_str}</p>", unsafe_allow_html=True)
    with nav_col3:
        st.button("▶", on_click=change_week, args=(7,), key="btn_next")

    # Données de la semaine
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
        })

    # Options Calendrier
    calendar_options = {
        "initialView": "timeGridWeek",
        "initialDate": st.session_state.current_date.strftime("%Y-%m-%d"),
        "headerToolbar": False,
        "firstDay": 1,
        "slotMinTime": "06:00:00", # Moins de scroll en cachant la nuit
        "slotMaxTime": "23:30:00",
        "allDaySlot": False,
        "locale": "fr",
        "height": "auto",
        "selectable": True,
    }

    # Affichage du calendrier
    state = calendar(
        events=formatted_events,
        options=calendar_options,
        custom_css=".fc-timegrid-slot { height: 2.8em!important; }",
        key=f"cal_{st.session_state.current_date.strftime('%Y%W')}"
    )

    # Bouton d'ajout flottant
    st.button("➕ Ajouter un événement", on_click=add_event_dialog, use_container_width=True)

    # Logique de clic
    if state.get("callback") == "dateClick":
        add_event_dialog(state["dateClick"]["date"])
    if state.get("callback") == "eventClick":
        event_details_dialog(state["eventClick"]["event"])

if __name__ == "__main__":
    show_calendar()