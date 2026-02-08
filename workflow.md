# Workflow – Retail_Sales_Analysis_Project

Ce document décrit le flux de travail complet du projet **Retail_Sales_Analysis_Project**, depuis la collecte des données jusqu'à l'application interactive et le modèle prédictif.

---

## 1. Préparation de l'environnement

1. Cloner le dépôt GitHub :

```bash
git clone https://github.com/Overchkin/Retail_Sales_Analysis_Project.git
```

2. Se positionner dans le dossier du projet :

```bash
cd Retail_Sales_Analysis_Project
```

3. Installer les dépendances Python :

```bash
pip install -r requirements.txt
```

---

## 2. Préparation et nettoyage des données

1. **Chargement des données brutes** :

   * Fichier source : `data/raw/OnlineRetail.xlsx`
   * Script : `src/data_processing.py`

```python
from src.data_processing import load_raw_data, clean_data, save_processed_data

df = load_raw_data('data/raw/OnlineRetail.xlsx')
df_clean = clean_data(df)
save_processed_data(df_clean, 'data/processed/online_retail_clean.csv')
```

2. **Nettoyage effectué** :

   * Suppression des factures annulées (InvoiceNo commençant par 'C')
   * Suppression des lignes sans `Customer_ID`
   * Conversion des types (`Customer_ID`, `InvoiceDate`)
   * Suppression des doublons
   * Calcul du `Revenue` par transaction
   * Filtrage des valeurs négatives ou nulles

---

## 3. Analyse exploratoire (EDA)

1. **Chargement des données nettoyées** :

```python
import pandas as pd
df = pd.read_csv('data/processed/online_retail_clean.csv')
```

2. **Analyse et visualisation** :

   * Statistiques descriptives globales
   * Chiffre d'affaires total, nombre de clients, commandes et produits
   * Évolution mensuelle du CA
   * Top 10 pays par CA
   * Distribution du CA par client
3. **Notebooks EDA** : `notebooks/02_eda.ipynb`

---

## 4. Feature Engineering

1. **Ajout des features temporelles** :

```python
from src.feature_engineering import add_time_features, add_customer_revenue

df = add_time_features(df)
df = add_customer_revenue(df)
```

2. **Features créées** :

   * `InvoiceYear`, `InvoiceMonth`, `InvoiceDay`, `InvoiceHour`
   * `TotalRevenue` par client
3. **Scripts** : `src/feature_engineering.py`

---

## 5. Segmentation RFM

1. **Calcul des métriques RFM** :

```python
from src.rfm_segmentation import compute_rfm, rfm_scoring

rfm = compute_rfm(df)
rfm = rfm_scoring(rfm)
rfm.to_csv('data/processed/rfm_segmentation.csv', index=False)
```

2. **Segmentation clients** :

   * Recency (R) : jours depuis dernier achat
   * Frequency (F) : nombre de commandes
   * Monetary (M) : valeur monétaire totale
   * Score RFM : R + F + M
3. **Notebook RFM** : `notebooks/03_rfm_segmentation.ipynb`

---

## 6. Modélisation prédictive (LTV)

1. **Chargement des données RFM**

```python
import pandas as pd
rfm = pd.read_csv('data/processed/rfm_segmentation.csv')
```

2. **Entraînement modèle Random Forest**

```python
from src.ml_model import train_ltv_model

model, mae = train_ltv_model(rfm)
```

3. **Évaluation** :

   * `MAE` pour l'erreur absolue
   * Visualisation Actual vs Predicted
4. **Sauvegarde du modèle** : `models/customer_revenue_model.pkl`
5. **Notebook ML** : `notebooks/04_ml_modeling.ipynb`

---

## 7. Visualisation et Dashboard

1. **Application Streamlit** : `app/streamlit_app.py`
2. **Fonctionnalités** :

   * Filtres interactifs (pays, années, segments RFM)
   * KPIs clés : chiffre d'affaires, commandes, clients uniques, articles vendus
   * Visualisations : CA mensuel, CA par pays, distribution RFM
   * LTV et churn analysis
3. **Exécution** :

```bash
streamlit run app/streamlit_app.py
```

---

## 8. Visualisations prédéfinies

* `src/visualisation.py` contient des fonctions réutilisables :

  * `revenue_by_country(df)`
  * `monthly_revenue(df)`
  * `rfm_distribution(rfm)`

---

## 9. Structure finale du projet

```
Retail_Sales_Analysis_Project/
│
├─ .gitignore
├─ README.md
├─ Workflow.md
├─ requirements.txt
├─ data/
│  ├─ raw/
│  └─ processed/
├─ notebooks/
│  ├─ 01_data_cleaning.ipynb
│  ├─ 02_eda.ipynb
│  ├─ 03_rfm_segmentation.ipynb
│  └─ 04_ml_modeling.ipynb
├─ src/
│  ├─ data_processing.py
│  ├─ feature_engineering.py
│  ├─ rfm_segmentation.py
│  ├─ ml_model.py
│  └─ visualisation.py
├─ app/
│  └─ streamlit_app.py
└─ models/
   └─ customer_revenue_model.pkl
```

---

## 10. Bonnes pratiques

* Toujours nettoyer les données brutes avant l'analyse
* Utiliser la normalisation/standardisation pour le clustering
* Sauvegarder les modèles et données traitées pour reproductibilité
* Utiliser les notebooks pour documentation et visualisation interactive
