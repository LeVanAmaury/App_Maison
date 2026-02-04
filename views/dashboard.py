import streamlit as st
from src.database import get_db
from datetime import datetime
from src.weather import get_weather

db = get_db()
st.title("📊 Tableau de bord familial")

# --- MÉTÉO ET DATE ---
city_weather = 'Saint-Sulpice'
w = get_weather(city_weather)
col1, col2 = st.columns(2)

with col1:
    if w:
        col_icon, col_temp = st.columns([0.2,0.8])
        with col_icon:
            icon_url = f"https://openweathermap.org/img/wn/{w['icon']}@2x.png"
            st.image(icon_url, width=100)
        with col_temp:
            st.metric(label=f"Météo à {city_weather}", value=f"{w['temp']}°C", delta=w['desc'])
    else:
        st.error("Météo indisponible")

with col2:
    st.info(f"Aujourd'hui nous sommes le **{datetime.now().strftime('%d %B %Y')}**")
    st.write(f"👤 Utilisateur : **{st.session_state.get('user', 'Anonyme')}**")

st.divider()

# --- LE MUR DE NOTES ---
st.write("### 📝 Le mur de la famille")
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
    for i, (n_id, n_content, n_date, n_author,n_read_by) in enumerate(notes):
        lecteurs = n_read_by if n_read_by else []
        current_user = st.session_state['user']
        if current_user not in lecteurs:
            if current_user != n_author:
                db.mark_note_as_read(n_id, current_user)
        with cols[i % 3]:
            with st.container(border=True):
                st.write(n_content)
                st.caption(f"{n_author} • {n_date[:10]}")
                col_button_suppr, col_read_by = st.columns([0.4,0.6])
                if col_button_suppr.button("🗑️", key=f"note_{n_id}"):
                    db.delete_note(n_id)
                    st.rerun()
                if n_read_by:
                    col_read_by.caption(f"Lu par {','.join(map(str,n_read_by))}")
else:
    st.info("Le mur est vide.")

st.divider()

# --- DERNIÈRES ACTIVITÉS (Shopping & Tasks) ---
c1, c2 = st.columns(2)

with c1:
    st.write("### 🛒 Derniers ajouts courses")
    shopping_data = db.get_shopping_list() # Récupère les dictionnaires
    
    if shopping_data:
        # On trie par ID décroissant pour avoir les derniers ajoutés en premier
        latest_shopping = sorted(shopping_data, key=lambda x: x['item_id'], reverse=True)[:5]
        for item in latest_shopping:
            st.write(f"• **{item['item'].strip()}** (dans *{item['list_category']}*)")
    else:
        st.info("Aucun article à acheter.")

with c2:
    st.write("### ⚠️ Dernières tâches créées")
    tasks_data = db.get_tasks() # Récupère les tuples
    
    if tasks_data:
        # On trie par task_id (index 0 du tuple) décroissant
        latest_tasks = sorted(tasks_data, key=lambda x: x[0], reverse=True)[:5]
        for t_id, t_title, t_assignee, t_done, t_creator in latest_tasks:
            status = "✅" if t_done else "⏳"
            st.write(f"{status} **{t_title.strip()}** → {','.join(map(str,t_assignee))}")
    else:
        st.info("Toutes les corvées sont finies !")