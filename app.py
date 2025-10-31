import streamlit as st
import pandas as pd
import numpy as np
import re
import base64
import io
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import country_converter as coco
import phonenumbers
from phonenumbers import PhoneNumberFormat, format_number, is_valid_number, parse as parse_phone
import requests
import json

# =============================================================================
# CONFIGURATION GLOBALE - DESIGN SYSTÈME
# =============================================================================

st.set_page_config(
    page_title="🔮 LOOPY DIOD v7 - Intelligence Platform",
    page_icon="🌀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Design System - Bleu Roi & Minimaliste
ROYAL_BLUE = "#002FA7"
WHITE = "#FFFFFF"
LIGHT_BLUE = "#E6F0FF"
DARK_BG = "#0A0A14"
ACCENT_GREEN = "#00D4AA"
ACCENT_ORANGE = "#FF6B35"

st.markdown(f"""
<style>
    /* Reset et base */
    .main .block-container {{
        padding-top: 2rem;
        max-width: 95%;
    }}
    
    /* Thème principal */
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(135deg, {DARK_BG} 0%, #1A1A2E 50%, #16213E 100%);
        color: {WHITE};
    }}
    
    .stApp {{
        background: transparent;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    
    /* En-tête élégant */
    .main-header {{
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, {ROYAL_BLUE}20 0%, {ROYAL_BLUE}40 100%);
        border-radius: 24px;
        margin-bottom: 3rem;
        border: 1px solid {ROYAL_BLUE}40;
        backdrop-filter: blur(10px);
    }}
    
    /* Cartes modernes */
    .feature-card {{
        background: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid {ROYAL_BLUE}30;
        backdrop-filter: blur(8px);
        transition: all 0.3s ease;
    }}
    
    .feature-card:hover {{
        transform: translateY(-4px);
        border-color: {ROYAL_BLUE}60;
        box-shadow: 0 8px 32px {ROYAL_BLUE}20;
    }}
    
    /* Boutons premium */
    .stButton > button {{
        background: linear-gradient(135deg, {ROYAL_BLUE}, #0040CC);
        color: {WHITE};
        border: none;
        border-radius: 12px;
        padding: 12px 28px;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.3s ease;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px {ROYAL_BLUE}40;
    }}
    
    /* Métriques élégantes */
    .metric-card {{
        background: rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        border-left: 4px solid {ROYAL_BLUE};
    }}
    
    /* Badges de classification */
    .classification-badge {{
        display: inline-block;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin: 2px;
        background: {ROYAL_BLUE}20;
        border: 1px solid {ROYAL_BLUE}40;
        color: {WHITE};
    }}
    
    /* Sidebar améliorée */
    .css-1d391kg {{
        background: rgba(10, 10, 20, 0.95) !important;
    }}
    
    /* Inputs modernes */
    .stTextInput > div > div > input, 
    .stTextArea > div > div > textarea {{
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid {ROYAL_BLUE}40;
        border-radius: 12px;
        color: {WHITE};
        padding: 12px 16px;
    }}
    
    .stSelectbox > div > div {{
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid {ROYAL_BLUE}40;
        border-radius: 12px;
        color: {WHITE};
    }}
    
    /* Animations subtiles */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .fade-in {{
        animation: fadeIn 0.6s ease-out;
    }}
</style>
""", unsafe_allow_html=True)

# =============================================================================
# SYSTÈME INTELLIGENT DE CLASSIFICATION v7
# =============================================================================

class IntelligentClassifier:
    def __init__(self):
        self.country_converter = coco.CountryConverter()
        self.initialize_classification_rules()
    
    def initialize_classification_rules(self):
        self.rules = {
            "🌍 Téléphones Internationaux": {
                "patterns": [r'^\+?[1-9]\d{0,3}'],
                "subcategories": {
                    "🇭🇹 Haïti": {"patterns": [r'^\+?509'], "color": "#FF6B6B"},
                    "🇫🇷 France": {"patterns": [r'^\+?33'], "color": "#4ECDC4"},
                    "🇺🇸 USA/Canada": {"patterns": [r'^\+?1'], "color": "#45B7D1"},
                    "🇧🇪 Belgique": {"patterns": [r'^\+?32'], "color": "#FFD93D"},
                    "🇨🇭 Suisse": {"patterns": [r'^\+?41'], "color": "#6BCF7F"},
                },
                "color": ROYAL_BLUE
            },
            "📧 Communications Électroniques": {
                "patterns": [r'@', r'^[\w\.-]+@[\w\.-]+\.\w+$'],
                "subcategories": {
                    "💼 Professionnels": {"patterns": [r'@(gmail|yahoo|hotmail|outlook)\.'], "color": "#96CEB4"},
                    "🏢 Entreprises": {"patterns": [r'@(entreprise|societe|company|corp|inc)\.'], "color": "#FFEAA7"},
                    "🎓 Éducation": {"patterns": [r'@(edu|ac\.|univ|school)\.'], "color": "#A29BFE"},
                },
                "color": ACCENT_GREEN
            },
            "🌐 Contenus Numériques": {
                "patterns": [r'^https?://', r'^www\.', r'\.(com|org|net|io|ai)$'],
                "subcategories": {
                    "🔗 Sites Web": {"patterns": [r'^https?://'], "color": "#DDA0DD"},
                    "📱 Applications": {"patterns": [r'\.(app|io|ai)$'], "color": "#FFA07A"},
                    "🛒 E-commerce": {"patterns": [r'(shop|store|market|buy)\.'], "color": "#20B2AA"},
                },
                "color": "#BA55D3"
            },
            "🔢 Identifiants Structurés": {
                "patterns": [r'^[A-Z]{2,4}\d{3,6}$', r'^[A-Z]+-\d+$', r'^[A-Z]+\d+[A-Z]+$'],
                "subcategories": {
                    "📦 Codes Produits": {"patterns": [r'^(PROD|ITEM|SKU|REF)[_-]'], "color": "#98D8C8"},
                    "👤 Identifiants": {"patterns": [r'^(ID|USER|EMP)[_-]'], "color": "#F7DC6F"},
                    "🏷️ Références": {"patterns": [r'^(REF|CODE|NUM)[_-]'], "color": "#BB8FCE"},
                },
                "color": "#F39C12"
            },
            "👥 Réseaux Sociaux": {
                "patterns": [r'^@[\w\.]+$', r'instagram\.com/', r'facebook\.com/', r'twitter\.com/'],
                "subcategories": {
                    "📸 Instagram": {"patterns": [r'instagram\.com/'], "color": "#E1306C"},
                    "👥 Facebook": {"patterns": [r'facebook\.com/'], "color": "#4267B2"},
                    "🐦 Twitter/X": {"patterns": [r'twitter\.com/'], "color": "#1DA1F2"},
                },
                "color": "#405DE6"
            }
        }
    
    def classify_item(self, item, user_country_code=None):
        """Classification intelligente multi-niveaux"""
        item_str = str(item).strip().lower()
        
        # Niveau 1: Classification principale
        for main_category, main_rules in self.rules.items():
            for pattern in main_rules["patterns"]:
                if re.search(pattern, item_str, re.IGNORECASE):
                    # Niveau 2: Sous-classification
                    subcategory, subcolor = self.get_subclassification(item_str, main_rules["subcategories"])
                    
                    return {
                        "main_category": main_category,
                        "subcategory": subcategory,
                        "main_color": main_rules["color"],
                        "sub_color": subcolor,
                        "confidence": self.calculate_confidence(item_str, pattern)
                    }
        
        # Classification par défaut avec analyse contextuelle
        return self.contextual_classification(item_str, user_country_code)
    
    def get_subclassification(self, item, subcategories):
        """Détermine la sous-catégorie précise"""
        for sub_name, sub_rules in subcategories.items():
            for pattern in sub_rules["patterns"]:
                if re.search(pattern, item, re.IGNORECASE):
                    return sub_name, sub_rules["color"]
        return "Autre", "#95A5A6"
    
    def calculate_confidence(self, item, pattern):
        """Calcule le niveau de confiance de la classification"""
        match_strength = len(re.findall(pattern, item, re.IGNORECASE))
        length_factor = min(len(item) / 50, 1.0)
        return min(match_strength * 0.3 + length_factor * 0.7, 1.0)
    
    def contextual_classification(self, item, user_country_code):
        """Classification contextuelle avancée"""
        # Analyse de la structure
        if len(item) <= 5 and item.isalnum():
            return {
                "main_category": "🔤 Codes Courts",
                "subcategory": "Code simple",
                "main_color": "#7F8C8D",
                "sub_color": "#95A5A6",
                "confidence": 0.7
            }
        elif len(item.split()) >= 3:
            return {
                "main_category": "📝 Textes Libres",
                "subcategory": "Phrase ou description",
                "main_color": "#34495E",
                "sub_color": "#5D6D7E",
                "confidence": 0.6
            }
        else:
            return {
                "main_category": "❓ Non Classifié",
                "subcategory": "À analyser",
                "main_color": "#566573",
                "sub_color": "#7B7D7D",
                "confidence": 0.3
            }

# =============================================================================
# MOTEUR DE PURIFICATION INTELLIGENTE
# =============================================================================

class DataPurificationEngine:
    def __init__(self):
        self.classifier = IntelligentClassifier()
    
    def normalize_phone_number(self, phone, target_country_code="FR"):
        """Normalisation avancée des numéros de téléphone"""
        try:
            if not phone or pd.isna(phone):
                return None, 0
            
            # Nettoyage initial
            cleaned = re.sub(r'[^\d+]', '', str(phone))
            
            # Conversion des formats internationaux
            if cleaned.startswith('00'):
                cleaned = '+' + cleaned[2:]
            elif cleaned.startswith('0') and len(cleaned) > 6:
                cleaned = '+33' + cleaned[1:]  # France par défaut
            
            # Validation avec phonenumbers
            try:
                parsed = parse_phone(cleaned, None)
                if is_valid_number(parsed):
                    formatted = format_number(parsed, PhoneNumberFormat.INTERNATIONAL)
                    return formatted, 1.0
            except:
                pass
            
            # Validation basique
            if re.match(r'^\+?[\d\s\-\(\)]{8,20}$', cleaned):
                return cleaned, 0.8
                
            return None, 0
            
        except Exception:
            return None, 0
    
    def validate_and_correct_email(self, email):
        """Validation et correction intelligente d'email"""
        try:
            email = str(email).strip().lower()
            
            # Pattern de validation
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(pattern, email):
                return None, 0.0, "Format invalide"
            
            # Vérification des domaines courants avec suggestions
            common_domains = {
                'gmil.com': 'gmail.com',
                'gmai.com': 'gmail.com',
                'gmal.com': 'gmail.com',
                'yahooo.com': 'yahoo.com',
                'hotmal.com': 'hotmail.com',
                'outlok.com': 'outlook.com'
            }
            
            user, domain = email.split('@')
            if domain in common_domains:
                suggestion = f"{user}@{common_domains[domain]}"
                return suggestion, 0.7, "Correction de domaine suggérée"
            
            return email, 1.0, "Email valide"
            
        except Exception:
            return None, 0.0, "Erreur de validation"
    
    def extract_and_validate_url(self, text):
        """Extraction et validation d'URLs"""
        url_pattern = r'https?://[^\s]+|www\.[^\s]+'
        urls = re.findall(url_pattern, text)
        
        validated_urls = []
        for url in urls:
            if not url.startswith('http'):
                url = 'https://' + url
            validated_urls.append(url)
        
        return validated_urls
    
    def advanced_data_cleaning(self, data_list, cleaning_options):
        """Nettoyage avancé des données avec options configurables"""
        cleaned_data = []
        stats = {
            'total_processed': len(data_list),
            'valid_phones': 0,
            'valid_emails': 0,
            'valid_urls': 0,
            'corrected_items': 0,
            'removed_duplicates': 0
        }
        
        seen_items = set()
        
        for item in data_list:
            original_item = str(item).strip()
            if not original_item:
                continue
            
            processed_item = original_item
            validation_score = 1.0
            correction_note = ""
            
            # Application des règles de nettoyage
            if cleaning_options.get('normalize_phones', True):
                phone_result, phone_score = self.normalize_phone_number(original_item)
                if phone_result:
                    processed_item = phone_result
                    validation_score = phone_score
                    stats['valid_phones'] += 1
            
            if cleaning_options.get('validate_emails', True) and '@' in original_item:
                email_result, email_score, email_note = self.validate_and_correct_email(original_item)
                if email_result:
                    processed_item = email_result
                    validation_score = email_score
                    correction_note = email_note
                    stats['valid_emails'] += 1
                    if original_item != email_result:
                        stats['corrected_items'] += 1
            
            # Suppression des doublons
            if cleaning_options.get('remove_duplicates', True):
                item_key = processed_item.lower().strip()
                if item_key in seen_items:
                    stats['removed_duplicates'] += 1
                    continue
                seen_items.add(item_key)
            
            # Classification
            classification = self.classifier.classify_item(processed_item)
            
            cleaned_data.append({
                'original': original_item,
                'processed': processed_item,
                'classification': classification,
                'validation_score': validation_score,
                'correction_note': correction_note
            })
        
        stats['final_count'] = len(cleaned_data)
        return cleaned_data, stats

# =============================================================================
# SYSTÈME D'ANALYSE STATISTIQUE AVANCÉE
# =============================================================================

class AdvancedAnalytics:
    def __init__(self):
        self.colors = [ROYAL_BLUE, ACCENT_GREEN, ACCENT_ORANGE, "#BA55D3", "#F39C12"]
    
    def create_classification_chart(self, classified_data):
        """Crée un graphique de classification interactif"""
        categories = {}
        for item in classified_data:
            main_cat = item['classification']['main_category']
            sub_cat = item['classification']['subcategory']
            
            if main_cat not in categories:
                categories[main_cat] = {}
            if sub_cat not in categories[main_cat]:
                categories[main_cat][sub_cat] = 0
            categories[main_cat][sub_cat] += 1
        
        # Préparation des données pour le graphique
        main_categories = list(categories.keys())
        subcategories_data = []
        
        for main_cat, subs in categories.items():
            for sub_cat, count in subs.items():
                subcategories_data.append({
                    'Main Category': main_cat,
                    'Subcategory': sub_cat,
                    'Count': count
                })
        
        df = pd.DataFrame(subcategories_data)
        
        if df.empty:
            return None
        
        # Création du graphique sunburst
        fig = px.sunburst(
            df, 
            path=['Main Category', 'Subcategory'], 
            values='Count',
            color='Main Category',
            color_discrete_sequence=self.colors,
            title="📊 Classification Hiérarchique des Données"
        )
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color=WHITE,
            title_font_color=WHITE
        )
        
        return fig
    
    def create_quality_metrics(self, stats):
        """Crée des indicateurs de qualité visuels"""
        metrics_data = {
            'Metric': ['Taux de Validation', 'Données Uniques', 'Éléments Corrigés', 'Taux de Classification'],
            'Value': [
                (stats['final_count'] / stats['total_processed']) * 100 if stats['total_processed'] > 0 else 0,
                ((stats['final_count'] - stats['removed_duplicates']) / stats['total_processed']) * 100 if stats['total_processed'] > 0 else 0,
                (stats['corrected_items'] / stats['total_processed']) * 100 if stats['total_processed'] > 0 else 0,
                85  # Taux de classification estimé
            ]
        }
        
        df = pd.DataFrame(metrics_data)
        fig = px.bar(
            df, 
            x='Metric', 
            y='Value',
            color='Metric',
            color_discrete_sequence=self.colors,
            title="📈 Métriques de Qualité des Données"
        )
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color=WHITE,
            title_font_color=WHITE,
            showlegend=False
        )
        
        fig.update_traces(
            texttemplate='%{y:.1f}%',
            textposition='outside'
        )
        
        return fig

