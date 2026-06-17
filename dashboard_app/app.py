import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import altair as alt

st.set_page_config(
    page_title="Détection d'Anomalies — IEEE-CIS",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Styles CSS (Thème Clair Premium avec Cartes Colorées) ─
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Force light theme background on the entire app */
[data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background-color: #f8fafc !important;
    color: #1e293b !important;
}

[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #e2e8f0 !important;
}

/* Make sure all sidebar native text is readable */
[data-testid="stSidebar"] p, 
[data-testid="stSidebar"] label, 
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div {
    color: #334155;
}

[data-testid="stSidebar"] .sidebar-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 6px 0 20px 0;
    border-bottom: 1px solid #e2e8f0;
    margin-bottom: 20px;
}
[data-testid="stSidebar"] .sidebar-logo-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    background: #2563eb;
    box-shadow: 0 0 6px rgba(37, 99, 235, 0.4);
    flex-shrink: 0;
}
[data-testid="stSidebar"] .sidebar-logo-text { 
    font-size: 0.82rem; 
    font-weight: 600; 
    color: #0f172a !important; 
    letter-spacing: 0.4px; 
}

/* Sidebar sections styled as neat cards */
[data-testid="stSidebar"] .sidebar-section { 
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 14px 16px;
    margin-bottom: 20px; 
}
[data-testid="stSidebar"] .sidebar-label {
    font-size: 0.68rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    color: #64748b !important;
    margin-bottom: 12px;
}
[data-testid="stSidebar"] .sidebar-stat {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px solid #e2e8f0;
    font-size: 0.82rem;
}
[data-testid="stSidebar"] .sidebar-stat:last-child {
    border-bottom: none;
}
[data-testid="stSidebar"] .sidebar-stat-label { 
    color: #475569 !important; 
}
[data-testid="stSidebar"] .sidebar-stat-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #0f172a !important;
    font-weight: 600;
}
[data-testid="stSidebar"] .sidebar-stat-value.alerte { color: #dc2626 !important; }
[data-testid="stSidebar"] .sidebar-stat-value.ok     { color: #16a34a !important; }
[data-testid="stSidebar"] .sidebar-stat-value.neutre { color: #2563eb !important; }
[data-testid="stSidebar"] .sidebar-stat-value.orange { color: #ea580c !important; }

/* Sidebar footer is standard-flowing, not fixed (avoids overlaps) */
[data-testid="stSidebar"] .sidebar-footer {
    margin-top: 30px;
    padding: 16px 0;
    border-top: 1px solid #e2e8f0;
    font-size: 0.73rem;
    color: #64748b !important;
    line-height: 1.7;
}

/* Radio options styling in the sidebar */
[data-testid="stSidebar"] div[role="radiogroup"] label p {
    color: #334155 !important;
}

/* ── En-tête ── */
.entete {
    background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 60%, #eff6ff 100%);
    border: 1px solid #bfdbfe;
    border-radius: 10px;
    padding: 28px 32px;
    margin-bottom: 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.entete-titre h1 {
    margin: 0 0 6px 0;
    font-size: 1.45rem;
    font-weight: 700;
    color: #1e3a8a;
    letter-spacing: -0.3px;
}
.entete-titre p {
    margin: 0;
    font-size: 0.83rem;
    color: #1e40af;
    letter-spacing: 0.2px;
}
.entete-badge {
    background: rgba(37, 99, 235, 0.08);
    border: 1px solid rgba(37, 99, 235, 0.2);
    border-radius: 6px;
    padding: 10px 18px;
    text-align: center;
    flex-shrink: 0;
}
.entete-badge .badge-val  { font-family: 'JetBrains Mono', monospace; font-size: 1.1rem; font-weight: 600; color: #2563eb; }
.entete-badge .badge-lab  { font-size: 0.7rem; color: #1e40af; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 2px; }

/* ── KPI Cards (Vibrant Pastel Palette) ── */
.kpi-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; margin-bottom: 20px; }
.kpi-card {
    border-radius: 8px;
    padding: 16px 18px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
}
.kpi-label { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 8px; font-weight: 600; }
.kpi-value { font-family: 'JetBrains Mono', monospace; font-size: 1.5rem; font-weight: 750; line-height: 1; }
.kpi-sub   { font-size: 0.72rem; margin-top: 6px; }

/* Bleu Card */
.kpi-card.bleu { background: #f0f9ff; border: 1px solid #bae6fd; }
.kpi-card.bleu::before { background: #0284c7; }
.kpi-card.bleu .kpi-label { color: #0369a1 !important; }
.kpi-card.bleu .kpi-value { color: #0369a1 !important; }
.kpi-card.bleu .kpi-sub { color: #0284c7 !important; }

/* Rouge Card */
.kpi-card.rouge { background: #fef2f2; border: 1px solid #fecaca; }
.kpi-card.rouge::before { background: #dc2626; }
.kpi-card.rouge .kpi-label { color: #991b1b !important; }
.kpi-card.rouge .kpi-value { color: #991b1b !important; }
.kpi-card.rouge .kpi-sub { color: #dc2626 !important; }

/* Orange Card */
.kpi-card.orange { background: #fff7ed; border: 1px solid #ffedd5; }
.kpi-card.orange::before { background: #ea580c; }
.kpi-card.orange .kpi-label { color: #9a3412 !important; }
.kpi-card.orange .kpi-value { color: #9a3412 !important; }
.kpi-card.orange .kpi-sub { color: #ea580c !important; }

/* Vert Card */
.kpi-card.vert { background: #f0fdf4; border: 1px solid #bbf7d0; }
.kpi-card.vert::before { background: #16a34a; }
.kpi-card.vert .kpi-label { color: #065f46 !important; }
.kpi-card.vert .kpi-value { color: #065f46 !important; }
.kpi-card.vert .kpi-sub { color: #16a34a !important; }

/* Violet Card */
.kpi-card.violet { background: #f5f3ff; border: 1px solid #ddd6fe; }
.kpi-card.violet::before { background: #7c3aed; }
.kpi-card.violet .kpi-label { color: #5b21b6 !important; }
.kpi-card.violet .kpi-value { color: #5b21b6 !important; }
.kpi-card.violet .kpi-sub { color: #7c3aed !important; }

/* ── Section titre ── */
.section-titre {
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    color: #475569;
    margin: 24px 0 12px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid #e2e8f0;
}

/* ── Custom containers style ── */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 8px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
}

.carte-titre { 
    font-size: 0.8rem; 
    font-weight: 600; 
    color: #475569; 
    text-transform: uppercase; 
    letter-spacing: 0.6px; 
    margin-bottom: 14px; 
}

/* ── Note ── */
.note {
    background: #f8fafc;
    border-left: 3px solid #2563eb;
    padding: 10px 14px;
    border-radius: 0 4px 4px 0;
    font-size: 0.8rem;
    color: #334155;
    margin-top: 12px;
    line-height: 1.65;
}

/* ── Statuts ── */
.statut-alerte {
    background: #fee2e2;
    border: 1px solid #fca5a5;
    color: #b91c1c;
    font-weight: 600;
    padding: 14px 18px;
    border-radius: 6px;
    text-align: center;
    font-size: 0.92rem;
    letter-spacing: 0.3px;
}
.statut-valide {
    background: #dcfce7;
    border: 1px solid #86efac;
    color: #15803d;
    font-weight: 600;
    padding: 14px 18px;
    border-radius: 6px;
    text-align: center;
    font-size: 0.92rem;
    letter-spacing: 0.3px;
}
.score-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 14px 16px;
    margin-top: 12px;
    font-size: 0.82rem;
    color: #334155;
    line-height: 1.75;
}
.score-box code {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    background: #f1f5f9;
    padding: 1px 6px;
    border-radius: 3px;
    color: #2563eb !important;
}

/* ── Tableau de transaction ── */
.tx-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px solid #f1f5f9;
    font-size: 0.82rem;
}
.tx-key { color: #475569 !important; }
.tx-val { font-family: 'JetBrains Mono', monospace; color: #0f172a !important; font-size: 0.78rem; font-weight: 600; }

/* Streamlit overrides */
[data-testid="stMetric"] { display: none; }

div[data-testid="stSelectbox"] label {
    color: #475569 !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}
div[data-testid="stSelectbox"] div[data-baseweb="select"] {
    background-color: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
}
div[data-testid="stSelectbox"] div[data-baseweb="select"] * {
    color: #0f172a !important;
}

.stButton > button {
    background: #2563eb !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 10px 22px !important;
    letter-spacing: 0.3px !important;
}
.stButton > button:hover { 
    background: #1d4ed8 !important; 
}
.stButton > button:active, .stButton > button:focus {
    color: #ffffff !important;
    background: #1d4ed8 !important;
}
</style>
""", unsafe_allow_html=True)


# ── Helper HTML rendering ────────────────────────────────
def render_html(html_code: str):
    # Enlève l'indentation de chaque ligne pour éviter le mode code block de Markdown
    clean_lines = [line.strip() for line in html_code.splitlines()]
    st.markdown("\n".join(clean_lines), unsafe_allow_html=True)


# Chemins absolus des fichiers requis
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATH_MODEL = os.path.join(BASE_DIR, "iforest_model.pkl")
PATH_SCALER = os.path.join(BASE_DIR, "scaler.pkl")
PATH_DATA = os.path.join(BASE_DIR, "test_sample.csv")

# Initialisation par défaut pour éviter NameError
modele, scaler, df, ok = None, None, None, False

def encoder_categories(X):
    # On fait une copie locale pour ne pas modifier l'original
    X_encoded = X.copy()
    
    CATEGORICAL_MAPPINGS = {
        'ProductCD': ['C', 'H', 'R', 'S', 'W'],
        'card4': ['Unknown', 'american express', 'discover', 'mastercard', 'visa'],
        'card6': ['Unknown', 'charge card', 'credit', 'debit', 'debit or credit'],
        'P_emaildomain': [
            'Unknown', 'aim.com', 'anonymous.com', 'aol.com', 'att.net', 'bellsouth.net',
            'cableone.net', 'centurylink.net', 'cfl.rr.com', 'charter.net', 'comcast.net',
            'cox.net', 'earthlink.net', 'embarqmail.com', 'frontier.com', 'frontiernet.net',
            'gmail', 'gmail.com', 'gmx.de', 'hotmail.co.uk', 'hotmail.com',
            'hotmail.de', 'hotmail.es', 'hotmail.fr', 'icloud.com', 'juno.com',
            'live.com', 'live.com.mx', 'live.fr', 'mac.com', 'mail.com', 'me.com',
            'msn.com', 'netzero.com', 'netzero.net', 'optonline.net', 'outlook.com',
            'outlook.es', 'prodigy.net.mx', 'protonmail.com', 'ptd.net', 'q.com',
            'roadrunner.com', 'rocketmail.com', 'sbcglobal.net', 'sc.rr.com',
            'servicios-ta.com', 'suddenlink.net', 'twc.com', 'verizon.net', 'web.de',
            'windstream.net', 'yahoo.co.jp', 'yahoo.co.uk', 'yahoo.com', 'yahoo.com.mx',
            'yahoo.de', 'yahoo.es', 'yahoo.fr', 'ymail.com'
        ],
        'M4': ['M0', 'M1', 'M2', 'Unknown'],
        'M6': ['F', 'T', 'Unknown'],
        'M1': ['F', 'T', 'nan'],
        'M2': ['F', 'T', 'nan'],
        'M3': ['F', 'T', 'nan'],
        'M5': ['F', 'T', 'nan'],
        'M7': ['F', 'T', 'nan'],
        'M8': ['F', 'T', 'nan'],
        'M9': ['F', 'T', 'nan'],
    }
    
    for col, classes_list in CATEGORICAL_MAPPINGS.items():
        if col in X_encoded.columns:
            # 1. Remplissage des valeurs manquantes pour les colonnes spécifiques
            if col in ['card4', 'card6', 'P_emaildomain', 'M4', 'M6']:
                X_encoded[col] = X_encoded[col].fillna('Unknown')
            
            # 2. Conversion en chaînes de caractères et normalisation des nans
            s = X_encoded[col].astype(str).replace({'None': 'nan', '<NA>': 'nan', 'nan': 'nan', 'NaN': 'nan'})
            
            # 3. Correspondance vers les indices triés
            mapping = {val: idx for idx, val in enumerate(classes_list)}
            fallback_val = 'Unknown' if 'Unknown' in classes_list else ('nan' if 'nan' in classes_list else classes_list[0])
            fallback_idx = classes_list.index(fallback_val)
            
            X_encoded[col] = s.map(lambda val: mapping.get(val, fallback_idx))
            
    return X_encoded

@st.cache_resource
def charger():
    if os.path.exists(PATH_MODEL) and os.path.exists(PATH_SCALER) and os.path.exists(PATH_DATA):
        modele = joblib.load(PATH_MODEL)
        scaler = joblib.load(PATH_SCALER)
        df     = pd.read_csv(PATH_DATA)
        
        # 1. Sélectionner uniquement les features attendues par le modèle
        features_attendues = scaler.feature_names_in_
        
        # 2. Préparation propre : on prend le df, on supprime les colonnes inutiles, 
        # on réindexe pour correspondre au modèle, et on remplit les vides avec 0
        cols_exclues = [c for c in ['isFraud','anomalie','score','heure'] if c in df.columns]
        X = df.drop(columns=cols_exclues)
        X = X.reindex(columns=features_attendues, fill_value=0)
        
        # Encodage des variables catégorielles avant la normalisation
        X_encoded = encoder_categories(X)
        
        # 3. Normalisation
        X_scaled = scaler.transform(X_encoded)
        
        seuil = -0.026048
        scores = modele.decision_function(X_scaled)
        df['anomalie'] = np.where(scores < seuil, 1, 0)
        df['score']    = scores
        
        return modele, scaler, df, True
    return None, None, pd.DataFrame(), False

# ── Appel de la fonction (ici c'est capital) ──
modele, scaler, df, ok = charger()

# ── Sidebar ──────────────────────────────────────────────
with st.sidebar:
    render_html("""
        <div class="sidebar-logo">
            <div class="sidebar-logo-dot"></div>
            <div class="sidebar-logo-text">AnomalyDetect</div>
        </div>
    """)

    page = st.radio("", ["Vue d'ensemble", "Simulateur de Risque"], label_visibility="collapsed")

    if ok:
        total         = len(df)
        n_fraudes     = int((df['isFraud']  == 1).sum())
        n_anomalies   = int((df['anomalie'] == 1).sum())
        taux_reel     = n_fraudes   / total * 100
        taux_ia       = n_anomalies / total * 100
        vp = int(((df['anomalie'] == 1) & (df['isFraud'] == 1)).sum())
        fp = int(((df['anomalie'] == 1) & (df['isFraud'] == 0)).sum())
        fn = int(((df['anomalie'] == 0) & (df['isFraud'] == 1)).sum())
        precision_val = vp / (vp + fp) * 100 if (vp + fp) > 0 else 0
        rappel_val    = vp / (vp + fn) * 100 if (vp + fn) > 0 else 0

        render_html(f"""
            <div class="sidebar-section">
                <div class="sidebar-label">Résumé du jeu de test</div>
                <div class="sidebar-stat">
                    <span class="sidebar-stat-label">Transactions</span>
                    <span class="sidebar-stat-value neutre">{total:,}</span>
                </div>
                <div class="sidebar-stat">
                    <span class="sidebar-stat-label">Fraudes réelles</span>
                    <span class="sidebar-stat-value alerte">{n_fraudes:,} ({taux_reel:.1f}%)</span>
                </div>
                <div class="sidebar-stat">
                    <span class="sidebar-stat-label">Alertes générées</span>
                    <span class="sidebar-stat-value orange">{n_anomalies:,} ({taux_ia:.1f}%)</span>
                </div>
            </div>
            <div class="sidebar-section">
                <div class="sidebar-label">Performance du modèle</div>
                <div class="sidebar-stat">
                    <span class="sidebar-stat-label">Vrais positifs</span>
                    <span class="sidebar-stat-value ok">{vp:,}</span>
                </div>
                <div class="sidebar-stat">
                    <span class="sidebar-stat-label">Faux positifs</span>
                    <span class="sidebar-stat-value alerte">{fp:,}</span>
                </div>
                <div class="sidebar-stat">
                    <span class="sidebar-stat-label">Faux négatifs</span>
                    <span class="sidebar-stat-value alerte">{fn:,}</span>
                </div>
                <div class="sidebar-stat">
                    <span class="sidebar-stat-label">Précision</span>
                    <span class="sidebar-stat-value neutre">{precision_val:.1f}%</span>
                </div>
                <div class="sidebar-stat">
                    <span class="sidebar-stat-label">Rappel</span>
                    <span class="sidebar-stat-value neutre">{rappel_val:.1f}%</span>
                </div>
            </div>
            <div class="sidebar-section">
                <div class="sidebar-label">Paramètres du modèle</div>
                <div class="sidebar-stat">
                    <span class="sidebar-stat-label">Algorithme</span>
                    <span class="sidebar-stat-value">Isolation Forest</span>
                </div>
                <div class="sidebar-stat">
                    <span class="sidebar-stat-label">Seuil de décision</span>
                    <span class="sidebar-stat-value neutre">-0.026048</span>
                </div>
                <div class="sidebar-stat">
                    <span class="sidebar-stat-label">Contamination</span>
                    <span class="sidebar-stat-value">3.5 %</span>
                </div>
                <div class="sidebar-stat">
                    <span class="sidebar-stat-label">Estimateurs</span>
                    <span class="sidebar-stat-value">100</span>
                </div>
            </div>
        """)

    render_html("""
        <div class="sidebar-footer">
            Abdrafith Zongo<br>
            Master 1 Data Science — IFOAD<br>
            Université Joseph Ki-Zerbo · Juin 2026
        </div>
    """)

# ── Garde-fou ────────────────────────────────────────────
if not ok:
    st.error("Fichiers introuvables : `iforest_model.pkl` et `test_sample.csv` attendus dans le répertoire de l'application.")
    st.stop()

# ── En-tête principal ────────────────────────────────────
render_html(f"""
<div class="entete">
    <div class="entete-titre">
        <h1>Détection d'Anomalies dans les Transactions Numériques</h1>
        <p>Apprentissage non supervisé &nbsp;·&nbsp; Isolation Forest &nbsp;·&nbsp; IEEE-CIS Fraud Detection (Kaggle, 2019)</p>
    </div>
    <div class="entete-badge">
        <div class="badge-val">{len(df):,}</div>
        <div class="badge-lab">transactions</div>
    </div>
</div>
""")


# ════════════════════════════════════════════════
# PAGE 1 — VUE D'ENSEMBLE
# ════════════════════════════════════════════════
if page == "Vue d'ensemble":

    total       = len(df)
    n_fraudes   = int((df['isFraud']  == 1).sum())
    n_anomalies = int((df['anomalie'] == 1).sum())
    taux_reel   = n_fraudes   / total * 100
    taux_ia     = n_anomalies / total * 100
    ecart       = n_anomalies - n_fraudes
    moy         = df['TransactionAmt'].mean()
    med         = df['TransactionAmt'].median()

    # ── KPI Grid ──
    render_html(f"""
    <div class="kpi-grid">
        <div class="kpi-card bleu">
            <div class="kpi-label">Transactions</div>
            <div class="kpi-value">{total:,}</div>
            <div class="kpi-sub">Jeu de test IEEE-CIS</div>
        </div>
        <div class="kpi-card rouge">
            <div class="kpi-label">Fraudes réelles</div>
            <div class="kpi-value">{n_fraudes:,}</div>
            <div class="kpi-sub">{taux_reel:.2f} % du total</div>
        </div>
        <div class="kpi-card orange">
            <div class="kpi-label">Alertes générées</div>
            <div class="kpi-value">{n_anomalies:,}</div>
            <div class="kpi-sub">{ecart:+d} vs fraudes réelles</div>
        </div>
        <div class="kpi-card vert">
            <div class="kpi-label">Montant moyen</div>
            <div class="kpi-value">{moy:.0f}<span style="font-size:0.9rem"> $</span></div>
            <div class="kpi-sub">Médiane : {med:.0f} $</div>
        </div>
        <div class="kpi-card violet">
            <div class="kpi-label">Taux de détection</div>
            <div class="kpi-value">{taux_ia:.1f}<span style="font-size:0.9rem"> %</span></div>
            <div class="kpi-sub">Contamination modèle</div>
        </div>
    </div>
    """)

    # ── Graphiques ──
    st.markdown('<div class="section-titre">Analyse graphique</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            render_html("<div class='carte-titre'>Taux de fraude et de détection par heure (%)</div>")
            if 'heure' in df.columns:
                df_t = pd.DataFrame({
                    'Fraude réelle (%)' : df.groupby('heure')['isFraud'].mean()  * 100,
                    'Détection IA (%)'  : df.groupby('heure')['anomalie'].mean() * 100
                })
                st.line_chart(df_t, color=["#f87171", "#2563eb"])
            render_html("""
                <div class="note">
                    Les deux courbes suivent une tendance similaire. Les pics nocturnes (0h–5h)
                    confirment que les fraudes surviennent principalement durant les heures creuses,
                    période où la surveillance humaine est réduite. Le modèle capte correctement
                    cette saisonnalité temporelle.
                </div>
            """)

    with col2:
        with st.container(border=True):
            render_html("<div class='carte-titre'>Distribution des montants par tranche (USD)</div>")
            tranches = pd.cut(df['TransactionAmt'],
                              bins=[0,20,50,100,250,500,1000,10000],
                              labels=['0–20','20–50','50–100','100–250','250–500','500–1k','1k+'])
            st.bar_chart(tranches.value_counts().sort_index())
            render_html("""
                <div class="note">
                    La grande majorité des transactions est inférieure à 100 dollars,
                    ce qui correspond au profil standard des achats en ligne.
                    Les transactions supérieures à 500 dollars sont rares mais présentent
                    un ratio de fraude statistiquement plus élevé.
                </div>
            """)

    col3, col4 = st.columns(2)

    with col3:
        with st.container(border=True):
            render_html("<div class='carte-titre'>Taux de fraude par type de carte (card6)</div>")
            if 'card6' in df.columns:
                corresp = {0:'Débit', 1:'Crédit', 2:'Inconnu'}
                df_c6   = df.copy()
                df_c6['type_carte'] = df_c6['card6'].map(corresp).fillna('Autre')
                taux_c6 = df_c6.groupby('type_carte')['isFraud'].mean() * 100
                st.bar_chart(taux_c6)
            render_html("""
                <div class="note">
                    Les cartes de crédit affichent un taux de fraude supérieur aux cartes
                    de débit, en raison de leurs plafonds plus élevés qui maximisent
                    le gain potentiel pour le fraudeur.
                </div>
            """)

    with col4:
        with st.container(border=True):
            render_html("<div class='carte-titre'>Score d'anomalie — distribution par classe</div>")
            if 'score' in df.columns:
                df_scores_melted = pd.DataFrame({
                    'Score': pd.concat([
                        df[df['isFraud']==1]['score'],
                        df[df['isFraud']==0]['score']
                    ]),
                    'Classe': ['Fraude (Réelle)'] * (df['isFraud']==1).sum() + ['Légitime'] * (df['isFraud']==0).sum()
                }).dropna()

                chart = alt.Chart(df_scores_melted).mark_area(
                    opacity=0.6,
                    interpolate='monotone'
                ).encode(
                    alt.X('Score:Q', bin=alt.Bin(maxbins=30), title="Score d'anomalie (plus bas = plus suspect)"),
                    alt.Y('count():Q', stack=None, title="Nombre de transactions"),
                    alt.Color('Classe:N', scale=alt.Scale(domain=['Fraude (Réelle)', 'Légitime'], range=['#dc2626', '#2563eb']), title="Classe")
                ).properties(
                    height=200
                )
                st.altair_chart(chart, use_container_width=True)

            render_html("""
                <div class="note">
                    <strong>Comment interpréter ?</strong><br>
                    Plus le score est bas (vers la gauche), plus la transaction est jugée suspecte par le modèle. 
                    La zone rouge (fraudes réelles) se concentre nettement plus à gauche que la zone bleue (transactions légitimes), validant la pertinence du modèle.
                </div>
            """)


# ════════════════════════════════════════════════
# PAGE 2 — SIMULATEUR DE RISQUE
# ════════════════════════════════════════════════
elif page == "Simulateur de Risque":

    st.markdown('<div class="section-titre">Fonctionnement du modèle</div>', unsafe_allow_html=True)
    with st.container(border=True):
        render_html("""
            <p style="font-size:0.88rem; line-height:1.8; color:#334155; margin:0;">
                L'algorithme <strong style="color:#0f172a;">Isolation Forest</strong> analyse chaque transaction
                en la comparant au comportement statistique de l'ensemble du jeu de données.
                Il procède par découpages aléatoires successifs : une transaction normale nécessite
                de nombreuses étapes pour être isolée (comportement fréquent), tandis qu'une transaction
                anormale est isolée en très peu d'étapes (comportement rare et atypique).
                Ce mécanisme produit un <strong style="color:#0f172a;">score d'anomalie</strong> :
                plus ce score est bas, plus la transaction s'écarte du comportement habituel
                et mérite une vérification manuelle.
                Le seuil de décision a été calibré à <strong style="color:#2563eb;">-0.026048</strong>
                pour maximiser le rappel sur le jeu de validation.
            </p>
        """)

    st.markdown('<div class="section-titre">Sélection de la transaction</div>', unsafe_allow_html=True)
    with st.container(border=True):
        indice      = st.selectbox("Index de transaction :", df.index.tolist())
        transaction = df.iloc[indice]
        label_reel  = int(transaction['isFraud'])

        # Affichage des caractéristiques
        cols_tx = [c for c in ['TransactionAmt','ProductCD','card1','card4','card6','P_emaildomain','TransactionDT'] if c in df.columns]
        
        rows_html = []
        for col in cols_tx:
            val = transaction[col]
            rows_html.append(f"""
                <div class="tx-row">
                    <span class="tx-key">{col}</span>
                    <span class="tx-val">{val}</span>
                </div>
            """)
        render_html("\n".join(rows_html))

    if st.button("Analyser cette transaction", type="primary"):

        features_attendues = scaler.feature_names_in_
        cols_exclues = [c for c in ['isFraud','anomalie','score','heure'] if c in df.columns]
        X_tx         = df.drop(columns=cols_exclues).iloc[[indice]]
        X_tx         = X_tx.reindex(columns=features_attendues, fill_value=0)
        
        # Encodage des variables catégorielles de la transaction sélectionnée
        X_tx_encoded = encoder_categories(X_tx)
        
        # Normalisation indispensable car le modèle a été entraîné sur données centrées/réduites
        X_tx_scaled  = scaler.transform(X_tx_encoded)
        
        seuil        = -0.026048
        score        = modele.decision_function(X_tx_scaled)[0]
        est_anomalie = int(score < seuil)

        st.markdown('<div class="section-titre">Résultat de l\'analyse</div>', unsafe_allow_html=True)

        rcol1, rcol2 = st.columns(2)

        with rcol1:
            with st.container(border=True):
                render_html("<div class='carte-titre'>Diagnostic du modèle</div>")

                if est_anomalie:
                    render_html('<div class="statut-alerte">ALERTE — Anomalie détectée &nbsp;·&nbsp; Risque élevé</div>')
                else:
                    render_html('<div class="statut-valide">VALIDATION — Transaction conforme &nbsp;·&nbsp; Risque faible</div>')

                render_html(f"""
                    <div class="score-box">
                        Score d'anomalie &nbsp;·&nbsp; <code>{score:.6f}</code><br>
                        Seuil de décision &nbsp;·&nbsp; <code>{seuil}</code><br>
                        Décision &nbsp;·&nbsp; <code>{'score < seuil → ALERTE' if est_anomalie else 'score ≥ seuil → VALIDATION'}</code><br><br>
                        {'Le score est inférieur au seuil critique. Cette transaction présente des écarts statistiques significatifs par rapport au comportement moyen du dataset. Une inspection manuelle est recommandée avant tout traitement.' if est_anomalie else 'Le score est supérieur au seuil critique. Le comportement de cette transaction est cohérent avec les habitudes transactionnelles observées dans le dataset.'}
                    </div>
                """)

        with rcol2:
            with st.container(border=True):
                render_html("<div class='carte-titre'>Vérification terrain</div>")

                render_html(f"""
                    <div class="tx-row">
                        <span class="tx-key">Statut réel historique</span>
                        <span class="tx-val" style="color:{'#dc2626' if label_reel else '#16a34a'}">{'Frauduleuse' if label_reel else 'Légitime'}</span>
                    </div>
                    <div class="tx-row">
                        <span class="tx-key">Prédiction du modèle</span>
                        <span class="tx-val" style="color:{'#dc2626' if est_anomalie else '#16a34a'}">{'Anomalie' if est_anomalie else 'Légitime'}</span>
                    </div>
                    <div class="tx-row">
                        <span class="tx-key">Résultat</span>
                        <span class="tx-val" style="color:{'#16a34a' if est_anomalie == label_reel else '#ea580c'}">
                            {'Vrai positif' if est_anomalie and label_reel else 'Vrai négatif' if not est_anomalie and not label_reel else 'Faux positif' if est_anomalie and not label_reel else 'Faux négatif'}
                        </span>
                    </div>
                """)

                if est_anomalie == label_reel:
                    st.success("Le diagnostic du modèle est conforme au statut réel.")
                elif est_anomalie and not label_reel:
                    st.warning("Faux positif — Transaction légitime signalée comme suspecte.")
                else:
                    st.error("Faux négatif — Cette fraude n'a pas été détectée par le modèle.")

                render_html("""
                    <div class="note" style="margin-top:14px;">
                        Un écart entre le diagnostic et la réalité est attendu en mode non supervisé :
                        le modèle n'a pas eu accès aux labels lors de son entraînement.
                        Les alertes doivent être soumises à une validation humaine avant
                        toute décision de blocage.
                    </div>
                """)