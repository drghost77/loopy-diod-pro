# LOOPY DIOD v14.9 - BUNKER MODE (LOCAL + CLOUD READY)
import streamlit as st
import pandas as pd
import re
import base64
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import phonenumbers
from phonenumbers import format_number, PhoneNumberFormat, geocoder, is_valid_number, parse
import json

# === CONFIG ===
st.set_page_config(page_title="LOOPY DIOD v14.9", layout="wide", page_icon="")

# === NEON CYBER CSS (FIXED & CLOSED) ===
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&display=swap');
    :root { --cyan: #00FFFF; --magenta: #FF00FF; --void: #0D1117; }
    body { background: var(--void); color: white; font-family: 'Orbitron', monospace; }
    .stApp { background: transparent !important; }
    .glass { background: rgba(255,255,255,0.05); backdrop-filter: blur(20px); border: 1px solid var(--cyan); border-radius: 20px; padding: 1.5rem; box-shadow: 0 8px 32px rgba(0,255,255,0.3); }
    .glass:hover { transform: scale(1.02); }
    .neon-btn { background: linear-gradient(45deg, var(--cyan), var(--magenta)); color: black; font-weight: bold; border: none; border-radius: 12px; padding: 12px 24px; }
    .dropzone { border: 3px dashed var(--cyan); border-radius: 16px; padding: 2rem; text-align: center; }
    .dropzone:hover { background: rgba(0,255,255,0.1); }
    .neon-text { background: linear-gradient(45deg, var(--cyan), var(--magenta), #FFD700); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; }
</style>
""", unsafe_allow_html=True)  # FERMETURE CORRECTE ICI

# === VOICE INPUT JS ===
st.markdown("""
<script>
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = 'fr-FR';
recognition.onresult = (e) => {
    const text = e.results[0][0].transcript;
    document.getElementById('voice-output').innerText = text;
    // Envoie au backend Streamlit
    Streamlit.setComponentValue(text);
};
function startVoice() {
    recognition.start();
}
</script>
""", unsafe_allow_html=True)

# === MAIN UI ===
st.markdown("<h1 class='neon-text'>LOOPY DIOD v14.9</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; opacity:0.8;'>Bunker Mode – Local + Cloud Ready</p>", unsafe_allow_html=True)

# === INPUTS ===
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### Entrée de Données")
    input_method = st.radio("Choisis", ["Texte", "Fichier", "Voix"], horizontal=True)

    if input_method == "Texte":
        data_input = st.text_area("Colle ici", height=150, placeholder="+509 31 45 66 42")
    elif input_method == "Fichier":
        uploaded = st.file_uploader("Glisse ou upload", type=['txt','csv','xlsx','pdf'])
        data_input = ""
        if uploaded:
            if uploaded.type == "text/csv":
                df = pd.read_csv(uploaded)
            elif "sheet" in uploaded.type:
                df = pd.read_excel(uploaded)
            else:
                content = uploaded.read().decode("utf-8")
                df = pd.DataFrame({"raw": content.split("\n")})
            data_input = "\n".join(df.iloc[:,0].astype(str).tolist())
            st.success(f"{len(data_input.split())} lignes chargées")
    else:  # Voix
        st.button("Parle maintenant", on_click=lambda: None, key="voice_btn")
        st.markdown("<button onclick='startVoice()' class='neon-btn'>Activer le micro</button>", unsafe_allow_html=True)
        st.markdown("<p id='voice-output'></p>", unsafe_allow_html=True)
        data_input = st.text_input("Résultat voix", key="voice_result")

with col2:
    st.markdown("### Actions")
    if st.button("PURIFIER", type="primary"):
        if data_input:
            lines = [x.strip() for x in data_input.split("\n") if x.strip()]
            cleaned = []
            for line in lines:
                try:
                    p = parse(line, None)
                    if is_valid_number(p):
                        cleaned.append(format_number(p, PhoneNumberFormat.INTERNATIONAL))
                        continue
                except:
                    pass
                cleaned.append(line)
            
            st.session_state.cleaned = cleaned
            st.success(f"{len(cleaned)} éléments purifiés")
        else:
            st.warning("Aucune donnée")

# === RÉSULTATS ===
if 'cleaned' in st.session_state:
    st.markdown("### Résultats")
    df_out = pd.DataFrame({"Nettoyé": st.session_state.cleaned})
    st.dataframe(df_out, use_container_width=True)

    # AI Insights
    phones = [x for x in st.session_state.cleaned if x.startswith('+')]
    haiti = sum(1 for x in phones if x.startswith('+509'))
    st.info(f"IA : {len(phones)} numéros | {haiti} Haïti (+509) | {haiti/len(phones)*100:.1f}% local")

    # Exports
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        csv = "\n".join(st.session_state.cleaned)
        st.download_button("TXT", csv, "loopy_clean.txt", "text/plain")
    with col_dl2:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = [Paragraph("LOOPY DIOD v14.9 - Rapport", styles['Title'])]
        for item in st.session_state.cleaned[:100]:
            story.append(Paragraph(item, styles['Normal']))
            story.append(Spacer(1, 6))
        doc.build(story)
        st.download_button("PDF PRO", buffer.getvalue(), "loopy_report.pdf", "application/pdf")

# === FOOTER ===
st.markdown("---")
st.markdown("**Local** : `streamlit run app.py` | **Cloud** : GitHub + Streamlit Cloud")