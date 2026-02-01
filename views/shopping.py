import streamlit as st
from src.database import get_db

st.set_page_config(layout="wide")
st.title("Liste de courses")

db = get_db()

data = db.get_shopping_list()

if data:
    categories = sorted(list(set(d['list_category'] for d in data)))
else:
    categories = ['Commune']

# --- SECTION AJOUT DE COURSES ---
with st.container(border=True):
    st.write("### Ajouter un article")
    with st.form("global_add_form", clear_on_submit=True):
        col_txt, col_cat, col_btn = st.columns([0.5,0.3,0.2])

        with col_txt:
            new_item = st.text_input("Objet à acheter", placeholder='Ex: Fromage')
        
        with col_cat:
            cat_choice = st.selectbox("Dans quelle liste ?", categories + ["Nouvelle liste..."])
            new_cat_name = ""
            if cat_choice == "Nouvelle liste...":
                new_cat_name = st.text_input("Nom de la nouvelle liste", placeholder="Ex: Anniversaire")
                
        with col_btn:
            st.write(" ")
            submit = st.form_submit_button("Ajouter")
        

    if submit and new_item:
        final_cat = new_cat_name if cat_choice == 'Nouvelle liste...' else cat_choice
        if final_cat:
            db.add_shopping_item(new_item, final_cat)
            st.success(f"{new_item} ajouté à {final_cat}")
            st.rerun()
            
st.divider()


# --- SECTION AFFICHAGE LISTE ---
if not data:
    st.info("La liste est vide.")
else:
    cols = st.columns(len(categories))

    for i, cat_name in enumerate(categories):
        with cols[i]:
            st.markdown(f"### {cat_name}")

            item_in_cat = [d for d in data if d['list_category'] == cat_name]

            for it in item_in_cat:
                c_txt, c_del = st.columns([0.8,0.2])
                c_txt.write(f"• {it['item']}")
                if c_del.button("🗑️", key=f"del_{it['id']}"):
                    db.remove_shopping_item(it['item_id'])
                    st.rerun()
            
            if not item_in_cat:
                st.caption("Liste vide")