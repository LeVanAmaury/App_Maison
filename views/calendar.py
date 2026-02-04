import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime, timedelta

def show_calendar():
    # 1. Configuration de la page et style CSS pour Mobile
    # On injecte du CSS pour maximiser l'espace et éviter le "glissement" latéral sur mobile [4, 3, 5]
    st.markdown("""
        <style>
            /* Supprime les marges excessives en haut de page */
            [data-testid="block-container"] {
                padding-top: 1rem;
                padding-bottom: 1rem;
                padding-left: 0.5rem;
                padding-right: 0.5rem;
            }
            /* Empêche le scroll horizontal parasite sur smartphone */
            section[tabindex="0"] {
                overflow-x: hidden;
            }
            /* Style des boutons de navigation */
           .stButton>button {
                width: 100%;
                border-radius: 10px;
                height: 3em;
                background-color: #f0f2f6;
            }
            /* Rend le titre du calendrier plus lisible */
           .fc-toolbar-title {
                font-size: 1.2rem!important;
                font-weight: bold;
            }
        </style>
    """, unsafe_allow_html=True)

    # 2. Gestion de l'état (Session State) pour la navigation 
    if 'current_date' not in st.session_state:
        st.session_state.current_date = datetime.now()

    # Fonctions de navigation
    def prev_week():
        st.session_state.current_date -= timedelta(days=7)

    def next_week():
        st.session_state.current_date += timedelta(days=7)

    def go_today():
        st.session_state.current_date = datetime.now()

    # 3. Interface de Navigation (Barre de contrôle compacte)
    col1, col2, col3, col4 = st.columns([1, 1, 2, 1])
    with col1:
        st.button("⬅️", on_click=prev_week, help="Semaine précédente")
    with col2:
        st.button("🎯", on_click=go_today, help="Aujourd'hui")
    with col4:
        st.button("➡️", on_click=next_week, help="Semaine suivante")
    with col3:
        # Affiche le mois/année courant de manière élégante
        st.markdown(f"<div style='text-align:center; padding-top:10px;'><b>{st.session_state.current_date.strftime('%B %Y')}</b></div>", unsafe_allow_html=True)

    # 4. Configuration des données (Exemple d'événements)
    # Dans votre projet, remplacez ceci par vos données de base de données [8, 9]
    calendar_events =

    # 5. Options du Calendrier optimisées pour "Zéro Scroll" [10, 2, 11]
    calendar_options = {
        "initialView": "timeGridWeek", # Vue hebdomadaire avec heures
        "initialDate": st.session_state.current_date.strftime("%Y-%m-%d"),
        "headerToolbar": False, # On cache la toolbar native pour utiliser nos boutons propres
        "allDaySlot": False, # Gain de place vertical
        "slotMinTime": "07:00:00", # On commence à 7h pour éviter le vide de la nuit 
        "slotMaxTime": "22:00:00", # On finit à 22h
        "height": "auto", # S'adapte au contenu
        "navLinks": True,
        "selectable": True,
        "firstDay": 1, # Commence la semaine le Lundi
        "locale": 'fr', # Français
        "slotDuration": "00:30:00",
        "eventClick": "js:function(info) { alert('Event: ' + info.event.title); }",
    }

    # 6. Rendu du composant [1, 12]
    state = calendar(
        events=calendar_events,
        options=calendar_options,
        custom_css="""
           .fc-v-event { border-radius: 5px; border: none; padding: 2px; }
           .fc-timegrid-slot { height: 3em!important; } /* Ajuste la hauteur des cases pour le tactile */
        """,
        key='family_calendar',
    )

    # Gestion des interactions (clic sur événement ou date)
    if state.get("callback") == "dateClick":
        st.info(f"Date cliquée : {state['dateClick']['date']}")
    if state.get("callback") == "eventClick":
        st.success(f"Événement sélectionné : {state['eventClick']['event']['title']}")

if __name__ == "__main__":
    show_calendar()