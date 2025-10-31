# LOOPY DIOD v15 - CLEAN, STABLE, BEAUTIFUL
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
from phonenumbers import format_number, PhoneNumberFormat, is_valid_number, parse

# ========================================
# CONFIG & DESIGN
# ========================================
st.set_page_config(
    page_title="LOOPY DIOD v15",
    page_icon="",
    layout="wide"
)

# NEON CYBER DESIGN
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&display=swap');
    :root {
        --cyan: #00FFFF;
        --magenta: #FF00FF;
        --void: #0D1117;
        --gold: #FFD700;
    }
    body {
        background: var(--void);
        color: white;
        font-family: 'Orbitron', monospace;
    }
    .stApp { background: transparent !important; }
    .glass {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(20px);
        border: 1px solid var(--cyan);
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(0,255,255,0.3);
        margin: 1rem 0;
    }
    .neon-btn {
        background: linear-gradient(45deg, var(--cyan), var(--magenta));
        color: black !important;
        font-weight: bold;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        box-shadow: 0 0 20px var(--cyan);
    }
    .dropzone {
        border: 3px dashed var(--cyan);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s;
    }
    .dropzone:hover {
        background: rgba(0,255,255,0.1);
        border-color: var(--magenta);
    }
    .neon-text {
        background: linear-gradient(45deg, var(--cyan), var(--magenta), var(--gold));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 2.5rem;
        text-align: center;
    }
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(255,255,255,0.1);
        border: 1px solid var(--cyan);
        color: white;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ========================================
# VOICE INPUT (JS)
# ========================================
st.markdown("""
<script>
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = 'fr-FR';
recognition.onresult = (e) => {
    const text = e.results[0][0].transcript;
    document.getElementById('voice-output').value = text;
    Streamlit.setComponentValue(text);
};
function startVoice() {
    recognition.start();
}
</script>
""", unsafe_allow_html=True)

# ========================================
# HEADER
# ========================================
st.markdown("<h1 class='neon-text'>LOOPY DIOD v15</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; opacity:0.8; font-size:1.1rem;'>Nettoyage Global • IA • Export Pro • 100% Gratuit</p>", unsafe_allow_html=True)

# ========================================
# INPUT SECTION
# ========================================
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### Entrée de Données")
    input_method = st.radio("Choisis ta méthode", ["Texte", "Fichier", "Voix"], horizontal=True)

    data_input = ""

    if input_method == "Texte":
        data_input = st.text_area(
            "Colle tes données ici",
            height=180,
            placeholder="+509 31 45 66 42\ncontact@example.com\n+33 6 12 34 56 78"
        )
    elif input_method == "Fichier":
        uploaded = st.file_uploader(
            "Glisse ton fichier ici",
            type=['txt', 'csv', 'xlsx', 'pdf'],
            help="TXT, CSV, Excel, PDF"
        )
        if uploaded:
            try:
                if uploaded.type == "text/csv":
                    df = pd.read_csv(uploaded)
                elif "sheet" in uploaded.type:
                    df = pd.read_excel(uploaded)
                else:
                    content = uploaded.read().decode("utf-8", errors="ignore")
                    df = pd.DataFrame({"raw": [line for line in content.split("\n") if line.strip()]})
                data_input = "\n".join(df.iloc[:, 0].astype(str).dropna().tolist())
                st.success(f"{len(data_input.split())} lignes chargées")
            except Exception as e:
                st.error(f"Erreur de lecture: {e}")
    else:  # Voix
        st.markdown("<button onclick='startVoice()' class='neon-btn'>Activer le micro</button>", unsafe_allow_html=True)
        st.markdown("<textarea id='voice-output' style='width:100%; height:80px; background:rgba(255,255,255,0.1); border:1px solid var(--cyan); color:white; border-radius:12px; padding:12px; margin-top:10px;'></textarea>", unsafe_allow_html=True)
        voice_result = st.text_input("Résultat vocal", key="voice_result", label_visibility="collapsed")
        if voice_result:
            data_input = voice_result

with col2:
    st.markdown("### Action")
    if st.button("PURIFIER LES DONNÉES", type="primary", use_container_width=True):
        if data_input.strip():
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
            st.warning("Aucune donnée à traiter")

# ========================================
# RESULTS & AI INSIGHTS
# ========================================
if 'cleaned' in st.session_state:
    st.markdown("### Résultats Nettoyés")
    df_result = pd.DataFrame({"Nettoyé": st.session_state.cleaned})
    st.dataframe(df_result, use_container_width=True)

    # AI INSIGHTS (ZERO DIVISION FIXED)
    phones = [x for x in st.session_state.cleaned if x.startswith('+')]
    haiti_count = sum(1 for x in phones if x.startswith('+509'))

    st.markdown("### IA Insights")
    if len(phones) > 0:
        local_rate = (haiti_count / len(phones)) * 100
        st.info(f"{len(phones)} numéros détectés | {haiti_count} Haïti (+509) | {local_rate:.1f}% local")
    else:
        st.info("Aucun numéro de téléphone détecté.")

    # ========================================
    # EXPORTS
    # ========================================
    col_dl1, col_dl2 = st.columns(2)

    with col_dl1:
        txt_data = "\n".join(st.session_state.cleaned)
        st.download_button(
            label="TXT",
            data=txt_data,
            file_name="loopy_clean.txt",
            mime="text/plain"
        )

    with col_dl2:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = [
            Paragraph("LOOPY DIOD v15 - Rapport de Nettoyage", styles['Title']),
            Spacer(1, 12)
        ]
        for item in st.session_state.cleaned[:200]:
            story.append(Paragraph(item, styles['Normal']))
            story.append(Spacer(1, 6))
        doc.build(story)
        st.download_button(
            label="PDF PRO",
            data=buffer.getvalue(),
            file_name="loopy_report.pdf",
            mime="application/pdf"
        )

# ========================================
# FOOTER
# ========================================
st.markdown("---")
st.markdown("<p style='text-align:center; opacity:0.6; font-size:0.9rem;'>LOOPY DIOD v15 • Gratuit • Open Source • Made with</p>", unsafe_allow_html=True)