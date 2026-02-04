import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime, timedelta
from src.database import get_db

# 1. Fenêtre pour ajouter un événement [1, 2]
@st.dialog("Ajouter un événement")
def add_event_dialog(selected_date=None):
    db = get_db()
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

# 2. Fenêtre pour supprimer [2]
@st.dialog("Supprimer l'événement")
def event_details_dialog(event_info):
    db = get_db()
    st.write(f"Supprimer l'événement : **{event_info['title']}**?")
    if st.button("🗑️ Confirmer", variant="primary", use_container_width=True):
        db.remove_calendar(event_info['id'])
        st.rerun()

def show_calendar():
    db = get_db()

    # --- CSS ULTRA-PRECIS POUR L'ALIGNEMENT --- [3, 4, 5]
    st.markdown("""
        <style>
            /* Force l'alignement horizontal strict pour la barre de navigation sur MOBILE */
            div:has(button[key*="nav_"]) {
                display: flex!important;
                flex-direction: row!important;
                flex-wrap: nowrap!important;
                align-items: center!important;
                justify-content: center!important;
            }
            
            /* Style des boutons ronds de navigation */
            div:has(button[key*="nav_"]) button {
                border-radius: 50%!important;
                width: 42px!important;
                height: 42px!important;
                padding: 0px!important;
                line-height: 1!important;
            }

            /* Supprime les marges du titre pour un alignement vertical parfait sur PC */
           .month-title {
                margin: 0!important;
                padding: 0!important;
                text-align: center;
                font-weight: bold;
                font-size: 1.2rem;
                min-width: 130px;
            }

            /* Nettoyage général mobile */
            [data-testid="block-container"] { padding-top: 1rem; padding-left: 0.5rem; padding-right: 0.5rem; }
            section[tabindex="0"] { overflow-x: hidden; }
        </style>
    """, unsafe_allow_html=True)

    if 'current_date' not in st.session_state:
        st.session_state.current_date = datetime.now()

    def change_week(delta):
        st.session_state.current_date += timedelta(days=delta)

    # --- BARRE DE NAVIGATION ALIGNÉE (PC & MOBILE) ---
    # L'option vertical_alignment="center" règle votre problème d'alignement vertical sur PC
    nav_col1, nav_col2, nav_col3 = st.columns([1, 3, 1], vertical_alignment="center")
    
    with nav_col1:
        st.button("◀", on_click=change_week, args=(-7,), key="nav_prev")
    
    with nav_col2:
        month_str = st.session_state.current_date.strftime('%b %Y')
        st.markdown(f"<p class='month-title'>{month_str}</p>", unsafe_allow_html=True)
    
    with nav_col3:
        st.button("▶", on_click=change_week, args=(7,), key="nav_next")

    # Données
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

    # Options Calendrier
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
        "nowIndicator": True,
    }

    state = calendar(
        events=formatted_events,
        options=calendar_options,
        custom_css=".fc-event { border-radius: 6px; padding: 2px; }",
        key=f"cal_{st.session_state.current_date.strftime('%Y%W')}"
    )

    st.button("➕ Ajouter un événement", on_click=add_event_dialog, use_container_width=True)

    if state.get("callback") == "dateClick":
        add_event_dialog(state["dateClick"]["date"])
    if state.get("callback") == "eventClick":
        event_details_dialog(state["eventClick"]["event"])

if __name__ == "__main__":
    show_calendar()