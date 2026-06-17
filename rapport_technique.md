# Rapport Technique : Détection d'Anomalies Comportementales dans les Transactions Numériques

**Auteur :** Abdrafith ZONGO  
**Niveau :** Master 1 Data Science  
**Institution :** Université Joseph Ki-Zerbo / IFOAD  
**Date :** 17 Juin 2026  

---

## 1. Introduction et Problématique Métier

L'essor fulgurant des paiements en ligne et des services transactionnels numériques a multiplié les opportunités d'attaques frauduleuses. Pour les institutions financières, le coût de la fraude ne se limite pas aux pertes directes, mais englobe également le coût opérationnel d'investigation et l'impact sur la confiance des clients. 

Traditionnellement, la détection repose sur des moteurs de règles statiques (ex: bloquer si le montant dépasse X). Cependant, les fraudeurs adaptent continuellement leurs stratégies. Ce projet propose une approche moderne : **la détection d'anomalies comportementales par apprentissage non supervisé**. L'objectif est d'identifier les comportements de fraude comme étant des anomalies statistiques par rapport à la "norme" des transactions légitimes, sans dépendre d'étiquettes de fraude lors de la phase d'apprentissage.

---

## 2. Exploration des Données (EDA) et Analyse Temporelle

Le projet s'appuie sur le dataset **IEEE-CIS Fraud Detection** (Kaggle), composé de deux fichiers fusionnés via la clé `TransactionID` :
* `train_transaction.csv` : Données financières brutes (590 540 lignes, 394 colonnes).
* `train_identity.csv` : Informations de connexion et de terminal (144 233 lignes, 40 colonnes).

### Signes et caractéristiques statistiques d'une fraude
Notre analyse exploratoire (EDA) a mis en évidence plusieurs comportements anormaux caractéristiques :
1. **La Dimension Temporelle (Heure de la journée)** : L'extraction de l'heure (`TransactionHour`) montre que le taux de fraude grimpe fortement durant les **heures creuses (la nuit, de 0h à 5h)**. Durant cette période, le volume de transactions légitimes est au plus bas, et les fraudeurs automatisent leurs attaques de type "carding" (tests de cartes par robots).
2. **Le Profil Financier (Montants)** : Bien que la fraude touche toutes les gammes de prix, les distributions montrent une plus forte variabilité et des valeurs atypiques pour les montants frauduleux.
3. **Le Type de Paiement et Produit** : Les **cartes de crédit** (`card6`) affichent un taux de fraude deux fois supérieur aux cartes de débit. De plus, le code de produit **'C'** (souvent lié à des transactions transfrontalières ou téléphoniques) est statistiquement le plus à risque.

---

## 3. Pipeline de Prétraitement et Feature Engineering

Avant de soumettre les données aux modèles, un pipeline de prétraitement rigoureux a été implémenté pour éliminer le bruit et structurer les données :

