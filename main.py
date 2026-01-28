import streamlit as st
from src.database import FamilyDB

st.set_page_config(page_title="Famille", page_icon="🏠", layout="wide")

@st.cache_resource      # Pour ne pas recréer la connexion à chaque clic
def get_db():
    return FamilyDB()

db = get_db()

dashboard_page = st.Page("views/dashboard.py", title="Tableau de bord", icon="📊", default=True)
tasks_page = st.Page("views/tasks.py", title="Tâches", icon="📝")
shopping_page = st.Page("views/shopping.py", title="Liste de courses", icon="🛒")
birthdays_page = st.Page("views/birthdays.py", title="Annviversaires", icon="🎂")
tv_page = st.Page("views/tv.py", title="Programme TV", icon="📺")
upgrade_page = st.Page("views/upgrades.py", title="Améliorations", icon="🆙")
menu_page = st.Page("views/menu.py", title="Menu", icon="🍛")


pg = st.navigation([dashboard_page, tasks_page, shopping_page, birthdays_page, tv_page, upgrade_page, menu_page])
pg.run()