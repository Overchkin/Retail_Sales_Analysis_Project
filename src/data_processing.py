import pandas as pd


def load_raw_data(path: str) -> pd.DataFrame:
    """Charge les données brutes depuis un fichier Excel source"""
    return pd.read_excel(path)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Nettoyage principal du dataset Online Retail"""

    # Standardisation des noms de colonnes pour cohérence projet
    df = df.rename(columns={
        "Invoice": "InvoiceNo",
        "Price": "UnitPrice",
        "Customer ID": "Customer_ID"
    })

    # Élimination des transactions annulées (factures préfixées par 'C')
    df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]

    # Retrait des lignes sans identification client (analyse comportementale impossible)
    df = df.dropna(subset=["Customer_ID"])

    # Conversion des types pour exploitation temporelle et jointures
    df["Customer_ID"] = df["Customer_ID"].astype(int)
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    # Calcul du chiffre d'affaires par transaction unitaire
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]

    # Filtrage des anomalies commerciales (erreurs de saisie ou remboursements)
    df = df[df["Revenue"] > 0]

    return df


def save_processed_data(df: pd.DataFrame, output_path: str):
    """Export des données nettoyées vers fichier CSV sans index"""
    df.to_csv(output_path, index=False)