import streamlit as st
from src.database import get_db
db = get_db()

st.title("Liste des tâches")

# --- SECTION AJOUT DE TÂCHE ---
with st.form("add_task_form"):
    task_text = st.text_input("Quelle est la tâche ?")
    member = st.selectbox("Pour qui ?", ["Amaury", "Thais" , "Corentin", "Maman", "Papoune"])
    submit = st.form_submit_button("Ajouter la tache")

    if submit and task_text:
        db.add_task(task_text, member)
        st.success("Tâche ajoutée !")





st.subheader("Liste des tâches en cours")
tasks = db.get_tasks()

if not tasks:
    st.info("Aucune tâche pour le moment.")
else:
    for task in tasks:
        task_id = task[0]
        task_title = task[1]
        task_member = task[2]

        col_text_task, col_btn_task = st.columns([0.5,0.5])

        with col_text_task:
            st.write(f"**{task_member}** : {task_title}")

        with col_btn_task:
            if st.button("Supprimer", key=f"delete_{task_id}"):
                db.remove_task(task_id)
                st.rerun()