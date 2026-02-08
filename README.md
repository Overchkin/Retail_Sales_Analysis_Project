# Retail_Sales_Analysis_Project

## 📌 Objectif du projet

Ce projet a pour objectif de transformer des **données de ventes brutes** en **insights business exploitables**, via une analyse approfondie, des segments clients RFM, des prévisions de valeur client (LTV) et une **application interactive** pour la prise de décision par un décideur non technique.

---

## 🗂 Structure du projet

```
Retail_Sales_Analysis_Project/
│
├─ .gitignore                
├─ README.md                 
├─ Workflow.md               
├─ requirements.txt          
│
├─ data/
│   ├─ raw/                  # Dataset original
│   ├─ processed/            # Données nettoyées et RFM
│
├─ notebooks/
│   ├─ 01_data_cleaning.ipynb
│   ├─ 02_eda.ipynb
│   ├─ 03_rfm_segmentation.ipynb
│   ├─ 04_ml_modeling.ipynb
│
├─ src/
│   ├─ data_processing.py     
│   ├─ feature_engineering.py
│   ├─ rfm_segmentation.py    
│   ├─ ml_model.py            
│   ├─ visualisation.py       
│
├─ app/
│   ├─ streamlit_app.py      
│
├─ models/
│   ├─ customer_revenue_model.pkl
│
└─ reports/
    ├─ figures/              
    ├─ summary_report.pdf    
```

---

## 🛠 Technologies et librairies utilisées

* **Python 3.9+**
* Data manipulation: `pandas`, `numpy`
* Visualisation: `plotly`
* Machine Learning: `scikit-learn`
* Web app: `streamlit`
* Serialisation modèle: `joblib`

---

## 🔹 Description des modules

### 1️⃣ Data Processing (`src/data_processing.py`)

* Chargement et nettoyage des données brutes.
* Suppression des doublons et anomalies.
* Calcul du chiffre d’affaires par transaction.

### 2️⃣ Feature Engineering (`src/feature_engineering.py`)

* Extraction des composantes temporelles (année, mois, jour, heure).
* Ajout du chiffre d’affaires cumulé par client.

### 3️⃣ RFM Segmentation (`src/rfm_segmentation.py`)

* Calcul des métriques **RFM** pour chaque client :

  * **Recency** : jours depuis dernier achat
  * **Frequency** : nombre de commandes
  * **Monetary** : valeur monétaire totale
* Attribution des scores R, F, M et score RFM global.
* Segmentation des clients pour analyses business et marketing.

### 4️⃣ Machine Learning (`src/ml_model.py`)

* Modélisation prédictive de la valeur client (LTV) avec **Random Forest**.
* Évaluation avec **MAE**.
* Export du modèle final (`models/customer_revenue_model.pkl`) pour intégration.

### 5️⃣ Visualisation (`src/visualisation.py`)

* Graphiques interactifs pour :

  * Chiffre d’affaires par pays
  * Évolution mensuelle
  * Distribution des segments RFM

### 6️⃣ Application interactive (`app/streamlit_app.py`)

* Dashboard BI interactif avec **Streamlit**.
* Filtrage par pays et année.
* KPI clés : chiffre d’affaires, commandes, clients uniques, articles vendus.
* Analyses multi-pays et visualisations interactives.
* Segmentation RFM et visualisation des distributions.
* Calcul de **LTV** et **churn**, heatmap pour identifier les clients à risque.

---

## 💾 Fichiers de données

* `data/raw/OnlineRetail.xlsx` : dataset original.
* `data/processed/online_retail_clean.csv` : données nettoyées.
* `data/processed/rfm_segmentation.csv` : métriques RFM calculées.

---

## 🚀 Instructions pour exécuter le projet

1. **Cloner le projet**

```bash
git clone https://github.com/Overchkin/Retail_Sales_Analysis_Project.git
cd Retail_Sales_Analysis_Project
```

2. **Installer les dépendances**

```bash
pip install -r requirements.txt
```

3. **Exécuter les notebooks pour vérifier les étapes**

```bash
jupyter notebook
```

4. **Lancer l’application interactive**

```bash
streamlit run app/streamlit_app.py
```

---

## 📊 Résultats attendus

* **Analyse exploratoire** : chiffre d’affaires global, évolution mensuelle, top pays et clients.
* **Segmentation RFM** : 5 segments principaux basés sur Recency, Frequency et Monetary.
* **Modèle prédictif LTV** : estimation de la valeur client future.
* **Dashboard interactif** : filtres multi-pays/année, KPI, graphiques et heatmaps.

---

## 📝 Notes

* Le projet est **modulaire** : chaque étape (data cleaning, EDA, RFM, ML, dashboard) peut être exécutée séparément.
* **Reproductibilité** garantie via `random_state=42` pour ML et split.
* Le projet est conçu pour un **décideur non technique**, avec des visuels intuitifs et interactifs.

---

## 📌 Auteur

**Israël – Software Engineer & Data Scientist/IA**
Portfolio et projets Data Science / Full-Stack
