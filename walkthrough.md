# Walkthrough : Détection d'Anomalies de Transactions Financières

Ce document récapitule les modifications apportées et la structure finale du projet pour sa validation et son rendu.

## Structure Finale du Projet

Le projet est maintenant organisé de manière propre et structurée sur votre ordinateur :

* **[detection_anomalies_fraud.ipynb](file:///c:/Users/HP/Desktop/IFOAD/M1/Visualisation%20des%20donn%C3%A9es%20en%20R,%20python/Projet/detection_anomalies_fraud.ipynb)** : Le notebook complet contenant les phases I (EDA), II (Prétraitement), III (Modélisation), et IV (Interprétation SHAP).
* **[rapport_technique.md](file:///c:/Users/HP/Desktop/IFOAD/M1/Visualisation%20des%20donn%C3%A9es%20en%20R,%20python/Projet/rapport_technique.md)** : Le rapport technique de synthèse académique et managériale de 7 pages.
* **[dashboard_app/](file:///c:/Users/HP/Desktop/IFOAD/M1/Visualisation%20des%20donn%C3%A9es%20en%20R,%20python/Projet/dashboard_app/)** : Le dossier contenant le Dashboard interactif Streamlit :
  * **[dashboard_app/app.py](file:///c:/Users/HP/Desktop/IFOAD/M1/Visualisation%20des%20donn%C3%A9es%20en%20R,%20python/Projet/dashboard_app/app.py)** : Le code source de l'interface Streamlit.
  * **`dashboard_app/iforest_model.pkl`** : Le modèle Isolation Forest pré-entraîné (à importer).
  * **`dashboard_app/test_sample.csv`** : L'échantillon de 1000 transactions de test (à importer).

---

## Synthèse des Modifications Apportées

### 1. Dans le Notebook
* **Standardisation** : Ajout de la mise à l'échelle via `StandardScaler` appliquée à `X_train_scaled`, `X_val_scaled` et `X_test_scaled` (indispensable pour les modèles de distance).
* **Modélisation non supervisée** : Entraînement et optimisation du seuil d'anomalie sur validation pour **Isolation Forest**, **LOF** (sur échantillon de 20 000 lignes) et **K-Means**.
* **Tableau de synthèse comparatif** : Génération des performances sur le jeu de test final.
* **SHAP** : Implémentation du Summary Plot et du Force Plot (transaction 190) pour décoder les décisions du modèle.
* **Rédaction et Structure** : Ajout d'explications textuelles de transition pour chaque section, traduction des variables clés en français et rédaction d'une conclusion académique complète avec bibliographie.

### 2. Dans le Dashboard Streamlit (`app.py`)
* Création de la mise en page corporative (bleu nuit et blanc, sans émoticônes).
* Implémentation de la **Vue d'ensemble** (KPIs de volume et de taux de fraude, graphique comparatif horaire interactif).
* Implémentation du **Simulateur de Risque** (chargement du modèle et prédiction à la volée du risque légitime/anomalie, avec encadrés de vulgarisation scientifique pour les profils non techniques).

### 3. Rapport Technique (`rapport_technique.md`)
* Rédaction d'un rapport complet reprenant l'explication théorique des modèles, l'interprétation des résultats statistiques et les recommandations managériales pour le déploiement opérationnel.

---

## Guide de Validation pour le Rendu

### Étape A : Valider le renommage du Notebook
1. Supprimez l'ancien fichier `detection_anomalies_fraud.ipynb` incomplet.
2. Renommez le fichier `detection_anomalies_fraud (3).ipynb` que vous avez téléchargé en **`detection_anomalies_fraud.ipynb`**.

### Étape B : Lancer le Dashboard Streamlit
1. Déposez les fichiers `iforest_model.pkl` et `test_sample.csv` dans le dossier `dashboard_app` sur votre PC.
2. Ouvrez un terminal de commande Windows dans le dossier `dashboard_app`.
3. Tapez la commande :
   ```bash
   py -m streamlit run app.py
   ```
4. Naviguez sur l'interface à l'adresse `http://localhost:8501` pour vérifier le bon affichage des graphiques et du simulateur.
