import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error


def train_ltv_model(rfm: pd.DataFrame):
    """Entraînement d'un modèle prédictif de Lifetime Value (LTV) client"""

    # Définition des variables explicatives (features RFM)
    X = rfm[["Recency", "Frequency", "Monetary"]]

    # Variable cible : valeur monétaire actuelle comme proxy du LTV futur
    y = rfm["Monetary"]

    # Division des données : 80% entraînement, 20% test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Initialisation du modèle Random Forest avec 200 arbres
    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42
    )

    # Entraînement sur les données d'apprentissage
    model.fit(X_train, y_train)

    # Évaluation des performances sur l'ensemble de test
    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)

    return model, mae