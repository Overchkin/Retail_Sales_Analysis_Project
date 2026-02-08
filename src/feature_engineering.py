import pandas as pd


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """Extraction des composantes temporelles depuis la date de facture"""
    df["InvoiceYear"] = df["InvoiceDate"].dt.year      # Année de la transaction
    df["InvoiceMonth"] = df["InvoiceDate"].dt.month    # Mois (1-12)
    df["InvoiceDay"] = df["InvoiceDate"].dt.day        # Jour du mois (1-31)
    df["InvoiceHour"] = df["InvoiceDate"].dt.hour      # Heure de la journée (0-23)
    return df


def add_customer_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """Ajout du chiffre d'affaires cumulé par client à chaque transaction"""
    # Agrégation du CA total par identifiant client
    customer_revenue = (
        df.groupby("Customer_ID")["Revenue"]
        .sum()
        .reset_index(name="TotalRevenue")
    )

    # Fusion avec le DataFrame original pour enrichir chaque ligne
    return df.merge(customer_revenue, on="Customer_ID", how="left")