# =============================================================================
# INTERFACE UTILISATEUR v7 - PLATEFORME INTELLIGENTE
# =============================================================================

def main():
    # Initialisation des moteurs
    purification_engine = DataPurificationEngine()
    analytics_engine = AdvancedAnalytics()
    
    # En-tête principal élégant
    st.markdown("""
    <div class="main-header fade-in">
        <h1 style="margin:0; font-size:3.5em; background:linear-gradient(135deg, #FFFFFF, #E6F0FF); 
                   -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
            🌀 LOOPY DIOD v7
        </h1>
        <p style="margin:0; font-size:1.3em; opacity:0.9; font-weight:300;">
            Plateforme Intelligente de Purification & Classification
        </p>
        <p style="margin-top:1rem; opacity:0.7; font-size:0.9em;">
            Transformez vos données brutes en informations actionnables
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar avancée
    with st.sidebar:
        st.markdown("### ⚙️ Modules Actifs")
        
        # Modules configurables
        modules = {
            '🧹 Purification Avancée': st.checkbox("Purification", True, help="Nettoyage et validation des données"),
            '🏷️ Classification Intelligente': st.checkbox("Classification", True, help="Catégorisation automatique"),
            '📊 Analytics Temps Réel': st.checkbox("Analytics", True, help="Analyse et visualisation"),
            '🌍 Géo-localisation': st.checkbox("Géo-localisation", False, help="Analyse géographique"),
            '🤖 IA Assistante': st.checkbox("Assistant IA", False, help="Suggestions intelligentes")
        }
        
        st.markdown("---")
        st.markdown("### 🎯 Paramètres de Purification")
        
        purification_options = {
            'normalize_phones': st.checkbox("Normaliser téléphones", True),
            'validate_emails': st.checkbox("Valider emails", True),
            'extract_urls': st.checkbox("Extraire URLs", True),
            'remove_duplicates': st.checkbox("Supprimer doublons", True),
            'auto_correct': st.checkbox("Correction auto", True)
        }
        
        st.markdown("---")
        st.markdown("### 🌐 Paramètres Internationaux")
        
        country_codes = ["FR", "US", "HT", "BE", "CH", "CA", "GB", "DE"]
        selected_country = st.selectbox(
            "Code pays par défaut",
            country_codes,
            index=0,
            help="Code pays pour la normalisation des numéros"
        )
        
        st.markdown("---")
        st.markdown("### 💾 Format d'Export")
        
        export_format = st.radio(
            "Format de sortie",
            ["CSV", "Excel", "JSON", "TXT"],
            horizontal=True
        )
    
    # Layout principal en onglets
    tab1, tab2, tab3, tab4 = st.tabs([
        "🚀 Import & Traitement", 
        "📊 Analytics Avancés", 
        "🎯 Résultats Détaillés", 
        "⚡ Export Intelligent"
    ])
    
    # Onglet 1: Import & Traitement
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 📥 Source des Données")
            
            input_method = st.radio(
                "Méthode d'import",
                ["Saisie directe", "Upload fichier", "URL externe"],
                horizontal=True
            )
            
            if input_method == "Saisie directe":
                input_data = st.text_area(
                    "Collez vos données (1 par ligne):",
                    height=300,
                    placeholder="+509 31 45 6642\ncontact@example.com\nhttps://site.com\n+33 1 23 45 67 89\nPROD_001\n@utilisateur",
                    help="Collez vos données brutes - une par ligne"
                )
                data_list = [line.strip() for line in input_data.split('\n') if line.strip()]
                
            elif input_method == "Upload fichier":
                uploaded_file = st.file_uploader(
                    "Choisissez un fichier",
                    type=['csv', 'txt', 'xlsx', 'json'],
                    help="Formats supportés: CSV, TXT, Excel, JSON"
                )
                
                if uploaded_file:
                    try:
                        if uploaded_file.type == "text/csv":
                            df = pd.read_csv(uploaded_file)
                            data_list = df.iloc[:, 0].astype(str).tolist()
                        elif uploaded_file.type.endswith('sheet'):
                            df = pd.read_excel(uploaded_file)
                            data_list = df.iloc[:, 0].astype(str).tolist()
                        elif uploaded_file.type == "application/json":
                            data = json.load(uploaded_file)
                            data_list = data if isinstance(data, list) else list(data.values())
                        else:
                            content = uploaded_file.getvalue().decode()
                            data_list = [line.strip() for line in content.split('\n') if line.strip()]
                            
                        st.success(f"✅ {len(data_list)} éléments chargés")
                    except Exception as e:
                        st.error(f"❌ Erreur de chargement: {str(e)}")
                        data_list = []
                else:
                    data_list = []
            
            else:  # URL externe
                url = st.text_input("URL des données", placeholder="https://exemple.com/donnees.csv")
                if url:
                    try:
                        response = requests.get(url)
                        data_list = response.text.split('\n')
                        st.success(f"✅ {len(data_list)} éléments chargés depuis l'URL")
                    except:
                        st.error("❌ Impossible de charger les données depuis l'URL")
                        data_list = []
        
        with col2:
            st.markdown("### ⚡ Traitement Instantané")
            
            if st.button("🌀 DÉMARRER LA PURIFICATION", use_container_width=True):
                if data_list:
                    with st.spinner("🔮 Purification intelligente en cours..."):
                        # Traitement des données
                        cleaned_data, stats = purification_engine.advanced_data_cleaning(
                            data_list, 
                            purification_options
                        )
                        
                        # Stockage en session
                        st.session_state.cleaned_data = cleaned_data
                        st.session_state.stats = stats
                        st.session_state.processed = True
                        
                    st.success(f"✨ Purification terminée: {len(cleaned_data)} éléments optimisés")
                    
                    # Métriques rapides
                    col_metric1, col_metric2, col_metric3 = st.columns(3)
                    with col_metric1:
                        st.metric("Entrées", stats['total_processed'])
                    with col_metric2:
                        st.metric("Sorties", stats['final_count'])
                    with col_metric3:
                        efficiency = (stats['final_count'] / stats['total_processed']) * 100
                        st.metric("Efficacité", f"{efficiency:.1f}%")
                else:
                    st.warning("⚠️ Veuillez fournir des données à traiter")
    
    # Onglet 2: Analytics Avancés
    with tab2:
        if st.session_state.get('processed', False):
            st.markdown("### 📈 Analytics Intelligents")
            
            cleaned_data = st.session_state.cleaned_data
            stats = st.session_state.stats
            
            # Graphiques principaux
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                classification_chart = analytics_engine.create_classification_chart(cleaned_data)
                if classification_chart:
                    st.plotly_chart(classification_chart, use_container_width=True)
            
            with col_chart2:
                quality_chart = analytics_engine.create_quality_metrics(stats)
                if quality_chart:
                    st.plotly_chart(quality_chart, use_container_width=True)
            
            # Métriques détaillées
            st.markdown("### 📊 Métriques Détaillées")
            
            metric_cols = st.columns(4)
            with metric_cols[0]:
                st.metric("📞 Téléphones valides", stats.get('valid_phones', 0))
            with metric_cols[1]:
                st.metric("📧 Emails valides", stats.get('valid_emails', 0))
            with metric_cols[2]:
                st.metric("🔗 URLs extraites", stats.get('valid_urls', 0))
            with metric_cols[3]:
                st.metric("🔄 Éléments corrigés", stats.get('corrected_items', 0))
        
        else:
            st.info("🎯 Traitez d'abord vos données dans l'onglet 'Import & Traitement'")
    
    # Onglet 3: Résultats Détaillés
    with tab3:
        if st.session_state.get('processed', False):
            st.markdown("### 🎯 Résultats de la Purification")
            
            cleaned_data = st.session_state.cleaned_data
            
            # Filtres interactifs
            col_filter1, col_filter2, col_filter3 = st.columns(3)
            
            with col_filter1:
                categories = list(set([item['classification']['main_category'] for item in cleaned_data]))
                selected_category = st.selectbox("Filtrer par catégorie", ["Toutes"] + categories)
            
            with col_filter2:
                min_confidence = st.slider("Confiance minimale", 0.0, 1.0, 0.5, 0.1)
            
            with col_filter3:
                sort_by = st.selectbox("Trier par", ["Confiance", "Catégorie", "Original"])
            
            # Application des filtres
            filtered_data = cleaned_data
            if selected_category != "Toutes":
                filtered_data = [item for item in filtered_data 
                               if item['classification']['main_category'] == selected_category]
            
            filtered_data = [item for item in filtered_data 
                           if item['validation_score'] >= min_confidence]
            
            if sort_by == "Confiance":
                filtered_data.sort(key=lambda x: x['validation_score'], reverse=True)
            elif sort_by == "Catégorie":
                filtered_data.sort(key=lambda x: x['classification']['main_category'])
            else:
                filtered_data.sort(key=lambda x: x['original'])
            
            # Affichage des résultats
            for item in filtered_data:
                classification = item['classification']
                
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.write(f"**{item['processed']}**")
                        if item['original'] != item['processed']:
                            st.caption(f"Original: {item['original']}")
                    
                    with col2:
                        st.markdown(
                            f"<div class='classification-badge' style='background:{classification['main_color']}20; border-color:{classification['main_color']}'>"
                            f"{classification['main_category']}</div>",
                            unsafe_allow_html=True
                        )
                    
                    with col3:
                        confidence_color = ACCENT_GREEN if item['validation_score'] > 0.8 else ACCENT_ORANGE
                        st.markdown(
                            f"<div style='text-align: center; color: {confidence_color}; font-weight: bold;'>"
                            f"{item['validation_score']:.0%}</div>",
                            unsafe_allow_html=True
                        )
                    
                    st.markdown("---")
        
        else:
            st.info("🎯 Traitez d'abord vos données pour voir les résultats détaillés")
    
    # Onglet 4: Export Intelligent
    with tab4:
        if st.session_state.get('processed', False):
            st.markdown("### 💾 Export Intelligent")
            
            cleaned_data = st.session_state.cleaned_data
            
            # Options d'export avancées
            export_col1, export_col2 = st.columns(2)
            
            with export_col1:
                st.markdown("#### 📁 Structure d'Export")
                include_original = st.checkbox("Inclure données originales", True)
                include_classification = st.checkbox("Inclure classification", True)
                include_confidence = st.checkbox("Inclure score de confiance", True)
                
                grouping_option = st.radio(
                    "Regroupement",
                    ["Aucun", "Par catégorie principale", "Par sous-catégorie"],
                    horizontal=True
                )
            
            with export_col2:
                st.markdown("#### 🎯 Filtres d'Export")
                min_confidence_export = st.slider("Confiance minimale d'export", 0.0, 1.0, 0.7, 0.1)
                
                selected_categories_export = st.multiselect(
                    "Catégories à inclure",
                    options=list(set([item['classification']['main_category'] for item in cleaned_data])),
                    default=list(set([item['classification']['main_category'] for item in cleaned_data]))
                )
            
            # Préparation des données d'export
            export_data = []
            for item in cleaned_data:
                if (item['validation_score'] >= min_confidence_export and 
                    item['classification']['main_category'] in selected_categories_export):
                    
                    export_item = {"Donnée traitée": item['processed']}
                    
                    if include_original:
                        export_item["Donnée originale"] = item['original']
                    
                    if include_classification:
                        export_item["Catégorie principale"] = item['classification']['main_category']
                        export_item["Sous-catégorie"] = item['classification']['subcategory']
                    
                    if include_confidence:
                        export_item["Score de confiance"] = f"{item['validation_score']:.1%}"
                    
                    if item['correction_note']:
                        export_item["Note de correction"] = item['correction_note']
                    
                    export_data.append(export_item)
            
            # Génération du fichier d'export
            if export_data:
                df_export = pd.DataFrame(export_data)
                
                if export_format == "CSV":
                    csv = df_export.to_csv(index=False)
                    b64 = base64.b64encode(csv.encode()).decode()
                    href = f'<a href="data:file/csv;base64,{b64}" download="loopy_diod_export.csv">📥 Télécharger CSV</a>'
                
                elif export_format == "Excel":
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                        df_export.to_excel(writer, index=False, sheet_name='Données_Purifiées')
                    excel_data = output.getvalue()
                    b64 = base64.b64encode(excel_data).decode()
                    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="loopy_diod_export.xlsx">📥 Télécharger Excel</a>'
                
                elif export_format == "JSON":
                    json_str = df_export.to_json(orient='records', indent=2)
                    b64 = base64.b64encode(json_str.encode()).decode()
                    href = f'<a href="data:application/json;base64,{b64}" download="loopy_diod_export.json">📥 Télécharger JSON</a>'
                
                else:  # TXT
                    txt_content = "\n".join([item['Donnée traitée'] for item in export_data])
                    b64 = base64.b64encode(txt_content.encode()).decode()
                    href = f'<a href="data:file/txt;base64,{b64}" download="loopy_diod_export.txt">📥 Télécharger TXT</a>'
                
                st.markdown(href, unsafe_allow_html=True)
                
                # Aperçu des données exportées
                st.markdown("#### 👁️ Aperçu des données exportées")
                st.dataframe(df_export.head(10), use_container_width=True)
                
                st.success(f"✅ {len(export_data)} éléments prêts pour l'export")
            else:
                st.warning("⚠️ Aucune donnée ne correspond aux critères d'export")
        
        else:
            st.info("🎯 Traitez d'abord vos données pour pouvoir les exporter")

# =============================================================================
# LANCEMENT DE L'APPLICATION
# =============================================================================

if __name__ == "__main__":
    # Initialisation de la session
    if 'processed' not in st.session_state:
        st.session_state.processed = False
    if 'cleaned_data' not in st.session_state:
        st.session_state.cleaned_data = []
    if 'stats' not in st.session_state:
        st.session_state.stats = {}
    
    main()
