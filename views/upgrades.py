import streamlit as st
from src.database import get_family_db

db = get_family_db()

st.title("🆙 Améliorations de la Maison")
st.write("Idées de projets, travaux ou achats pour améliorer notre foyer.")

# --- AJOUT ---
with st.container(border=True):
    with st.form("upgrades_form", clear_on_submit=True):
        new_upgrade = st.text_input("Nouvelle idée d'amélioration", placeholder="Ex: Refaire la peinture, Acheter un nouveau canapé...")
        if st.form_submit_button("💡 Ajouter à la liste", use_container_width=True):
            if new_upgrade:
                db.add_upgrade(new_upgrade)
                st.success("Idée ajoutée !")
                st.rerun()

st.divider()

# --- LISTE ---
upgrades = db.get_upgrades()
st.subheader("🛠️ Liste des projets")

if not upgrades:
    st.info("Aucun projet en vue. Tout est parfait ! ✨")
else:
    for item in upgrades:
        if not isinstance(item, dict):
            continue
            
        u_id = item.get('upgrade_id')
        u_name = item.get('upgrade_name') or 'Amélioration'
        
        if not u_id:
            continue

        
        with st.container(border=True):
            c1, c2 = st.columns([0.8, 0.2])
            c1.write(f"**{u_name}**")
            if c2.button("🗑️", key=f"upg_{u_id}", use_container_width=True):
                db.remove_upgrade(u_id)
                st.rerun()