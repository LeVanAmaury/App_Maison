import streamlit as st
from src.styles import inject_custom_css

# --- CONFIGURATION ---
st.set_page_config(
    page_title="App Maison - Hub Familial",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom CSS
inject_custom_css()

MEMBRES = ["Amaury", "Thais", "Corentin", "Maman", "Papoune"]

# --- LOGIN ---
if "user" not in st.session_state:
    st.title("🏠 Bienvenue dans la Maison")
    st.write("Veuillez vous identifier pour accéder au hub familial.")
    
    with st.container(border=True):
        user_choice = st.selectbox("Qui es-tu ?", [""] + MEMBRES)
        if user_choice != "":
            st.session_state["user"] = user_choice
            st.success(f"Salut {user_choice} ! Chargement du hub...")
            st.rerun()
    st.stop()

# --- SIDEBAR & NAV ---
st.sidebar.markdown(f"### 👤 {st.session_state['user']}")

dashboard_page = st.Page("views/dashboard.py", title="Tableau de bord", icon="📊", default=True)
tasks_page = st.Page("views/tasks.py", title="Tâches", icon="📝")
shopping_page = st.Page("views/shopping.py", title="Liste de courses", icon="🛒")
birthdays_page = st.Page("views/birthdays.py", title="Anniversaires", icon="🎂")
tv_page = st.Page("views/tv.py", title="Programme TV", icon="📺")
upgrade_page = st.Page("views/upgrades.py", title="Améliorations", icon="🆙")
menu_page = st.Page("views/menu.py", title="Menu", icon="🍛")
douches_page = st.Page("views/douches.py", title="Douches", icon='🚿')
calendar_page = st.Page('views/calendar.py', title='Planning', icon='📅')

pg = st.navigation({
    "Principal": [dashboard_page, calendar_page],
    "Gestion": [tasks_page, shopping_page, menu_page, douches_page],
    "Loisirs & Projets": [tv_page, birthdays_page, upgrade_page]
})

# Logout button at the bottom of sidebar
if st.sidebar.button("🚪 Se déconnecter", use_container_width=True):
    del st.session_state["user"]
    st.rerun()

pg.run()