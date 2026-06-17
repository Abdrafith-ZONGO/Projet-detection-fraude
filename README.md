# 🛡️ Détection d'Anomalies Comportementales - IEEE-CIS Fraud Detection

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit App](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.2+-F7931E.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Ce projet de détection de fraudes transactionnelles s'inscrit dans le cadre du **Master 1 Data Science (IFOAD)** de l'**Université Joseph Ki-Zerbo** (Juin 2026). 

L'objectif est de concevoir un système d'apprentissage non supervisé capable d'identifier les transactions bancaires atypiques en ligne à partir du célèbre jeu de données de la compétition Kaggle **IEEE-CIS Fraud Detection** (2019). Le projet s'appuie sur l'algorithme de forêt d'isolation (**Isolation Forest**) et propose un tableau de bord interactif pour l'aide à la décision.

---

## 📂 Structure du Projet

```text
├── README.md                           <- Guide d'installation et de démarrage
├── requirements.txt                    <- Liste globale des packages requis pour le projet
├── detection_anomalies_fraud (3).ipynb <- Le notebook Jupyter complet (EDA, Modélisation, SHAP)
├── rapport_technique.md                <- Rapport académique détaillé
├── Rapport_Executif_Simplifie.md       <- Synthèse managériale et glossaire
└── dashboard_app/                      <- Répertoire de l'application interactive
    ├── app.py                          <- Code source de l'application Streamlit (dashboard)
    ├── iforest_model.pkl               <- Le modèle Isolation Forest pré-entraîné
    ├── scaler.pkl                      <- StandardScaler de Scikit-Learn
    └── test_sample.csv                 <- Échantillon de test (5 000 transactions brutes)
```

> ⚠️ **Note sur les volumes de données** : Les fichiers originaux de Kaggle (`train_transaction.csv`, `test_transaction.csv`, etc.) font plus de 1,3 Go et ont été exclus de l'archive Git. Le modèle et le sous-ensemble `test_sample.csv` fournis dans `dashboard_app/` sont suffisants pour exécuter et tester le dashboard localement sans télécharger la totalité des données d'origine.

---

## 🚀 Guide d'Installation et Exécution

Suivez les étapes ci-dessous pour lancer le projet dans votre environnement local.

### 1. Cloner le dépôt GitHub
```bash
git clone https://github.com/votre-username/votre-depot.git
cd votre-depot
```

### 2. Configurer l'environnement virtuel (Recommandé)
Créez et activez un environnement virtuel Python pour isoler les dépendances :

**Sur Windows (PowerShell) :**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Sur Linux / macOS :**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Installer les dépendances
Installez les packages nécessaires répertoriés dans le fichier de configuration :
```bash
pip install -r dashboard_app/requirements.txt
```

### 4. Lancer le Dashboard interactif (Streamlit)
Déplacez-vous dans le répertoire de l'application et démarrez le serveur Streamlit :
```bash
cd dashboard_app
streamlit run app.py
```
L'application s'ouvrira automatiquement à l'adresse : **[http://localhost:8501](http://localhost:8501)**.

---

## 📈 Fonctionnalités du Dashboard Streamlit

L'interface se compose de deux pages principales conçues avec une esthétique moderne :

### 📊 Page 1 — Vue d'ensemble (Dashboard Managérial)
* **Indicateurs KPIs** : Analyse synthétique des volumes de transaction, taux de fraudes réelles détectées, alertes de l'IA et montants moyens.
* **Analyses temporelles** : Graphiques du taux de fraude par heure (mettant en évidence les pics nocturnes de 0h à 5h).
* **Profils de cartes** : Graphiques du taux de fraude selon le type de carte (Crédit vs Débit).
* **Aide à l'évaluation** : Analyse interactive de la distribution du score d'anomalie produit par l'algorithme.

### 🔍 Page 2 — Simulateur de Risque (Aide à la Décision)
* **Sélection interactive** : Choix d'une transaction du dataset via son index.
* **Diagnostic IA** : Calcul en temps réel du score d'anomalie par le modèle *Isolation Forest* (seuil calibré à `-0.026048`) et rendu visuel du verdict (Risque élevé vs Risque faible).
* **Vérification terrain** : Comparaison immédiate entre le statut réel historique de la transaction (fraude/légitime) et le diagnostic de l'IA (Vrai Positif, Vrai Négatif, Faux Positif, Faux Négatif).

---

## 🛠️ Aperçu de la Modélisation (*Notebook*)
* **Algorithme** : Isolation Forest (Apprentissage non supervisé).
* **Feature Engineering** : 6 nouvelles caractéristiques comportementales créées (`montant_log`, `ratio_montant`, `frequence_carte`, `frequence_email`, `heure_transaction`, `est_weekend`).
* **Calibrage du Seuil** : Déterminé sur l'ensemble de validation à `-0.026048` afin de maximiser le Rappel (détecter un maximum de fraudes tout en maintenant un taux acceptable de faux positifs).

---

## 🧑‍💻 Auteur
* **Développeur** : **Abdrafith Zongo**
* **Cursus** : Master 1 Data Science — IFOAD
* **Université** : Université Joseph Ki-Zerbo (Burkina Faso)
* **Date** : Juin 2026
