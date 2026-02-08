import pandas as pd
from datetime import timedelta

def compute_rfm(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcule les métriques RFM pour chaque client dans le DataFrame filtré.
    Gère les clients sans commande après filtrage.
    """
    # Supprimer lignes invalides
    df = df.dropna(subset=['InvoiceDate', 'Customer_ID', 'Revenue'])

    if df.empty:
        # Si le sous-ensemble est vide après filtrage
        return pd.DataFrame(columns=['Customer_ID', 'Recency', 'Frequency', 'Monetary'])

    snapshot_date = df['InvoiceDate'].max() + timedelta(days=1)

    def calc_recency(x):
        last_order = x.max()
        if pd.isnull(last_order):
            return None
        return (snapshot_date - last_order).days

    rfm = df.groupby('Customer_ID').agg({
        'InvoiceDate': calc_recency,
        'InvoiceNo': 'nunique',
        'Revenue': 'sum'
    }).reset_index()

    rfm.columns = ['Customer_ID', 'Recency', 'Frequency', 'Monetary']

    # Supprimer les clients avec Recency invalide
    rfm = rfm.dropna(subset=['Recency'])
    rfm['Recency'] = rfm['Recency'].astype(int)

    return rfm

def rfm_scoring(rfm: pd.DataFrame) -> pd.DataFrame:
    """
    Crée les scores R, F, M et le score RFM total.
    """
    rfm = rfm.copy()
    if rfm.empty:
        return rfm

    rfm['R'] = pd.qcut(rfm['Recency'], 5, labels=[5,4,3,2,1], duplicates='drop')
    rfm['F'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1,2,3,4,5], duplicates='drop')
    rfm['M'] = pd.qcut(rfm['Monetary'], 5, labels=[1,2,3,4,5], duplicates='drop')

    rfm['RFM_Score'] = rfm['R'].astype(int) + rfm['F'].astype(int) + rfm['M'].astype(int)

    return rfm
