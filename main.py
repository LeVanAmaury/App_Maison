import streamlit as st
from src.database import FamilyDB

MEMBRES = ["Amaury", "Thais", "Corentin", "Maman", "Papoune"]

if "user" not in st.session_state:
    st.title("🏠 Bienvenue dans la Maison")
    st.write("Veuillez vous identifier pour accéder au hub familial.")
    
    user_choice = st.selectbox("Qui es-tu ?", [""] + MEMBRES)
    
    if user_choice != "":
        st.session_state["user"] = user_choice
        st.success(f"Salut {user_choice} ! Chargement...")
        st.rerun()
    else:
        st.stop()

st.sidebar.write(f"Connecté en tant que : **{st.session_state['user']}**")
if st.sidebar.button("Se déconnecter"):
    del st.session_state["user"]
    st.rerun()

dashboard_page = st.Page("views/dashboard.py", title="Tableau de bord", icon="📊", default=True)
tasks_page = st.Page("views/tasks.py", title="Tâches", icon="📝")
shopping_page = st.Page("views/shopping.py", title="Liste de courses", icon="🛒")
birthdays_page = st.Page("views/birthdays.py", title="Annviversaires", icon="🎂")
tv_page = st.Page("views/tv.py", title="Programme TV", icon="📺")
upgrade_page = st.Page("views/upgrades.py", title="Améliorations", icon="🆙")
menu_page = st.Page("views/menu.py", title="Menu", icon="🍛")
douches_page = st.Page("views/douches.py", title="Douches", icon='🚿')


pg = st.navigation([dashboard_page, tasks_page, shopping_page, birthdays_page, tv_page, upgrade_page, menu_page, douches_page])
pg.run()