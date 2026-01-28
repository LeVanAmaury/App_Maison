import streamlit as st
from src.database import get_db
db = get_db()

st.title("Améliorations")

# --- SECTION AJOUT DE COURSES ---
with st.form("upgrades_form", clear_on_submit=True):
    new_upgrade = st.text_input("Ajouter une amélioration à faire")
    if st.form_submit_button("Ajouter"):
        if new_upgrade:
            db.add_upgrade(new_upgrade)
            st.rerun()

st.divider()


# --- SECTION AFFICHAGE LISTE ---
upgrades = db.get_upgrades()
if not upgrades:
    st.info("La liste est vide.")
else:
    for upgrade_id, upgrade_name in upgrades:
        col1, col2 = st.columns([0.6,0.4])
        col1.write(f"{upgrade_name}")
        if col2.button("Supprimer", key=f"item_{upgrade_id}"):
            db.remove_upgrade(upgrade_id)
            st.rerun()