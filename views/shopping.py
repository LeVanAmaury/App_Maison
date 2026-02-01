import streamlit as st
from src.database import get_db

# Configuration large pour voir toutes les colonnes
st.title("🛒 Liste de courses")

db = get_db()
data = db.get_shopping_list()

# Récupération dynamique des catégories
if data:
    categories = sorted(list(set(d.get('list_category', 'Commune') for d in data)))
else:
    categories = ['Commune']

# --- SECTION AJOUT DE COURSES ---
with st.container(border=True):
    st.write("### Ajouter un article")
    with st.form("global_add_form", clear_on_submit=True):
        # FIX : On utilise [] pour les colonnes
        col_txt, col_cat, col_btn = st.columns([0.5, 0.3, 0.2])

        with col_txt:
            new_item = st.text_input("Objet à acheter", placeholder='Ex: Fromage')
        
        with col_cat:
            cat_choice = st.selectbox("Dans quelle liste ?", categories + ["Nouvelle liste..."])
            new_cat_name = st.text_input("Nom de la nouvelle liste (si besoin)", placeholder="Ex: Anniversaire")
                
        with col_btn:
            st.write(" ") # Alignement
            submit = st.form_submit_button("Ajouter")

    if submit and new_item:
        final_cat = new_cat_name if cat_choice == 'Nouvelle liste...' else cat_choice
        if final_cat:
            db.add_shopping_item(new_item, final_cat)
            st.success(f"{new_item} ajouté à {final_cat}")
            st.rerun() # Ceci vide la case et rafraîchit l'affichage
            
st.divider()

# --- SECTION AFFICHAGE LISTE (Colonnes dynamiques) ---
if not data:
    st.info("La liste est vide.")
else:
    cols = st.columns(len(categories))

    for i, cat_name in enumerate(categories):
        with cols[i]:
            st.markdown(f"### {cat_name}")
            items_in_cat = [d for d in data if d.get('list_category') == cat_name]

            for it in items_in_cat:
                c_txt, c_del = st.columns([0.8, 0.2])
                c_txt.write(f"• {it['item']}")
                # FIX : On utilise item_id partout pour la cohérence
                if c_del.button("🗑️", key=f"del_{it['item_id']}"):
                    db.remove_shopping_item(it['item_id'])
                    st.rerun()