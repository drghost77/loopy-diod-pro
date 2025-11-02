# LOOPY DIOD v21 - OPEN EMPIRE ULTRACLEAN
import streamlit as st
import pandas as pd
import io, base64, re
import plotly.express as px
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import phonenumbers
from phonenumbers import format_number, PhoneNumberFormat, is_valid_number, parse

# === UI SETUP ===
st.set_page_config(page_title="Loopy Diod v21", page_icon="🔮", layout="wide")

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

st.markdown("<h1 class='neon-text'>🔮 LOOPY DIOD <strong>v21</strong></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Open Data Lab • Déduplication & Formatage International</p>", unsafe_allow_html=True)

# === SIDEBAR ===
with st.sidebar:
    st.header("⚙️ OPTIONS")
    lang = st.selectbox("Langue", ["FR", "EN"])
    presets = st.selectbox("Preset Pays", ["Auto", "Haïti +509", "France +33", "USA +1", "Global"])
    dedup = st.checkbox("🗑️ Dédoublonner (recommandé)", True)
    format_type = st.selectbox("Format", ["International", "National", "E164"])
    batch_size = st.slider("Batch Max", 1000, 1000000, 10000)

# === TABS ===
tab1, tab2, tab3 = st.tabs(["📥 Input", "🚀 Purifier", "📊 Résultats"])

with tab1:
    st.markdown('<div class="glass">📤 Multi-Fichiers Batch</div>', unsafe_allow_html=True)
    files = st.file_uploader("Glisse fichiers", accept_multiple_files=True, type=['txt','csv','xlsx'])
    text_input = st.text_area("Ou colle tes données ici :", height=200)
    if st.button("Charger un exemple", key="sample"):
        text_input = "+50931456642\n+33123456789\n+50937214589\n+50937214589\nemail@test.com"

with tab2:
    if st.button("🔄 PURIFIER & DÉDOUBLER", type="primary"):
        if not text_input.strip():
            st.warning("⚠️ Aucun texte à purifier. Colle des données d'abord.")
        else:
            # --- Nettoyage de base ---
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

            # --- Déduplication ---
            if dedup:
                # Uniformise pour supprimer les doublons réels (ex: +50937214589 == +509 37 21 4589)
                def normalize_str(s): return re.sub(r'\D', '', s)
                unique = {}
                for num in cleaned:
                    key = normalize_str(num)
                    unique[key] = num  # garde dernière version formatée
                cleaned = list(unique.values())

            st.session_state.cleaned = cleaned
            st.session_state.invalid = invalid

            st.success(f"✅ {len(cleaned)} numéros purifiés ({len(invalid)} invalides).")
            st.balloons()

with tab3:
    if 'cleaned' in st.session_state:
        st.markdown('<div class="glass">📊 Visualisation</div>', unsafe_allow_html=True)
        df = pd.DataFrame({"Data": st.session_state.cleaned})
        fig = px.histogram(df, x="Data", title="Distribution des numéros uniques")
        st.plotly_chart(fig, use_container_width=True)

        share_data = base64.b64encode("\n".join(st.session_state.cleaned).encode()).decode()
        st.markdown(f"[**🔗 Lien de partage**](https://loopydiod.streamlit.app/?data={share_data})")

        st.download_button("💾 Télécharger TXT", "\n".join(st.session_state.cleaned), "loopy_clean.txt")

        if st.session_state.invalid:
            with st.expander("⚠️ Numéros invalides détectés"):
                st.write("\n".join(st.session_state.invalid))

# === FOOTER ===
st.markdown("<p style='text-align:center;'>v21 UltraClean • Déduplication intelligente • PWA Ready</p>", unsafe_allow_html=True)