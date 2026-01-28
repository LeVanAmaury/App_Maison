import streamlit as st
from src.database import get_db
db = get_db()

st.title("Liste de courses")

# --- SECTION AJOUT DE COURSES ---
with st.form("shopping_form", clear_on_submit=True):
    new_item = st.text_input("Ajouter un article")
    if st.form_submit_button("Ajouter à la liste"):
        if new_item:
            db.add_shopping_item(new_item)
            st.rerun()

st.divider()


# --- SECTION AFFICHAGE LISTE ---
items = db.get_shopping_list()
if not items:
    st.info("La liste est vide.")
else:
    for item_id, item_name in items:
        col1, col2 = st.columns([0.6,0.4])
        col1.write(f"🔹 {item_name}")
        if col2.button("Supprimer", key=f"item_{item_id}"):
            db.remove_shopping_item(item_id)
            st.rerun()