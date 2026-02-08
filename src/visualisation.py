import plotly.express as px


def revenue_by_country(df):
    fig = px.bar(
        df.groupby("Country", as_index=False)["Revenue"].sum(),
        x="Country",
        y="Revenue",
        title="Revenue par pays"
    )
    return fig


def monthly_revenue(df):
    monthly = (
        df.groupby(["InvoiceYear", "InvoiceMonth"], as_index=False)["Revenue"]
        .sum()
    )

    fig = px.line(
        monthly,
        x="InvoiceMonth",
        y="Revenue",
        color="InvoiceYear",
        title="Évolution mensuelle du chiffre d'affaires"
    )
    return fig


def rfm_distribution(rfm):
    fig = px.histogram(
        rfm,
        x="RFM_Score",
        nbins=15,
        title="Distribution des scores RFM"
    )
    return fig
