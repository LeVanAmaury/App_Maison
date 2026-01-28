import streamlit as st
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

CHANNEL_MAP = {
    "TF1.fr": "TF1", "France2.fr": "France 2", "France3.fr": "France 3",
    "CanalPlus.fr": "Canal+", "France5.fr": "France 5", "M6.fr": "M6",
    "Arte.fr": "Arte", "C8.fr": "C8", "W9.fr": "W9", "TMC.fr": "TMC",
    "TFX.fr": "TFX", "NRJ12.fr": "NRJ 12", "LCP.fr": "LCP", 
    "France4.fr": "France 4", "BFMTV.fr": "BFM TV", "CNews.fr": "CNEWS",
    "CStar.fr": "CStar", "Gulli.fr": "Gulli", "TF1SeriesFilms.fr": "TF1 Séries Films",
    "LEQUIPE.fr": "L'Équipe", "6ter.fr": "6ter", "RMCStory.fr": "RMC Story",
    "RMCDecouverte.fr": "RMC Découverte", "Cherie25.fr": "Chérie 25"
}

st.title("📺 Programme TV")

@st.cache_data(ttl=300)
def get_tv_data():
    url = "https://xmltvfr.fr/xmltv/xmltv_fr.xml"
    try:
        response = requests.get(url)
        root = ET.fromstring(response.content)
        programs = []
        now = datetime.now()
        
        for prog in root.findall('programme'):
            ch_id = prog.get('channel')
            if ch_id in CHANNEL_MAP:
                s_str = prog.get('start')[:14]
                e_str = prog.get('stop')[:14]
                start_dt = datetime.strptime(s_str, "%Y%m%d%H%M%S")
                stop_dt = datetime.strptime(e_str, "%Y%m%d%H%M%S")
                
                if stop_dt > now:
                    icon_tag = prog.find('icon')
                    programs.append({
                        "channel": CHANNEL_MAP[ch_id],
                        "start_dt": start_dt,
                        "stop_dt": stop_dt,
                        "title": prog.find('title').text,
                        "desc": prog.find('desc').text if prog.find('desc') is not None else "",
                        "category": prog.find('category').text if prog.find('category') is not None else "Autre",
                        "image": icon_tag.get('src') if icon_tag is not None else None
                    })
        programs.sort(key=lambda x: x['start_dt'])
        return programs
    except:
        return []

tv_list = get_tv_data()
now = datetime.now()

if not tv_list:
    st.info("Aucun programme trouvé.")
else:
    for p in tv_list[:20]:
        with st.container(border=True):
            col_h, col_img, col_txt = st.columns([0.15, 0.25, 0.6])
            
            with col_h:
                st.subheader(p['start_dt'].strftime("%Hh%M"))
            
            with col_img:
                if p['image']:
                    st.image(p['image'], use_container_width=True)
            
            with col_txt:
                st.markdown(f"**{p['channel']}** : {p['title']}")
                st.caption(f"🎭 {p['category']}")
                
                if p['start_dt'] <= now <= p['stop_dt']:
                    total = (p['stop_dt'] - p['start_dt']).total_seconds()
                    past = (now - p['start_dt']).total_seconds()
                    progression = min(past / total, 1.0)
                    st.progress(progression, text=f"Direct : {int(progression*100)}%")
                
                if p['desc']:
                    with st.expander("Détails"):
                        st.write(p['desc'])