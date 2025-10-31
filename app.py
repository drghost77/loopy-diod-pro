import streamlit as st
import pandas as pd
import re
import base64
from datetime import datetime
import io
from io import StringIO
import matplotlib.pyplot as plt  # Nouveau : pour les graphiques

# Liste de domaines email courants pour correction
COMMON_EMAIL_DOMAINS = [
    "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "orange.fr", "wanadoo.fr", "icloud.com", "live.com"
]

# Configuration
st.set_page_config(page_title="🔮 LOOPY DIOD Pro", layout="wide")

# CSS optimisé
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
    }
    .classification-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 15px;
        font-size: 12px;
        font-weight: bold;
        margin: 2px;
    }
</style>
""", unsafe_allow_html=True)

# SYSTÈME DE CLASSIFICATION INTELLIGENT
CLASSIFICATION_RULES = {
    "📞 Téléphones Haïti": {
        "patterns": [r'^509', r'^\+509'],
        "color": "#FF6B6B"
    },
    "📞 Téléphones France": {
        "patterns": [r'^33', r'^\+33', r'^0033'],
        "color": "#4ECDC4"
    },
    "📞 Téléphones USA/Canada": {
        "patterns": [r'^1', r'^\+1', r'^001'],
        "color": "#45B7D1"
    },
    "📧 Emails Professionnels": {
        "patterns": [r'@gmail\.com$', r'@yahoo\.com$', r'@hotmail\.com$'],
        "color": "#96CEB4"
    },
    "📧 Emails Entreprise": {
        "patterns": [r'@entreprise\.', r'@société\.', r'@company\.'],
        "color": "#FFEAA7"
    },
    "🌐 URLs Sites Web": {
        "patterns": [r'^https?://', r'^www\.'],
        "color": "#DDA0DD"
    },
    "🔢 Codes Produits": {
        "patterns": [r'^[A-Z]{2,3}\d{3,5}$', r'^PROD\_'],
        "color": "#98D8C8"
    },
    "👤 Noms Utilisateurs": {
        "patterns": [r'^@[\w\.]+$', r'^user_'],
        "color": "#F7DC6F"
    },
    "📝 Texte Générique": {
        "patterns": [r'^[A-Za-z\s]{5,50}$'],
        "color": "#BB8FCE"
    }
}

def suggest_email_domain(email):
    """Propose une correction de domaine si besoin"""
    if '@' not in email:
        return None
    user, domain = email.split('@', 1)
    domain = domain.lower()
    if domain in COMMON_EMAIL_DOMAINS:
        return None
    # Correction simple : distance de Levenshtein sur chaque domaine connu
    for common in COMMON_EMAIL_DOMAINS:
        # Distance naïve : nombre de caractères différents
        diff = sum(a != b for a, b in zip(domain, common)) + abs(len(domain) - len(common))
        if diff <= 2:
            return f"{user}@{common}"
    return None

def validate_email(email):
    """Validation syntaxique et suggestion de correction email"""
    pattern = r'\b[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Z|a-z]{2,})\b'
    if not re.fullmatch(pattern, email):
        return False, None  # Syntaxe invalide
    suggestion = suggest_email_domain(email)
    return True, suggestion

def classify_item(item, custom_rules=None):
    """Système de classification intelligent avec support custom"""
    item_str = str(item).strip()
    # Règles personnalisées
    if custom_rules:
        for regex, category, color in custom_rules:
            if re.search(regex, item_str, re.IGNORECASE):
                return category, color
    # Règles classiques
    for category, rules in CLASSIFICATION_RULES.items():
        for pattern in rules['patterns']:
            if re.search(pattern, item_str, re.IGNORECASE):
                return category, rules['color']
    # Classification par défaut basée sur le contenu
    if re.match(r'^[\d\+\(\)\s\-]{8,20}$', item_str):
        return "📞 Téléphone Générique", "#AAB7B8"
    elif '@' in item_str and '.' in item_str.split('@')[-1]:
        return "📧 Email Générique", "#85C1E9"
    elif re.match(r'^https?://', item_str) or re.match(r'^www\.', item_str):
        return "🌐 Lien Web", "#F8C471"
    elif len(item_str) <= 10 and item_str.isalnum():
        return "🔤 Code Court", "#D7BDE2"
    else:
        return "📝 Texte Divers", "#F9E79F"

def normalize_phone(phone):
    """Normalisation des numéros de téléphone"""
    if not phone or pd.isna(phone):
        return None
    cleaned = re.sub(r'[^\d+]', '', str(phone))
    if cleaned.startswith('00'):
        cleaned = '+' + cleaned[2:]
    elif cleaned.startswith('0') and len(cleaned) > 6:
        cleaned = '+33' + cleaned[1:]
    if re.match(r'^\+?[\d\s\-\(\)]{8,20}$', cleaned):
        return cleaned
    return None

def extract_emails(text):
    """Extraction d'emails"""
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(pattern, str(text))

