import streamlit as st
from src.database import get_db
from src.notification import send_private_notification
db = get_db()

st.title("Liste des tâches")

# --- SECTION AJOUT DE TÂCHE ---
with st.form("add_task_form", clear_on_submit=True):
    task_text = st.text_input("Quelle est la tâche ?")
    member = st.selectbox("Pour qui ?", ["Amaury", "Thais" , "Corentin", "Maman", "Papoune"])
    submit = st.form_submit_button("Ajouter la tache")

    if submit and task_text:
        db.add_task(task_text, member, st.session_state["user"])
        notification_msg = f"Nouvelle mission de {st.session_state["user"]} : {task_text}"
        send_private_notification(notification_msg, member)
        st.success(f"Tâche ajoutée et norification envoyée à {member} !")
        st.rerun()


st.subheader("Liste des tâches en cours")
tasks = db.get_tasks()

if not tasks:
    st.info("Aucune tâche pour le moment.")
else:
    col_f, col_empty = st.columns([0.4,0.6])
    with col_f:
        show_only_todo = st.toggle("N'afficher que les tâches à faire", value=False)
    if show_only_todo:
        tasks = [t for t in tasks if t[3] == False]
    for t_id, t_title, t_member, t_done, t_created_by in tasks:
        col1, col2, col3 = st.columns([0.7, 0.1, 0.2])
        
        label = f"~~{t_title}~~" if t_done else t_title
        col1.write(f"Tâche de **{t_created_by}** pour **{t_member}** : {label}")
        
        status_done_button = "Fait" if t_done else "A faire"
        if col2.button(status_done_button, key=f"toggle_{t_id}"):
            db.toggle_task_status(t_id, t_done)
            st.rerun()
        
        if col3.button("Supprimer", key=f"task_{t_id}"):
            db.remove_task(t_id)
            st.success("Tâche supprimée avec succès")
            st.rerun()