import streamlit as st
from src.database import get_db

st.set_page_config(layout="wide")
st.title("🍴 Menu de la Semaine")

db = get_db()
jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

with st.expander("Ajouter un plat au menu"):
    with st.form("add_meal", clear_on_submit=True):
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            day_choice = st.selectbox("Jour", jours)
        with col_f2:
            type_choice = st.selectbox("Repas", ["Midi", "Soir"])
        with col_f3:
            dish_name = st.text_input("Repas")
        
        submit = st.form_submit_button("Ajouter au menu")
        
        if submit and dish_name:
            db.add_menu_item(day_choice, type_choice, dish_name)
            st.success(f"Ajouté pour {day_choice} !")
            st.rerun()

menu_data = db.get_menu()
cols = st.columns(7)

for i, jour in enumerate(jours):
    with cols[i]:
        st.markdown(f"### {jour}")
        
        # Filtrer les plats pour ce jour
        for meal in ["Midi", "Soir"]:
            st.markdown(f"**{meal}**")
            # On cherche les plats correspondants
            items = [item for item in menu_data if item['day'] == jour and item['meal_type'] == meal]
            
            if items:
                for it in items:
                    c1, c2 = st.columns([0.8, 0.4])
                    c1.caption(it['dish'])
                    if c2.button("🗑️", key=f"del_{it['item_id']}"):
                        db.clear_menu_item(it['item_id'])
                        st.rerun()
            else:
                st.write("*Rien de prévu*")
        
        st.divider()