def analyze_data_quality(items):
    """Analyse de qualité des données"""
    total = len(items)
    if total == 0:
        return {}
    stats = {
        'total': total,
        'emails': 0,
        'phones': 0,
        'urls': 0,
        'valid_format': 0,
        'classified': 0
    }
    for item in items:
        item_str = str(item).strip()
        if '@' in item_str and '.' in item_str.split('@')[-1]:
            stats['emails'] += 1
        if re.match(r'^[\d\+\(\)\s\-]{8,20}$', item_str):
            stats['phones'] += 1
        if re.match(r'^(https?://|www\.)', item_str.lower()):
            stats['urls'] += 1
        if len(item_str) >= 3 and len(item_str) <= 100:
            stats['valid_format'] += 1
        category, _ = classify_item(item_str)
        if category != "📝 Texte Divers":
            stats['classified'] += 1
    for key in ['emails', 'phones', 'urls', 'valid_format', 'classified']:
        stats[f'{key}_pct'] = (stats[key] / total) * 100
    return stats

def get_download_link(data, filename):
    """Générer lien de téléchargement"""
    b64 = base64.b64encode(data.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{filename}">📥 {filename}</a>'

def show_stats_pie(stats):
    """Affiche un camembert des stats principales"""
    labels = []
    sizes = []
    colors = ['#96CEB4', '#FF6B6B', '#DDA0DD', '#F7DC6F']
    if stats['emails']: labels.append('Emails'); sizes.append(stats['emails'])
    if stats['phones']: labels.append('Téléphones'); sizes.append(stats['phones'])
    if stats['urls']: labels.append('URLs'); sizes.append(stats['urls'])
    if stats['classified']: labels.append('Classifiés'); sizes.append(stats['classified'])
    if not sizes: return
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors[:len(sizes)])
    st.pyplot(fig)

