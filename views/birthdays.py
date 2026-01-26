import streamlit as st
from datetime import datetime
from src.database import get_db

db = get_db()
st.title("🎂 Anniversaires")

with st.expander("Ajouter un anniversaire"):
    name = st.text_input("Nom")
    date = st.date_input("Date de naissance", min_value = datetime(1900, 1, 1))
    if st.button("Enregistrer"):
        db.add_birthday(name, date.strftime("%Y-%m-%d"))
        st.success(f"Anniversaire de {name} ajouté !")
        st.rerun()

st.divider()

birthdays = db.get_birthdays()
today = datetime.now()

for b_id, b_name, b_date in birthdays:
    b_date_obj = datetime.strptime(b_date, "%Y-%m-%d")

    next_bday = b_date_obj.replace(year=today.year)
    if next_bday < today:
        next_bday = next_bday.replace(year=today.year +1)

    days_left = (next_bday - today).days

    col1, col2 = st.columns([0.8,0.2])
    col1.write(f"**{b_name}** - {b_date_obj.strftime('%d/%m')} (dans {days_left} jours)")
    if days_left == 0:
        st.balloons()