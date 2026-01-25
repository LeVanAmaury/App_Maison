import streamlit as st
from src.database import FamilyDB

@st.cache_resource      # Pour ne pas recréer la connexion à chaque clic
def get_db():
    return FamilyDB()

db = get_db()
with st.form("task_form"):
    task_text = st.text_input("Quelle est la tâche à supprimer ?")
    member = st.selectbox("Pour qui ?", ["Amaury","Thais","Corentin","Maman","Papoune"])
    submit = st.form_submit_button("Supprimer la tâche")

    if submit and task_text:
        db.remove_task(task_text, member)
        st.success("Tâche supprimée !")

# --- SECTION AFFICHAGE ---
st.divider()
st.subheader("📋 Liste des tâches en cours")
tasks = db.get_tasks()

if not tasks:
    st.info("Aucune tâche pour le moment. C'est les vacances !")
else:
    for task in tasks:
        # task[1] est le titre, task[2] est le membre (selon notre structure SQL)
        st.write(f"**{task[2]}** doit : {task[1]}")