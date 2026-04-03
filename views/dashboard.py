import streamlit as st
from src.database import get_db
from datetime import datetime
from src.weather import get_weather

db = get_db()

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .note-card {
        padding: 1rem;
        border-radius: 10px;
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 1rem;
    }
    .stMetric {
        background-color: rgba(61, 157, 243, 0.05);
        padding: 10px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 Tableau de bord familial")

# --- MÉTÉO ET DATE ---
city_weather = 'Saint-Sulpice'
w = get_weather(city_weather)
col1, col2 = st.columns([0.6, 0.4])

with col1:
    if w:
        c_icon, c_temp = st.columns([0.3, 0.7])
        with c_icon:
            icon_url = f"https://openweathermap.org/img/wn/{w['icon']}@2x.png"
            st.image(icon_url, width=100)
        with c_temp:
            st.metric(label=f"Météo à {city_weather}", value=f"{w['temp']}°C", delta=w['desc'])
    else:
        st.error("Météo indisponible")

with col2:
    st.info(f"✨ Aujourd'hui : **{datetime.now().strftime('%d %B %Y')}**")
    st.write(f"👤 Connecté : **{st.session_state.get('user', 'Anonyme')}**")

st.divider()

# --- LE MUR DE NOTES ---
st.subheader("📝 Le mur de la famille")
with st.expander("Laisser un petit mot sur le mur"):
    with st.form("note_form", clear_on_submit=True):
        note_text = st.text_area("Ton message :", placeholder="Écris quelque chose de sympa...")
        if st.form_submit_button("Épingler au mur") and note_text:
            db.add_note(note_text, st.session_state["user"])
            st.success("Note ajoutée !")
            st.rerun()

notes = db.get_notes()
if notes:
    cols = st.columns(3)
    for i, note in enumerate(notes):
        n_id = note['note_id']
        n_content = note['content']
        n_date = note['created_at']
        n_author = note.get('author', 'Anonyme')
        n_read_by = note.get('read_by', [])
        
        current_user = st.session_state.get('user')
        if current_user and current_user not in n_read_by and current_user != n_author:
            db.mark_note_as_read(n_id, current_user)
            
        with cols[i % 3]:
            with st.container(border=True):
                st.write(n_content)
                st.caption(f"✍️ {n_author} • {n_date[:10]}")
                c_del, c_read = st.columns([0.2, 0.8])
                if c_del.button("🗑️", key=f"note_{n_id}"):
                    db.delete_note(n_id)
                    st.rerun()
                if n_read_by:
                    c_read.caption(f"👀 Lu par: {', '.join(n_read_by)}")
else:
    st.info("Le mur est vide.")

st.divider()

# --- ACTIVITÉS RÉCENTES ---
c1, c2 = st.columns(2)

with c1:
    st.subheader("🛒 Liste de courses")
    shopping_data = db.get_shopping_list()
    
    if shopping_data:
        latest_shopping = sorted(shopping_data, key=lambda x: x['item_id'], reverse=True)[:5]
        for item in latest_shopping:
            st.write(f"• **{item['item'].strip()}** ({item['list_category']})")
        if st.button("Voir toute la liste"):
            st.switch_page("views/shopping.py")
    else:
        st.info("Rien à acheter.")

with c2:
    st.subheader("⚠️ Tâches en cours")
    tasks_data = db.get_tasks()
    
    if tasks_data:
        # Filtrer les tâches non faites
        pending_tasks = [t for t in tasks_data if not t['done']]
        latest_tasks = sorted(pending_tasks, key=lambda x: x['task_id'], reverse=True)[:5]
        
        if latest_tasks:
            for task in latest_tasks:
                assignees = task['assignee'] if isinstance(task['assignee'], list) else [task['assignee']]
                st.write(f"⏳ **{task['title'].strip()}** → {', '.join(assignees)}")
            if st.button("Voir toutes les tâches"):
                st.switch_page("views/tasks.py")
        else:
            st.success("Toutes les tâches sont finies ! 🎉")
    else:
        st.info("Aucune tâche créée.")