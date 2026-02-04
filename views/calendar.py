import streamlit as st
from datetime import datetime, date, timedelta
from src.database import get_db

st.set_page_config(layout="wide")
st.title("📅 Planning Familial")
db = get_db()

if "week_start" not in st.session_state:
    today = date.today()
    st.session_state.week_start = today - timedelta(days=today.weekday())
col_prev, col_center, col_next = st.columns([1, 2, 1])
with col_prev:
    if st.button("⬅️ Semaine précédente"):
        st.session_state.week_start -= timedelta(days=7)
        st.rerun()
with col_center:
    start = st.session_state.week_start
    end = start + timedelta(days=6)
    st.markdown(f"<h3 style='text-align: center;'>Semaine du {start.strftime('%d/%m')} au {end.strftime('%d/%m')}</h3>", unsafe_allow_html=True)
    if st.button("Revenir à Aujourd'hui", use_container_width=True):
        st.session_state.week_start = date.today() - timedelta(days=date.today().weekday())
        st.rerun()
with col_next:
    if st.button("Semaine suivante ➡️"):
        st.session_state.week_start += timedelta(days=7)
        st.rerun()
with st.expander("Ajouter un événement"):
    with st.form("add_event_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Quoi ?", placeholder="Ex: Concert de Rock")
            e_date = st.date_input("Le jour", value=date.today())
        with c2:
            t_start = st.time_input("Début", value=datetime.strptime("18:00", "%H:%M").time())
            t_end = st.time_input("Fin", value=datetime.strptime("20:00", "%H:%M").time())
        
        member = st.session_state['user']
        if st.form_submit_button("Ajouter au calendrier"):
            if name:
                db.add_calendar(name, e_date.isoformat(), t_start.isoformat(), t_end.isoformat(), member)
                st.success("Événement ajouté !")
                st.rerun()

st.divider()

monday = st.session_state.week_start
sunday = monday + timedelta(days=6)
events = db.get_calendar(monday.isoformat(), sunday.isoformat())
cols = st.columns(7)
jours_fr = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]

for i in range(7):
    current_day = monday + timedelta(days=i)
    with cols[i]:
        is_today = current_day == date.today()
        if is_today:
            st.markdown(f"### :red[{jours_fr[i]} {current_day.day}]")
            st.caption("🔴 Aujourd'hui")
        else:
            st.markdown(f"### {jours_fr[i]} {current_day.day}")
        day_events = [e for e in events if e['event_date'] == current_day.isoformat()]
        
        for ev in day_events:
            with st.container(border=True):
                titre = ev['event_name'].strip()
                st.markdown(f"**{titre}**")
                debut = ev['start_time'][:5]
                fin = ev['end_time'][:5]
                st.caption(f"🕒 {debut} - {fin} - {ev['member']}")
                if st.button("🗑️", key=f"del_{ev['calendar_id']}"):
                    db.remove_calendar(ev['calendar_id'])
                    st.rerun()