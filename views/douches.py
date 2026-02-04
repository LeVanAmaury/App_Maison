import streamlit as st
from datetime import datetime, date, timedelta
from src.database import get_db

st.title("🚿 Planning de Douches")
db = get_db()

choix = st.radio("Pour quel jour ?", ["Aujourd'hui", "Demain"], horizontal=True)

if choix == "Aujourd'hui":
    target_date = date.today()
else:
    target_date = date.today() + timedelta(days=1)

date_str = target_date.isoformat()
st.info(f"📅 Planning du : **{target_date.strftime('%d/%m/%Y')}**")

data = db.get_showers(date_str)
booked_slots = {d['slot_time']: d for d in data}

slots = ['06:00','06:15','06:30','06:45','07:00','07:15','07:30','07:45','08:00','08:15','08:30']

for slot in slots:
    col_time, col_action = st.columns([0.2, 0.8])
    
    with col_time:
        st.subheader(slot)
        
    with col_action:
        if slot in booked_slots:
            res = booked_slots[slot]
            nom = res['user_name']
            
            c_txt, c_btn = st.columns([0.8, 0.2])
            c_txt.warning(f"🚿 {nom}")
            
            if nom == st.session_state.get('user'):
                if c_btn.button("🗑️", key=f"del_{slot}_{date_str}"):
                    db.remove_shower(res['douche_id']) 
                    st.rerun()
        else:
            if st.button(f"Réserver {slot}", key=f"btn_{slot}_{date_str}", use_container_width=True):
                user = st.session_state.get('user', 'Anonyme')
                db.add_shower_slot(slot, user, date_str) 
                st.rerun()