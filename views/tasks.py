import streamlit as st
from src.database import get_db
from src.notification import send_family_notification
db = get_db()

st.title("Liste des tâches")

# --- SECTION AJOUT DE TÂCHE ---
with st.form("add_task_form", clear_on_submit=True):
    task_text = st.text_input("Quelle est la tâche ?")
    member = st.selectbox("Pour qui ?", ["Amaury", "Thais" , "Corentin", "Maman", "Papoune"])
    submit = st.form_submit_button("Ajouter la tache")

    if submit and task_text:
        db.add_task(task_text, member, st.session_state["user"])
        notification_msg = f"Nouvelle mission pour {member} : {task_text}"
        send_family_notification(notification_msg)
        st.success("Tâche ajoutée et norification envoyée !")
        st.rerun()


st.subheader("Liste des tâches en cours")
tasks = db.get_tasks()

if not tasks:
    st.info("Aucune tâche pour le moment.")
else:
    for t_id, t_title, t_member, t_done in tasks:
        col1, col2, col3 = st.columns([0.7, 0.1, 0.2])
        
        label = f"~~{t_title}~~" if t_done else t_title
        col1.write(f"**{t_member}** : {label}")
        
        icon = "✅" if t_done else "⏳"
        if col2.button(icon, key=f"toggle_{t_id}"):
            db.toggle_task_status(t_id, t_done)
            st.rerun()
        
        if col3.button("Supprimer", key=f"task_{t_id}"):
            db.remove_task(t_id)
            st.success("Tâche supprimée avec succès")
            st.rerun()