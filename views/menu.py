import streamlit as st
from src.database import get_db

st.title("🍴 Menu de la Semaine")

db = get_db()
jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

# --- AJOUT ---
with st.expander("➕ Planifier un nouveau repas"):
    with st.form("add_meal", clear_on_submit=True):
        col_f1, col_f2, col_f3 = st.columns([0.3, 0.3, 0.4])
        with col_f1:
            day_choice = st.selectbox("Jour", jours)
        with col_f2:
            type_choice = st.selectbox("Repas", ["☀️ Midi", "🌙 Soir"])
        with col_f3:
            dish_name = st.text_input("Qu'est-ce qu'on mange ?", placeholder="Lasagnes, Salade, etc.")
        
        if st.form_submit_button("📅 Ajouter au planning", use_container_width=True):
            if dish_name:
                db.add_menu_item(day_choice, type_choice, dish_name)
                st.success(f"Ajouté au menu !")
                st.rerun()

st.divider()

# --- AFFICHAGE ---
menu_data = db.get_menu()
cols = st.columns(7)

for i, jour in enumerate(jours):
    with cols[i]:
        st.markdown(f"### {jour[:3]}.") # Abrégé pour la largeur
        
        # Midi
        st.markdown("<small>☀️ <b>Midi</b></small>", unsafe_allow_html=True)
        midi_items = [item for item in menu_data if item['day'] == jour and "Midi" in item['meal_type']]
        with st.container(border=True):
            if midi_items:
                for it in midi_items:
                    st.write(it['dish'])
                    if st.button("🗑️", key=f"del_m_{it['item_id']}", use_container_width=True):
                        db.clear_menu_item(it['item_id'])
                        st.rerun()
            else:
                st.caption("---")
        
        # Soir
        st.markdown("<small>🌙 <b>Soir</b></small>", unsafe_allow_html=True)
        soir_items = [item for item in menu_data if item['day'] == jour and "Soir" in item['meal_type']]
        with st.container(border=True):
            if soir_items:
                for it in soir_items:
                    st.write(it['dish'])
                    if st.button("🗑️", key=f"del_s_{it['item_id']}", use_container_width=True):
                        db.clear_menu_item(it['item_id'])
                        st.rerun()
            else:
                st.caption("---")