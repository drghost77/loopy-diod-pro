# LOOPY DIOD v15 – GRATUIT & PRÊT
import streamlit as st
import pandas as pd
import re
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import phonenumbers
from phonenumbers import format_number, PhoneNumberFormat, is_valid_number, parse

# CONFIG
st.set_page_config(page_title="LOOPY DIOD v15", layout="wide", page_icon="")

# DESIGN NEON
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&display=swap');
    :root { --cyan: #00FFFF; --magenta: #FF00FF; --void: #0D1117; }
    body { background: var(--void); color: white; font-family: 'Orbitron', monospace; }
    .glass { background: rgba(255,255,255,0.05); backdrop-filter: blur(20px); border: 1px solid var(--cyan); border-radius: 20px; padding: 1.5rem; margin: 1rem 0; }
    .neon-btn { background: linear-gradient(45deg, var(--cyan), var(--magenta)); color: black !important; font-weight: bold; border: none; border-radius: 12px; padding: 12px 24px; }
    .neon-text { background: linear-gradient(45deg, var(--cyan), var(--magenta), #FFD700); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; text-align: center; font-size: 2.8rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='neon-text'>LOOPY DIOD v15</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; opacity:0.8;'>Nettoyage Global • IA • Export Pro • <strong>100% GRATUIT</strong></p>", unsafe_allow_html=True)

# INPUT
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("### Entrée")
    method = st.radio("Méthode", ["Texte", "Fichier"], horizontal=True)
    data = ""

    if method == "Texte":
        data = st.text_area("Colle ici", height=180, placeholder="+509 31 45 66 42")
    else:
        file = st.file_uploader("Upload", type=['txt','csv','xlsx'])
        if file:
            if file.type == "text/csv":
                df = pd.read_csv(file)
            elif "sheet" in file.type:
                df = pd.read_excel(file)
            else:
                df = pd.DataFrame({"raw": file.read().decode().split("\n")})
            data = "\n".join(df.iloc[:,0].astype(str).dropna().tolist())
            st.success(f"{len(data.split())} lignes")

with col2:
    st.markdown("### Action")
    if st.button("PURIFIER", type="primary", use_container_width=True):
        if data.strip():
            lines = [x.strip() for x in data.split("\n") if x.strip()]
            cleaned = []
            for line in lines:
                try:
                    p = parse(line, None)
                    if is_valid_number(p):
                        cleaned.append(format_number(p, PhoneNumberFormat.INTERNATIONAL))
                        continue
                except: pass
                cleaned.append(line)
            st.session_state.cleaned = cleaned
            st.success(f"{len(cleaned)} purifiés")
        else:
            st.warning("Données vides")

# RÉSULTATS
if 'cleaned' in st.session_state:
    st.markdown("### Résultats")
    df_out = pd.DataFrame({"Nettoyé": st.session_state.cleaned})
    st.dataframe(df_out, use_container_width=True)

    # IA
    phones = [x for x in st.session_state.cleaned if x.startswith('+')]
    haiti = sum(1 for x in phones if x.startswith('+509'))
    if phones:
        st.info(f"{len(phones)} numéros | {haiti} Haïti | {haiti/len(phones)*100:.1f}% local")
    else:
        st.info("Aucun numéro détecté.")

    # EXPORT
    col1, col2 = st.columns(2)
    with col1:
        st.download_button("TXT", "\n".join(st.session_state.cleaned), "loopy.txt", "text/plain")
    with col2:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = [Paragraph("LOOPY DIOD v15", styles['Title'])]
        for item in st.session_state.cleaned[:100]:
            story.append(Paragraph(item, styles['Normal']))
        doc.build(story)
        st.download_button("PDF", buffer.getvalue(), "loopy.pdf", "application/pdf")

st.markdown("---")
st.markdown("<p style='text-align:center; opacity:0.6;'>Gratuit • Open • Made with</p>", unsafe_allow_html=True)