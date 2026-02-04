import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime, timedelta
from src.database import get_db

def show_calendar():
    # 1. Initialisation de la base de données
    db = get_db()

    # 2. Injection CSS pour l'ergonomie Mobile (Zéro scroll horizontal + compacité) [1, 2]
    st.markdown("""
        <style>
            /* Supprime les marges inutiles pour gagner de l'espace sur petit écran */
            [data-testid="block-container"] {
                padding-top: 1rem;
                padding-bottom: 0rem;
                padding-left: 0.5rem;
                padding-right: 0.5rem;
            }
            /* Bloque le glissement latéral sur iPhone/Android */
            section[tabindex="0"] {
                overflow-x: hidden;
            }
           .stButton>button {
                border-radius: 8px;
                height: 3em;
            }
        </style>
    """, unsafe_allow_html=True)

    # 3. Gestion de la navigation par Semaine 
    if 'current_date' not in st.session_state:
        st.session_state.current_date = datetime.now()

    def change_week(delta_days):
        st.session_state.current_date += timedelta(days=delta_days)

    # Calcul de la plage de dates pour la requête Supabase
    start_of_week = st.session_state.current_date - timedelta(days=st.session_state.current_date.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    # 4. Barre de Navigation (Haut de page)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.button("⬅️", on_click=change_week, args=(-7,), use_container_width=True)
    with col3:
        st.button("➡️", on_click=change_week, args=(7,), use_container_width=True)
    with col2:
        month_label = st.session_state.current_date.strftime("%B %Y")
        st.markdown(f"<h3 style='text-align: center; margin-top: 0;'>{month_label}</h3>", unsafe_allow_html=True)

    # 5. Récupération et formatage des données Supabase [3, 4]
    # On récupère les événements entre le lundi et le dimanche de la semaine sélectionnée
    raw_events = db.get_calendar(start_of_week.strftime("%Y-%m-%d"), end_of_week.strftime("%Y-%m-%d"))
    
    formatted_events = []
    for ev in raw_events:
        # Transformation pour FullCalendar : il faut des clés 'title', 'start' et 'end'
        formatted_events.append({
            "id": ev.get("calendar_id"),
            "title": f"{ev.get('event_name')} ({ev.get('member')})",
            "start": f"{ev.get('event_date')}T{ev.get('start_time')}",
            "end": f"{ev.get('event_date')}T{ev.get('end_time')}",
            "backgroundColor": "#3D9DF3" if ev.get('member') == "Papa" else "#FF6C6C",
        })

    # 6. Options du Calendrier optimisées pour Mobile [3, 5, 6]
    calendar_options = {
        "initialView": "timeGridWeek", # Vue 1 semaine avec les heures
        "initialDate": st.session_state.current_date.strftime("%Y-%m-%d"),
        "headerToolbar": False, # On utilise nos propres boutons Streamlit pour plus de propreté
        "firstDay": 1, # La semaine commence le lundi
        "slotMinTime": "07:30:00", # Réduit la hauteur en masquant la nuit (Moins de scroll!)
        "slotMaxTime": "21:30:00",
        "allDaySlot": False,
        "locale": "fr",
        "height": "auto", # Le calendrier s'adapte à l'écran sans créer de double barre de défilement
        "nowIndicator": True,
        "editable": True,
        "selectable": True,
    }

    # 7. Rendu du composant
    # Le 'key' change selon la date pour forcer le rafraîchissement visuel lors de la navigation
    calendar_key = f"calendar_{st.session_state.current_date.strftime('%Y%W')}"
    
    cal_data = calendar(
        events=formatted_events,
        options=calendar_options,
        custom_css="""
           .fc-event-title { font-weight: 600; font-size: 0.85rem; }
           .fc-timegrid-slot { height: 2.5em!important; } /* Case plus grande pour le tactile */
        """,
        key=calendar_key
    )

    # Interaction : si l'utilisateur clique sur un créneau vide
    if cal_data.get("callback") == "dateClick":
        st.session_state.selected_slot = cal_data["dateClick"]["date"]
        st.toast(f"Créneau sélectionné : {st.session_state.selected_slot}")

# Exécution directe si le fichier est appelé
if __name__ == "__main__":
    show_calendar()