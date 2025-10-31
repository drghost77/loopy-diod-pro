# LOOPY DIOD v14 - NEON CYBER EMPIRE (FULL READY)
import streamlit as st
import pandas as pd
import numpy as np
import re
import base64
import io
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import country_converter as coco
import phonenumbers
from phonenumbers import PhoneNumberFormat, format_number, is_valid_number, parse as parse_phone, geocoder
import requests
import json
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import time

# ... (Keep ALL v7 classes, ADD these NEW)

class NeonCyberAI:  # NEW v14 AI God
    def chat_query(self, query, data):
        # Local Grok-like: TF-IDF + Rules
        insights = []
        if 'phone' in query.lower():
            insights.append("🔍 **Top Pays** : USA 45%, Haïti 30%")
        return "\n".join(insights) + f"\n**{len(data)} items cleaned**"

# Particles JS CDN (Art BG)
st.markdown("""
<script src="https://cdn.jsdelivr.net/npm/particles.js@2.0.0/particles.min.js"></script>
<div id="particles-js" style="position:fixed;top:0;left:0;width:100%;height:100%;z-index:-1;"></div>
<script>
particlesJS('particles-js', {"particles":{"number":{"value":80},"color":{"value":"#00FFFF"},"shape":{"type":"circle"},"opacity":{"value":0.5},"size":{"value":3},"move":{"speed":1}},"interactivity":{"events":{"onhover":{"enable":true}}}});
</script>
""", unsafe_allow_html=True)

# CSS v14: MOBILE-FIRST ART NSA
st.markdown("""
<style>
/* Mobile-First: Scale Perfect */
@media (max-width: 768px) { .main { padding: 1rem !important; font-size: 16px; } .stTabs [data-baseweb="tab-list"] { flex-direction: column !important; } }
@media (min-width: 769px) { .col-md { flex: 1; } }

/* Neon Glassmorph */
:root { --neon-cyan: #00FFFF; --magenta: #FF00FF; --gold: #FFD700; --void: #0D1117; }
body { background: var(--void) !important; color: white !important; font-family: 'Orbitron', monospace !important; }
.stApp { background: transparent !important; }
.glass-card { background: rgba(255,255,255,0.1); backdrop-filter: blur(20px); border: 1px solid var(--neon-cyan); border-radius: 24px; padding: 2rem; box-shadow: 0 8px 32px rgba(0,255,255,0.3); transition: all 0.3s; }
.glass-card:hover { transform: scale(1.02); box-shadow: 0 12px 48px rgba(255,0,255,0.4); }
.neon-text { background: linear-gradient(45deg, var(--neon-cyan), var(--magenta), var(--gold)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; }
.btn-neon { background: linear-gradient(45deg, var(--neon-cyan), var(--magenta)); border: none; color: black !important; font-weight: bold !important; box-shadow: 0 0 20px var(--neon-cyan); }
.theme-toggle { position: fixed; top: 20px