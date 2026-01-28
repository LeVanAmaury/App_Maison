import streamlit as st
from src.database import FamilyDB

st.set_page_config(page_title="Famille", page_icon="🏠", layout="wide")

FAMILY_MEMBERS = ["Amaury", "Thais", "Corentin", "Maman", "Papoune"]

def login():
    if "user" not in st.session_state:
        st.sidebar.title("Connexion")
        user = st.sidebar.selectbox("Qui es-tu ?", [""] + FAMILY_MEMBERS)

        if user != "":
            st.session_state["user"] = user
            st.sidebar.success(f"Salut {user} !")
            st.rerun()
        else:
            st.warning("Choisis ton nom pour entrer dans la maison")
            st.stop()
    
    else:
        st.sidebar.write(f"Connecté : **{st.session_state['user']}**")
        if st.sidebar.button("Déconnexion"):
            del st.session_state["user"]
            st.rerun()

dashboard_page = st.Page("views/dashboard.py", title="Tableau de bord", icon="📊", default=True)
tasks_page = st.Page("views/tasks.py", title="Tâches", icon="📝")
shopping_page = st.Page("views/shopping.py", title="Liste de courses", icon="🛒")
birthdays_page = st.Page("views/birthdays.py", title="Annviversaires", icon="🎂")
tv_page = st.Page("views/tv.py", title="Programme TV", icon="📺")
upgrade_page = st.Page("views/upgrades.py", title="Améliorations", icon="🆙")
menu_page = st.Page("views/menu.py", title="Menu", icon="🍛")


pg = st.navigation([dashboard_page, tasks_page, shopping_page, birthdays_page, tv_page, upgrade_page, menu_page])
pg.run()