# INTERFACE PRINCIPALE
def main():
    st.markdown("""
    <div class="main-header">
        <h1 style="margin:0; color:white;">🔮 LOOPY DIOD PRO</h1>
        <p style="margin:0; opacity:0.9;">Nettoyage & Classification Intelligente</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Paramètres")
        remove_duplicates = st.checkbox("Supprimer doublons", True)
        auto_classify = st.checkbox("Classification auto", True)
        export_by_category = st.checkbox("Exporter par catégorie", True)

        st.markdown("---")
        st.header("📊 Classification")
        for category, rules in CLASSIFICATION_RULES.items():
            st.markdown(
                f"<span style='background:{rules['color']}; padding:2px 8px; border-radius:10px; font-size:10px;'>●</span> {category}",
                unsafe_allow_html=True
            )
        # Amélioration : Ajout règle personnalisée
        st.markdown("---")
        st.header("✨ Règle personnalisée")
        custom_regex = st.text_input("Regex personnalisée")
        custom_label = st.text_input("Nom de la catégorie")
        custom_color = st.color_picker("Couleur", "#FFD700") if custom_label else "#FFD700"
        custom_rules = []
        if custom_regex and custom_label:
            custom_rules.append((custom_regex, custom_label, custom_color))
            st.markdown(f"<span style='background:{custom_color}; padding:2px 8px; border-radius:10px; font-size:10px;'>●</span> {custom_label}", unsafe_allow_html=True)

    # Zone de saisie principale
    col1, col2 = st.columns([2, 1])

    with col1:
        input_data = st.text_area(
            "📥 Collez vos données (1 par ligne):",
            height=300,
            placeholder="Exemple:\n+509 31 45 6642\ncontact@example.com\nhttps://site.com\njohn.doe@entreprise.com\n+33 1 23 45 67 89\nPROD_001\n@username\n001 555 123 4567"
        )

    with col2:
        st.subheader("🎯 Options")
        clean_phones = st.checkbox("Nettoyer téléphones", True)
        extract_emails_option = st.checkbox("Extraire emails", True)
        remove_empty = st.checkbox("Supprimer vide", True)

        st.subheader("📁 Import")
        uploaded_file = st.file_uploader("Fichier TXT/CSV", type=['txt', 'csv'])

    # Traitement du fichier uploadé
    if uploaded_file:
        if uploaded_file.type == "text/csv":
            df = pd.read_csv(uploaded_file)
            input_data = '\n'.join(df.iloc[:, 0].astype(str).tolist())
        else:
            input_data = uploaded_file.getvalue().decode()

    # Bouton de traitement
    if st.button("🔮 MAGIC CLEAN & CLASSIFY", use_container_width=True):
        if input_data:
            with st.spinner("Traitement en cours..."):
                lines = [line.strip() for line in input_data.split('\n')]
                if remove_empty:
                    lines = [line for line in lines if line.strip()]
                processed_data = []
                classification_results = {}

                for line in lines:
                    original = line
                    processed = line
                    # Nettoyage téléphones
                    if clean_phones:
                        phone_cleaned = normalize_phone(line)
                        if phone_cleaned:
                            processed = phone_cleaned

                    # Classification (avec custom)
                    category, color = classify_item(processed, custom_rules=custom_rules if auto_classify else None)

                    # Validation d'email avancée
                    email_valid = None
                    email_suggestion = None
                    if '@' in processed and '.' in processed.split('@')[-1]:
                        email_valid, email_suggestion = validate_email(processed)

                    processed_data.append({
                        'original': original,
                        'processed': processed,
                        'category': category,
                        'color': color,
                        'email_valid': email_valid,
                        'email_suggestion': email_suggestion
                    })

                    # Regroupement par catégorie
                    if category not in classification_results:
                        classification_results[category] = []
                    classification_results[category].append(processed)

                # Suppression doublons
                if remove_duplicates:
                    seen = set()
                    unique_data = []
                    for item in processed_data:
                        if item['processed'] not in seen:
                            seen.add(item['processed'])
                            unique_data.append(item)
                    processed_data = unique_data

                # AFFICHAGE DES RÉSULTATS
                st.success(f"✅ {len(processed_data)} éléments traités")

                stats = analyze_data_quality([item['processed'] for item in processed_data])

                # Métriques + graphique camembert
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total", len(processed_data))
                with col2:
                    st.metric("Emails", f"{stats.get('emails', 0)}")
                with col3:
                    st.metric("Téléphones", f"{stats.get('phones', 0)}")
                with col4:
                    st.metric("Classifiés", f"{stats.get('classified', 0)}")
                show_stats_pie(stats)

                # Résultats par catégorie
                st.subheader("📊 Résultats par Catégorie")
                for category, items in classification_results.items():
                    category_color = next(
                        (rules['color'] for cat, rules in CLASSIFICATION_RULES.items() if cat == category),
                        "#CCCCCC"
                    )
                    # Prise en compte des règles personnalisées
                    if custom_rules and category == custom_label:
                        category_color = custom_color
                    with st.expander(f"🎯 {category} ({len(items)} éléments)"):
                        for item in items:
                            st.markdown(
                                f"<div style='padding:5px; margin:2px; border-left:4px solid {category_color}'>{item}</div>",
                                unsafe_allow_html=True
                            )
                        if export_by_category:
                            category_filename = f"loopy_{category.replace(' ', '_').lower()}.txt"
                            category_data = '\n'.join(items)
                            st.markdown(
                                get_download_link(category_data, category_filename),
                                unsafe_allow_html=True
                            )

                # Export global
                st.subheader("💾 Export Global")
                all_processed = [item['processed'] for item in processed_data]
                global_data = '\n'.join(all_processed)

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(get_download_link(global_data, "loopy_tous_éléments.txt"), unsafe_allow_html=True)
                with col2:
                    classified_data = "\n".join([
                        f"{item['processed']} | {item['category']}"
                        for item in processed_data
                    ])
                    st.markdown(get_download_link(classified_data, "loopy_classifié.txt"), unsafe_allow_html=True)

                # Tableau détaillé
                st.subheader("📋 Vue Détaillée")
                df_results = pd.DataFrame(processed_data)
                # Ajout colonne validation et suggestion email
                if 'email_valid' in df_results.columns:
                    df_results['Email valide'] = df_results['email_valid'].apply(lambda v: "✅" if v is True else ("❌" if v is False else ""))
                    df_results['Correction email'] = df_results['email_suggestion'].fillna("")
                st.dataframe(df_results[['original', 'processed', 'category', 'Email valide', 'Correction email']], use_container_width=True)

        else:
            st.warning("⚠️ Veuillez coller des données ou uploader un fichier")

    # Section d'exemples
    with st.expander("🎯 Exemples de Classification"):
        st.write("""
        **Le système classe automatiquement :**
        - `+509 31 45 6642` → 📞 Téléphones Haïti
        - `contact@example.com` → 📧 Emails Professionnels  
        - `https://site.com` → 🌐 URLs Sites Web
        - `PROD_001` → 🔢 Codes Produits
        - `@username` → 👤 Noms Utilisateurs
        - `+33 1 23 45 67 89` → 📞 Téléphones France
        """)

if __name__ == "__main__":
    main()
