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
    "RMCDecouverte.fr": "RMC Découverte", "Cherie25.fr": "Chérie 25",
    "viaATV.fr": "ATV Martinique", "viaMaTele.fr": "Ma Télé"
}

st.title("📺 Programme à la télé")

@st.cache_data(ttl=300)
def get_sorted_tv():
    url = "https://xmltvfr.fr/xmltv/xmltv_fr.xml"
    try:
        response = requests.get(url)
        root = ET.fromstring(response.content)
        
        programs = []
        now = datetime.now()
        
        for prog in root.findall('programme'):
            channel_id = prog.get('channel')
            
            if channel_id in CHANNEL_MAP:
                start_dt = datetime.strptime(prog.get('start')[:14], "%Y%m%d%H%M%S")
                stop_dt = datetime.strptime(prog.get('stop')[:14], "%Y%m%d%H%M%S")
                
                if stop_dt > now:
                    title = prog.find('title').text
                    icon_tag = prog.find('icon')
                    
                    programs.append({
                        "channel": CHANNEL_MAP[channel_id],
                        "start_time": start_dt,
                        "display_hour": start_dt.strftime("%Hh%M"),
                        "title": title,
                        "desc": prog.find('desc').text if prog.find('desc') is not None else "",
                        "image": icon_tag.get('src') if icon_tag is not None else None,
                        "category": prog.find('category').text if prog.find('category') is not None else "Autre"
                    })
        
        programs.sort(key=lambda x: x['start_time'])
        return programs
    except:
        return []

# --- AFFICHAGE ---
tv_data = get_sorted_tv()

if not tv_data:
    st.info("Recherche des programmes en cours...")
else:
    for p in tv_data[:20]:
        with st.container(border=True):
            col_hour, col_img, col_text = st.columns([0.15, 0.25, 0.6])
            
            with col_hour:
                st.subheader(f"{p['display_hour']}")
            
            with col_img:
                if p['image']:
                    st.image(p['image'], use_container_width=True)
                else:
                    st.write("📺")
            
            with col_text:
                st.markdown(f"**{p['channel']}** : {p['title']}")
                st.caption(f"{p['category']}")
                
                if p['desc']:
                    with st.expander("Lire le résumé"):
                        st.write(p['desc'])