import streamlit as st
from datetime import datetime
from src.database import get_family_db

db = get_family_db()
st.title("🎂 Anniversaires")

# --- AJOUT ---
with st.expander("➕ Ajouter un anniversaire"):
    with st.form("birthdays_form", clear_on_submit=True):
        name = st.text_input("Prénom / Nom", placeholder="Ex: Maman, Lucas...")
        bday_date = st.date_input("Date de naissance", min_value=datetime(1900, 1, 1), value=datetime(2000, 1, 1))
        if st.form_submit_button("💾 Enregistrer", use_container_width=True):
            if name:
                db.add_birthday(name, bday_date.strftime("%Y-%m-%d"))
                st.success(f"Anniversaire de {name} ajouté !")
                st.rerun()

st.divider()

# --- AFFICHAGE ---
birthdays = db.get_birthdays()
today = datetime.now()

if not birthdays:
    st.info("Aucun anniversaire enregistré.")
else:
    # On trie un peu pour mettre les prochains plus proches en premier (optionnel)
    for bday in birthdays:
        # Defensive check for dictionary (prevents TypeError seen in logs)
        if not isinstance(bday, dict):
            continue
            
        b_id = bday.get('birthday_id')
        b_name = bday.get('name') or 'Utilisateur'
        b_date_str = bday.get('date')
        
        if not b_id or not b_date_str:
            continue

        
        b_date_obj = datetime.strptime(b_date_str, "%Y-%m-%d")
        
        # Prochain anniversaire
        next_bday = b_date_obj.replace(year=today.year)
        if next_bday.date() < today.date():
            next_bday = next_bday.replace(year=today.year + 1)
        
        days_left = (next_bday.date() - today.date()).days
        age = today.year - b_date_obj.year
        if next_bday.year > today.year:
            age -= 1 # Pas encore fêté cette année
            
        with st.container(border=True):
            c1, c2 = st.columns([0.8, 0.2])
            
            if days_left == 0:
                c1.subheader(f"🎉 JOYEUX ANNIVERSAIRE {b_name.upper()} ! 🎂")
                c1.write(f"Il/Elle fête ses **{age + 1} ans** aujourd'hui !")
                st.balloons()
            else:
                c1.write(f"**{b_name}** • {b_date_obj.strftime('%d %B')}")
                c1.caption(f"Prochain : dans **{days_left} jours** • Aura ({age + 1} ans)")
            
            if c2.button("🗑️", key=f"bday_{b_id}", use_container_width=True):
                db.remove_birthday(b_id)
                st.rerun()