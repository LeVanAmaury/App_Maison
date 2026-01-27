import streamlit as st
from src.database import get_db
from src.notification import send_family_notification
db = get_db()

st.title("Liste des tâches")

# --- SECTION AJOUT DE TÂCHE ---
with st.form("add_task_form"):
    task_text = st.text_input("Quelle est la tâche ?")
    member = st.selectbox("Pour qui ?", ["Amaury", "Thais" , "Corentin", "Maman", "Papoune"])
    submit = st.form_submit_button("Ajouter la tache")

    if submit and task_text:
        db.add_task(task_text, member)
        notification_msg = f"Nouvelle mission pour {member} : {task_text}"
        send_family_notification(notification_msg)
        st.success("Tâche ajoutée et norification envoyée !")
        st.rerun()


st.subheader("Liste des tâches en cours")
tasks = db.get_tasks()

if not tasks:
    st.info("Aucune tâche pour le moment.")
else:
    tab1, tab2 = st.tabs(["A faire", "Terminées"])
    with tab1:
        pending = [t for t in tasks if t[3] == 0]
        for t_id, t_title, t_member, t_status in pending:
            c1, c2 = st.columns([0.8,0.2])
            c1.write(f"**{t_member}** : {t_title}")
            if c2.button("Fait", key=f"check_{t_id}"):
                db.toggle_task_status(t_id)
                st.rerun()
    with tab2:
        completed = [t for t in tasks if t[3] == 1]
        for t_id, t_title, t_member, t_status in completed:
            c1, c2 = st.columns([0.8, 0.2])
            c1.write(f"~~{t_member} : {t_title}~~")
            if c2.button("Supprimer", key=f"suppr_{t_id}"):
                db.remove_task(t_id)
                st.rerun()