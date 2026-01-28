import streamlit as st
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta

# 1. Liste ordonnée des chaînes (pour le tri "réel")
CHANNELS_ORDER = [
    "TF1.fr", "France2.fr", "France3.fr", "CanalPlus.fr", "France5.fr", "M6.fr", 
    "Arte.fr", "C8.fr", "W9.fr", "TMC.fr", "TFX.fr", "NRJ12.fr", "LCP.fr", 
    "France4.fr", "BFMTV.fr", "CNews.fr", "CStar.fr", "Gulli.fr", 
    "TF1SeriesFilms.fr", "LEQUIPE.fr", "6ter.fr", "RMCStory.fr", 
    "RMCDecouverte.fr", "Cherie25.fr"
]

CHANNEL_NAMES = {
    "TF1.fr": "TF1", "France2.fr": "France 2", "France3.fr": "France 3",
    "CanalPlus.fr": "Canal+", "France5.fr": "France 5", "M6.fr": "M6",
    "Arte.fr": "Arte", "C8.fr": "C8", "W9.fr": "W9", "TMC.fr": "TMC",
    "TFX.fr": "TFX", "NRJ12.fr": "NRJ 12", "LCP.fr": "LCP", 
    "France4.fr": "France 4", "BFMTV.fr": "BFM TV", "CNews.fr": "CNEWS",
    "CStar.fr": "CStar", "Gulli.fr": "Gulli", "TF1SeriesFilms.fr": "TF1 Séries Films",
    "LEQUIPE.fr": "L'Équipe", "6ter.fr": "6ter", "RMCStory.fr": "RMC Story",
    "RMCDecouverte.fr": "RMC Découverte", "Cherie25.fr": "Chérie 25"
}

st.title("📺 Grille TV par chaîne")

@st.cache_data(ttl=300)
def get_grouped_tv_data():
    url = "https://xmltvfr.fr/xmltv/xmltv_fr.xml"
    try:
        response = requests.get(url)
        root = ET.fromstring(response.content)
        organized_data = {ch_id: [] for ch_id in CHANNELS_ORDER}
        
        # FIX HEURE : On définit l'heure actuelle en France (UTC+1)
        tz_france = timezone(timedelta(hours=1))
        now = datetime.now(tz_france)
        
        for prog in root.findall('programme'):
            ch_id = prog.get('channel')
            if ch_id in organized_data:
                # On parse avec le fuseau horaire du XML (%z)
                start_dt = datetime.strptime(prog.get('start'), "%Y%m%d%H%M%S %z")
                stop_dt = datetime.strptime(prog.get('stop'), "%Y%m%d%H%M%S %z")
                
                if stop_dt > now:
                    icon_tag = prog.find('icon')
                    organized_data[ch_id].append({
                        "start_dt": start_dt,
                        "stop_dt": stop_dt,
                        "title": prog.find('title').text,
                        "category": prog.find('category').text if prog.find('category') is not None else "Autre",
                        "image": icon_tag.get('src') if icon_tag is not None else None
                    })
        return organized_data
    except:
        return {}

# --- LOGIQUE D'AFFICHAGE ---
tz_france = timezone(timedelta(hours=1))
now = datetime.now(tz_france)
grouped_list = get_grouped_tv_data()

# On parcourt les chaînes dans l'ordre défini par CHANNELS_ORDER
for ch_id in CHANNELS_ORDER:
    progs = grouped_list.get(ch_id, [])
    if not progs:
        continue
    
    # On identifie le programme actuel et le suivant
    current_p = None
    next_p = None
    
    for p in progs:
        if p['start_dt'] <= now <= p['stop_dt']:
            current_p = p
        elif p['start_dt'] > now:
            next_p = p
            break # On prend le premier qui commence après "maintenant"

    # Si on n'a rien en cours, on saute la chaîne (ou on affiche la prochaine directement)
    if not current_p and not next_p:
        continue

    # --- RENDU DE LA CARTE CHAÎNE ---
    with st.container(border=True):
        # Header de la chaîne
        st.markdown(f"## {CHANNEL_NAMES[ch_id]}")
        
        # Colonnes pour le programme en cours
        col_img, col_info = st.columns([0.3, 0.7])
        
        with col_img:
            if current_p and current_p['image']:
                st.image(current_p['image'], use_container_width=True)
            else:
                st.write("📺")

        with col_info:
            if current_p:
                st.markdown(f"**EN DIRECT : {current_p['title']}**")
                st.caption(f"🕒 {current_p['start_dt'].strftime('%H:%M')} - {current_p['stop_dt'].strftime('%H:%M')} | {current_p['category']}")
                
                # Barre de progression
                total = (current_p['stop_dt'] - current_p['start_dt']).total_seconds()
                past = (now - current_p['start_dt']).total_seconds()
                progression = min(max(past / total, 0.0), 1.0)
                st.progress(progression)
            else:
                st.info("Aucun programme en cours.")

        # Affichage du programme suivant (plus discret)
        if next_p:
            st.markdown(f"➡️ **À SUIVRE :** {next_p['start_dt'].strftime('%H:%M')} - **{next_p['title']}**")