# LOOPY DIOD v22 - OPEN EMPIRE TELECOM ULTRACLEAN
import streamlit as st
import pandas as pd
import io, base64, re
import plotly.express as px
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import phonenumbers
from phonenumbers import format_number, PhoneNumberFormat, is_valid_number, parse

# === CONFIG GÉNÉRALE ===
st.set_page_config(page_title="Loopy Diod v22", page_icon="🔮", layout="wide")

# === STYLE VISUEL ===
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
:root { --cyan:#00FFFF; --magenta:#FF00FF; --void:#0D1117; }
body { background:var(--void); color:white; font-family:'Orbitron',monospace; }
.glass { background:rgba(255,255,255,0.08); backdrop-filter:blur(25px);
border:1px solid var(--cyan); border-radius:24px; padding:2rem; margin-top:1rem; }
.neon-text { background:linear-gradient(45deg,var(--cyan),var(--magenta));
-webkit-background-clip:text; -webkit-text-fill-color:transparent;
font-size:3rem; text-align:center; font-weight:900; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='neon-text'>🔮 LOOPY DIOD <strong>v22</strong></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Open Empire • Déduplication, Formatage & Classification Télécom</p>", unsafe_allow_html=True)

# === SIDEBAR ===
with st.sidebar:
    st.header("⚙️ OPTIONS")
    lang = st.selectbox("Langue", ["FR", "EN"])
    presets = st.selectbox("Preset Pays", ["Auto", "Haïti +509", "France +33", "USA +1", "Global"])
    dedup = st.checkbox("🗑️ Dédoublonner (recommandé)", True)
    format_type = st.selectbox("Format", ["International", "National", "E164"])
    batch_size = st.slider("Batch Max", 1000, 1000000, 10000)

# === LISTES TÉLÉCOM ===
DIGICEL_PREFIXES = {"31","34","36","37","38","39","44","45","46","47","48","49"}
NATCOM_PREFIXES = {"32","33","35","40","41","42","43","55"}

# === FONCTIONS UTILES ===
def normalize_str(s): 
    """Supprime tout sauf les chiffres pour comparaison"""
    return re.sub(r'\D', '', s)

def classify_509(num_str):
    """Retourne l'opérateur Digicel / Natcom / Autre"""
    num = normalize_str(num_str)
    if num.startswith("509") and len(num) >= 10:
        prefix = num[3:5]
        if prefix in DIGICEL_PREFIXES:
            return "Digicel"
        elif prefix in NATCOM_PREFIXES:
            return "Natcom"
    return "Autre"

# === TABS ===
tab1, tab2, tab3 = st.tabs(["📥 Input", "🚀 Purifier", "📊 Résultats"])

with tab1:
    st.markdown('<div class="glass">📤 Multi-Fichiers Batch</div>', unsafe_allow_html=True)
    files = st.file_uploader("Glisse fichiers", accept_multiple_files=True, type=['txt','csv','xlsx'])
    text_input = st.text_area("Ou colle tes données ici :", height=200)
    if st.button("Charger un exemple", key="sample"):
        text_input = "+50931456642\n+33123456789\n+50937214589\n+50937214589\n+50932112233\nemail@test.com"

with tab2:
    if st.button("🔄 PURIFIER & CLASSIFIER", type="primary"):
        if not text_input.strip():
            st.warning("⚠️ Aucun texte à purifier. Colle des données d'abord.")
        else:
            raw_lines = [re.sub(r'\s+', '', l.strip()) for l in text_input.split('\n') if l.strip()]
            cleaned, invalid = [], []
            country_hint = None

            # Choix pays
            if presets == "Haïti +509": country_hint = "HT"
            elif presets == "France +33": country_hint = "FR"
            elif presets == "USA +1": country_hint = "US"

            for l in raw_lines[:batch_size]:
                try:
                    p = parse(l, country_hint)
                    if is_valid_number(p):
                        fmt = (
                            PhoneNumberFormat.INTERNATIONAL if format_type=="International" else
                            PhoneNumberFormat.NATIONAL if format_type=="National" else
                            PhoneNumberFormat.E164
                        )
                        normalized = format_number(p, fmt)
                        cleaned.append(normalized)
                    else:
                        invalid.append(l)
                except:
                    invalid.append(l)

            # Déduplication intelligente
            if dedup:
                unique = {}
                for num in cleaned:
                    key = normalize_str(num)
                    unique[key] = num
                cleaned = list(unique.values())

            # Classification
            digicel_list = [n for n in cleaned if classify_509(n) == "Digicel"]
            natcom_list = [n for n in cleaned if classify_509(n) == "Natcom"]
            autres_list = [n for n in cleaned if classify_509(n) == "Autre"]

            # Sauvegarde
            st.session_state.cleaned = cleaned
            st.session_state.invalid = invalid
            st.session_state.digicel = digicel_list
            st.session_state.natcom = natcom_list
            st.session_state.autres = autres_list

            st.success(f"✅ {len(cleaned)} numéros purifiés ({len(invalid)} invalides).")
            st.info(f"📡 Digicel: {len(digicel_list)} • Natcom: {len(natcom_list)} • Autres: {len(autres_list)}")
            st.balloons()

with tab3:
    if 'cleaned' in st.session_state:
        st.markdown('<div class="glass">📊 Résultats Télécom</div>', unsafe_allow_html=True)
        df = pd.DataFrame({
            "Numéro": st.session_state.cleaned,
            "Opérateur": [classify_509(n) for n in st.session_state.cleaned]
        })
        fig = px.histogram(df, x="Opérateur", color="Opérateur", title="Répartition par opérateur")
        st.plotly_chart(fig, use_container_width=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.download_button("💾 Digicel.txt", "\n".join(st.session_state.digicel), "digicel.txt")
        with col2:
            st.download_button("💾 Natcom.txt", "\n".join(st.session_state.natcom), "natcom.txt")
        with col3:
            st.download_button("💾 Tous.txt", "\n".join(st.session_state.cleaned), "all_clean.txt")

        if st.session_state.invalid:
            with st.expander("⚠️ Numéros invalides détectés"):
                st.write("\n".join(st.session_state.invalid))

# === FOOTER ===
st.markdown("<p style='text-align:center;'>v22 UltraClean • Classification Télécom • Déduplication intelligente • PWA Ready</p>", unsafe_allow_html=True)