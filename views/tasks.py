import streamlit as st
from src.database import get_family_db
from src.notification import send_private_notification

db = get_family_db()
MEMBRES = ["Amaury", "Thais", "Corentin", "Maman", "Papoune"]

st.title("📝 Gestion des tâches")

# --- AJOUT DE TÂCHE ---
with st.expander("➕ Ajouter une nouvelle mission", expanded=True):
    with st.form("add_task_form", clear_on_submit=True):
        task_text = st.text_input("Quelle est la tâche ?", placeholder="Faire la vaisselle, sortir les poubelles...")
        assignees = st.multiselect("Pour qui ?", MEMBRES)
        
        if st.form_submit_button("Lancer la mission", use_container_width=True):
            if task_text and assignees:
                db.add_task(task_text, assignees, st.session_state["user"])
                # Notification
                notification_msg = f"🔔 Nouvelle mission de {st.session_state['user']} : {task_text}"
                try:
                    send_private_notification(notification_msg, assignees)
                    st.success(f"Tâche ajoutée et notification envoyée !")
                except Exception as e:
                    st.warning("Tâche ajoutée, mais erreur d'envoi de notification.")
                st.rerun()
            else:
                st.error("Précisez la tâche et au moins un responsable.")

st.divider()

# --- FILTRES ---
tasks = db.get_tasks()
col_title, col_filter = st.columns([0.6, 0.4])
col_title.subheader("📋 Missions en cours")
show_only_todo = col_filter.toggle("⏳ À faire uniquement", value=True)

if not tasks:
    st.info("Aucune tâche pour le moment. Reposez-vous ! 🌴")
else:
    # Filtrage
    display_tasks = [t for t in tasks if not t['done']] if show_only_todo else tasks
    # Tri (dernières créées en haut)
    display_tasks = sorted(display_tasks, key=lambda x: x['task_id'], reverse=True)

    for task in display_tasks:
        t_id = task['task_id']
        t_done = task['done']
        
        with st.container(border=True):
            c1, c2, c3 = st.columns([0.6, 0.2, 0.2])
            
            # Affichage texte
            status_icon = "✅" if t_done else "⏳"
            task_label = f"~~{task['title']}~~" if t_done else f"**{task['title']}**"
            c1.markdown(f"{status_icon} {task_label}")
            
            assignees = task['assignee'] if isinstance(task['assignee'], list) else [task['assignee']]
            c1.caption(f"👤 Par **{task.get('created_by', '?')}** pour **{', '.join(assignees)}**")
            
            # Boutons
            btn_label = "Refaire" if t_done else "Terminer"
            if c2.button(btn_label, key=f"toggle_{t_id}", use_container_width=True):
                db.toggle_task_status(t_id, t_done)
                st.rerun()
                
            if c3.button("🗑️", key=f"del_{t_id}", use_container_width=True):
                db.remove_task(t_id)
                st.rerun()