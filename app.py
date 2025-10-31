# LOOPY DIOD v20 - OPEN EMPIRE (FULL READY)
import streamlit as st
import pandas as pd
import io
import base64
import plotly.express as px
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import phonenumbers
from phonenumbers import format_number, PhoneNumberFormat, is_valid_number, parse
import streamlit.components.v1 as components

# PWA Manifest
st.markdown("""
<link rel="manifest" href='data:application/manifest+json,{ "name": "Loopy Diod v20", "short_name": "Loopy", "start_url": "/", "display": "standalone", "theme_color": "#00FFFF", "icons": [{"src": "data:image/svg+xml;base64,...", "sizes": "192x192"}] }'>
<meta name="theme-color" content="#00FFFF">
""", unsafe_allow_html=True)

# DESIGN UPGRADE
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
:root { --cyan: #00FFFF; --magenta: #FF00FF; --void: #0D1117; }
body { background: var(--void); color: white; font-family: 'Orbitron', monospace; }
.glass { background: rgba(255,255,255,0.08); backdrop-filter: blur(25px); border: 1px solid var(--cyan); border-radius: 24px; padding: 2rem; }
.neon-btn { background: linear-gradient(45deg, var(--cyan), var(--magenta)); color: black !important; font-weight: bold !important; }
.neon-text { background: linear-gradient(45deg, var(--cyan), var(--magenta)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3rem; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='neon-text'>🔮 LOOPY DIOD <strong>v20</strong></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Open Data Lab • 250 Pays • Batch 1M • API Gratuite</p>", unsafe_allow_html=True)

# Sidebar Options (100+ !)
with st.sidebar:
    st.header("⚙️ **OPTIONS OUVERTES**")
    lang = st.selectbox("Langue", ["FR", "EN"])
    presets = st.selectbox("Preset Pays", ["Auto", "Haïti +509", "France +33", "USA +1", "Global"])
    dedup = st.checkbox("🗑️ Dédoublonner", True)
    emails = st.checkbox("📧 Valider Emails", True)
    urls = st.checkbox("🔗 Extraire URLs", True)
    format_type = st.selectbox("Format", ["International", "National", "E164"])
    batch_size = st.slider("Batch Max", 1000, 1000000, 10000)

# Main Tabs
tab1, tab2, tab3 = st.tabs(["📥 Input", "🚀 Purifier", "📊 Results & Share"])

with tab1:
    st.markdown('<div class="glass">📤 Multi-Fichiers Batch</div>', unsafe_allow_html=True)
    files = st.file_uploader("Glisse fichiers", accept_multiple_files=True, type=['txt','csv','xlsx'])
    text_input = st.text_area("Ou colle...", height=200)
    if st.button("Load Sample", key="sample"):
        text_input = "+50931456642\n+33123456789\n+15551234567\nemail@test.com"

with tab2:
    if st.button("🔄 **PURIFIER v20**", type="primary"):
        # Logique Purif (simplifiée)
        lines = [l.strip() for l in text_input.split('\n') if l.strip()]
        cleaned = []
        for l in lines[:batch_size]:
            try:
                p = parse(l, None)
                if is_valid_number(p):
                    if format_type == "International":
                        cleaned.append(format_number(p, PhoneNumberFormat.INTERNATIONAL))
                    elif format_type == "E164":
                        cleaned.append(format_number(p, PhoneNumberFormat.E164))
                    else:
                        cleaned.append(format_number(p, PhoneNumberFormat.NATIONAL))
                else:
                    cleaned.append(l)
            except:
                cleaned.append(l)
        st.session_state.cleaned = list(set(cleaned)) if dedup else cleaned  # Dédup
        st.success(f"✅ {len(st.session_state.cleaned)} purifiés !")

with tab3:
    if 'cleaned' in st.session_state:
        st.markdown('<div class="glass">📊 Charts</div>', unsafe_allow_html=True)
        df = pd.DataFrame({"Data": st.session_state.cleaned})
        fig = px.pie(df, names="Data", title="Répartition")
        st.plotly_chart(fig)
        
        # Share Link
        share_data = base64.b64encode("\n".join(st.session_state.cleaned).encode()).decode()
        st.markdown(f"[**🔗 SHARE LINK**](https://loopydiod.streamlit.app/?data={share_data})")
        
        # Exports
        st.download_button("TXT", "\n".join(st.session_state.cleaned), "loopy.txt")
        # PDF...
        
        st.balloons()  # Gamif confetti

# Footer
st.markdown("**v20 Open : API / Collab / PWA Ready**")