1. **Réduction de dimension** : Élimination des colonnes contenant plus de 60 % de valeurs manquantes (les variables trop creuses nuisent à l'apprentissage). Nous avons toutefois préservé les 20 variables les plus fortement corrélées à la cible `isFraud`. Le jeu de données est ainsi passé de 434 à 219 colonnes.
2. **Imputation des valeurs manquantes** : 
   * Variables numériques : Remplacement des manquants par la **médiane** (robuste aux valeurs aberrantes).
   * Variables catégorielles (dont la colonne textuelle `id_12`) : Remplacées par la mention **"Unknown"** pour conserver l'absence d'information comme un signal comportemental.
3. **Label Encoding** : Conversion de toutes les variables textuelles qualitatives en nombres entiers uniques via `LabelEncoder` de Scikit-Learn.
4. **Partitionnement Stratifié** : Découpage des données en Train (60 %), Validation (20 %) et Test (20 %). L'utilisation d'une stratification garantit que chaque sous-ensemble conserve le ratio de fraude réel de ~3,5 %, évitant ainsi un biais d'entraînement.
5. **Standardisation (Scaling)** : Application de `StandardScaler` pour ramener chaque variable à une moyenne de 0 et une variance de 1. Cette étape est indispensable pour K-Means et LOF, qui sont fondés sur le calcul des distances géométriques.

---

## 4. Modélisation et Comparaison des Performances

Trois algorithmes d'apprentissage non supervisés ont été entraînés sur le jeu d'entraînement, optimisés sur le jeu de validation (pour trouver le seuil d'anomalie qui maximise le F1-Score), puis évalués sur le jeu de test final.

### Tableau comparatif sur le Jeu de Test final :
| Modèle | Précision | Rappel | F1-Score | ROC-AUC | Profil opérationnel |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Isolation Forest** | **18,28 %** | 15,03 % | **16,50 %** | 71,85 % | **Conservateur** : Moins de fausses alertes, cible la fraude de manière très précise. |
| **Local Outlier Factor (LOF)** | 9,74 % | **31,60 %** | 14,88 % | 67,67 % | **Sécuritaire** : Détecte un maximum de fraudes mais génère beaucoup de fausses alertes. |
| **K-Means Clustering** | 12,34 % | 23,31 % | 16,14 % | **72,98 %** | **Équilibré** : Offre la meilleure capacité de séparation globale (ROC-AUC). |

### Analyse décisionnelle de la modélisation :
* **Isolation Forest** est le plus robuste pour minimiser le coût opérationnel d'investigation, car sa précision est la plus élevée (18,28 %, soit 8 fois plus efficace qu'un tirage aléatoire).
* **LOF** offre le meilleur filet de sécurité avec **31,60 %** de détection (rappel), mais nécessite une équipe d'analystes importante pour traiter le grand volume de faux positifs.
* **K-Means** offre le meilleur équilibre géométrique général avec une excellente aire sous la courbe ROC (**72,98 %**).

---

## 5. Interprétabilité du Modèle avec SHAP

La modélisation par forêt d'isolation a été décryptée grâce à la méthode **SHAP (SHapley Additive exPlanations)**, qui attribue un score d'importance (valeur de Shapley) à chaque variable pour expliquer les décisions de l'algorithme.

* **Impact Global (Summary Plot)** : Les caractéristiques de sécurité réseau "Vesta" (ex: `V48`, `V289`, `V83`) et la distance temporelle entre les transactions d'un utilisateur (`D3`) sont les variables les plus discriminantes. Par exemple, des valeurs élevées de `V48` ou `V289` (points rouges) réduisent drastiquement le score de transaction, la poussant vers le statut d'anomalie.
* **Impact Local (Explication de la fraude 190)** : L'analyse locale d'une transaction frauduleuse montre que son score est tombé à `9.28` (très en dessous du seuil de normalité de 14.8). Les principales causes de cette alerte sont les variables **`C11 = 2454`** et **`C4 = 1738`**. Sur le plan métier, des compteurs d'opérations successives aussi élevés sur une carte bancaire révèlent de manière indiscutable une **attaque automatisée par robot (botting)** pour tester des numéros de cartes.

---

## 6. Présentation du Livrable : Le Dashboard Streamlit

Pour rendre ces résultats exploitables, un tableau de bord web interactif a été conçu (`app.py`) avec un style sobre, professionnel et sans émoticônes. Il est structuré en deux sections majeures :

1. **Vue d'ensemble (Décisionnel)** : Destiné aux décideurs, il présente les KPIs de performance du système (Volume, Taux de fraude réel, Anomalies détectées par l'IA) et propose une comparaison temporelle linéaire montrant la corrélation entre les pics réels de fraude et les détections nocturnes de notre modèle.
2. **Simulateur de Risque (Opérationnel)** : Destiné aux analystes fraude, il permet de sélectionner une transaction du jeu de test pour visualiser ses caractéristiques et lancer l'évaluation en direct. L'application calcule le score d'anomalie et affiche de manière claire le verdict (VALIDATION vs ALERTE), accompagné de textes expliquant la décision (seuil critique de `-0.026048`).

---

## 7. Conclusion, Limites et Perspectives

Ce projet démontre l'efficacité de l'apprentissage non supervisé pour détecter des fraudes sans dépendre de données préalablement étiquetées. 

### Limites identifiées :
1. **Déséquilibre extrême** : Avec seulement ~3,5 % de fraudes dans la population, caler le seuil de décision est complexe.
2. **Anonymisation** : L'utilisation de variables masquées (ex: `V48`, `C11`) limite l'analyse métier fine et concrète pour un analyste terrain.

### Perspectives :
* **Approche hybride/supervisée** : L'intégration d'un modèle supervisé (XGBoost ou LightGBM) en complément permettrait d'augmenter le rappel sur les fraudes historiques connues.
* **Techniques de rééquilibrage** : L'utilisation de méthodes de suréchantillonnage comme SMOTE sur les données d'entraînement.
* **Modèles Deep Learning** : L'implémentation d'Auto-encodeurs pour capturer des relations non linéaires plus complexes.

---

## Références Bibliographiques

1. **Liu, F. T., Ting, K. M., et Zhou, Z. H. (2008).** *Isolation Forest*. IEEE International Conference on Data Mining (ICDM).
2. **Breunig, M. M., Kriegel, H. P., Ng, R. T., et Sander, J. (2000).** *LOF: Identifying Density-Based Local Outliers*. ACM SIGMOD Record.
3. **Lundberg, S. M., et Lee, S. I. (2017).** *A Unified Approach to Interpreting Model Predictions*. Advances in Neural Information Processing Systems (NeurIPS).
4. **IEEE-CIS Fraud Detection (2019).** Kaggle Competition Dataset.
