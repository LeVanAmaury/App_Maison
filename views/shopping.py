import streamlit as st
from src.database import get_db

st.title("🛒 Listes de courses")

db = get_db()
data = db.get_shopping_list()

# Récupération des catégories existantes
if data:
    categories = sorted(list(set(d.get('list_category', 'Commune') for d in data)))
else:
    categories = ['Commune']

# --- ZONE D'ACTIONS ---
col_action1, col_action2 = st.columns(2)

with col_action1:
    with st.expander("Ajouter un objet", expanded=True):
        with st.form("quick_add", clear_on_submit=True):
            target_cat = st.selectbox("Dans quelle liste ?", categories)
            item_name = st.text_input("Quoi acheter ?")
            if st.form_submit_button("Ajouter"):
                if item_name:
                    db.add_shopping_item(item_name, target_cat)
                    st.rerun()

with col_action2:
    with st.expander("Créer une nouvelle liste de courses"):
        with st.form("new_list_form", clear_on_submit=True):
            new_cat = st.text_input("Nom de la liste", placeholder="Ex: Anniversaire")
            if st.form_submit_button("Créer la liste"):
                if new_cat:
                    db.add_shopping_item("", new_cat)
                    st.rerun()

st.divider()

# --- AFFICHAGE DES COLONNES (Dynamique) ---
if not data:
    st.info("Aucun article pour le moment.")
else:
    # On garde le système de colonnes dynamiques que tu aimais
    cols = st.columns(len(categories))

    for i, cat_name in enumerate(categories):
        with cols[i]:
            st.markdown(f"### {cat_name}")
            items = [d for d in data if d.get('list_category') == cat_name]
            
            for it in items:
                c_txt, c_del = st.columns([0.8, 0.2])
                c_txt.write(f"• {it['item']}")
                if c_del.button("🗑️", key=f"del_{it['item_id']}"):
                    db.remove_shopping_item(it['item_id'])
                    st.rerun() # Rafraîchit instantanément