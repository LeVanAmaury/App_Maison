import streamlit as st
from src.database import get_family_db

st.title("🛒 Listes de courses")

db = get_family_db()
data = db.get_shopping_list()

# Récupération des catégories existantes
all_categories = sorted(list(set(d.get('list_category', 'Commune') for d in data))) if data else ['Commune']
# Filtrer les catégories qui pourraient être vides ou juste des placeholders
categories = [c for c in all_categories if c] or ['Commune']

# --- ZONE D'ACTIONS ---
c1, c2 = st.columns(2)

with c1:
    with st.expander("➕ Ajouter un article", expanded=True):
        with st.form("quick_add", clear_on_submit=True):
            target_cat = st.selectbox("Dans quelle liste ?", categories)
            item_name = st.text_input("Quoi acheter ?", placeholder="Lait, Pain, etc.")
            if st.form_submit_button("Ajouter", use_container_width=True):
                if item_name:
                    db.add_shopping_item(item_name, target_cat)
                    st.success(f"{item_name} ajouté à {target_cat} !")
                    st.rerun()

with c2:
    with st.expander("📂 Créer une nouvelle liste"):
        with st.form("new_list_form", clear_on_submit=True):
            new_cat = st.text_input("Nom de la liste", placeholder="Ex: Bricolage, Pharmacie...")
            if st.form_submit_button("Créer la liste", use_container_width=True):
                if new_cat:
                    # On ajoute un item vide ou juste la catégorie
                    db.add_shopping_item("--- Liste créée ---", new_cat)
                    st.success(f"Liste '{new_cat}' créée !")
                    st.rerun()

st.divider()

# --- AFFICHAGE ---
if not data:
    st.info("Aucun article pour le moment. Votre frigo est-il si plein ? 🧀")
else:
    # Affichage en colonnes selon le nombre de catégories
    cols = st.columns(len(categories))

    for i, cat_name in enumerate(categories):
        with cols[i]:
            st.markdown(f"### 📍 {cat_name}")
            # Filtrer les items de cette catégorie
            items = [d for d in data if d.get('list_category') == cat_name and d.get('item')]
            
            for it in items:
                with st.container(border=True):
                    c_txt, c_del = st.columns([0.7, 0.3])
                    c_txt.write(it['item'])
                    if c_del.button("🗑️", key=f"del_{it['item_id']}", use_container_width=True):
                        db.remove_shopping_item(it['item_id'])
                        st.rerun()