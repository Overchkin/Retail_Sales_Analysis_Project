# ==========================================
# STREAMLIT APP – ONLINE RETAIL DASHBOARD (ULTIME & ROBUSTE & INTERACTIF)
# ==========================================

import sys
import os
import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# FIX MODULE PATH
# -----------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# -----------------------------
# IMPORTS
# -----------------------------
from src.feature_engineering import add_time_features
from src.rfm_segmentation import compute_rfm, rfm_scoring
from src.visualisation import (
    revenue_by_country,
    monthly_revenue,
    rfm_distribution
)

# -----------------------------
# CONFIG APP
# -----------------------------
st.set_page_config(
    page_title="Online Retail – Business Dashboard",
    layout="wide"
)

st.title("📊 Online Retail – Business Intelligence Dashboard")
st.markdown(
    """
    Cette application transforme des **données de ventes brutes**
    en **insights business exploitables** pour la prise de décision.
    """
)

# -----------------------------
# LOAD DATA
# -----------------------------
PROCESSED_CSV_PATH = os.path.join(
    PROJECT_ROOT, "data", "processed", "online_retail_clean.csv"
)

@st.cache_data
def load_and_prepare_data(csv_path):
    df = pd.read_csv(csv_path, parse_dates=["InvoiceDate"])
    df = add_time_features(df)
    return df

df = load_and_prepare_data(PROCESSED_CSV_PATH)

# =========================================================
# SIDEBAR FILTERS – FORM + RESET
# =========================================================
st.sidebar.header("🎛️ Filtres")

# --- Session state initial ---
if "selected_country" not in st.session_state:
    st.session_state.selected_country = []
if "selected_year" not in st.session_state:
    st.session_state.selected_year = []
if "applied_filters" not in st.session_state:
    st.session_state.applied_filters = False

with st.sidebar.form("filter_form"):

    country_options = sorted(df["Country"].dropna().unique())
    year_options = sorted(df["InvoiceYear"].dropna().unique())

    selected_country = st.multiselect(
        "Pays",
        options=country_options,
        default=st.session_state.selected_country
    )

    selected_year = st.multiselect(
        "Année",
        options=year_options,
        default=st.session_state.selected_year
    )

    col_apply, col_reset = st.columns(2)
    apply_filters = col_apply.form_submit_button("✅ Appliquer")
    reset_filters = col_reset.form_submit_button("🔄 Réinitialiser")

# -----------------------------
# RESET FILTERS
# -----------------------------
if reset_filters:
    st.session_state.selected_country = []
    st.session_state.selected_year = []
    st.session_state.applied_filters = False
    st.info("ℹ️ Les filtres ont été réinitialisés. Veuillez sélectionner de nouveaux filtres et cliquer sur ✅ Appliquer pour afficher les données.")

# -----------------------------
# APPLY FILTERS
# -----------------------------
if apply_filters:
    if not selected_country or not selected_year:
        st.warning("⚠️ Veuillez sélectionner au moins un pays et une année avant d'appliquer les filtres.")
    else:
        st.session_state.selected_country = selected_country
        st.session_state.selected_year = selected_year
        st.session_state.applied_filters = True

# -----------------------------
# STOP IF NO FILTERS APPLIED
# -----------------------------
if not st.session_state.applied_filters:
    st.info("ℹ️ Veuillez sélectionner des filtres puis cliquer sur ✅ Appliquer pour afficher les données.")
    st.stop()

# -----------------------------
# APPLY DATA FILTERING
# -----------------------------
filtered_df = df[
    (df["Country"].isin(st.session_state.selected_country)) &
    (df["InvoiceYear"].isin(st.session_state.selected_year))
]

if filtered_df.empty:
    st.warning("⚠️ Aucun client / vente disponible pour ces filtres.")
    st.stop()

st.caption(
    f"📍 Filtres appliqués : {len(st.session_state.selected_country)} pays · {len(st.session_state.selected_year)} années"
)

# =========================================================
# KPI METRICS
# =========================================================
st.subheader("📌 Indicateurs clés")
col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Chiffre d'affaires", f"${filtered_df['Revenue'].sum():,.0f}")
col2.metric("🧾 Commandes", filtered_df["InvoiceNo"].nunique())
col3.metric("👥 Clients uniques", filtered_df["Customer_ID"].nunique())
col4.metric("📦 Articles vendus", int(filtered_df["Quantity"].sum()))

# =========================================================
# COMPARAISON MULTI-PAYS
# =========================================================
st.subheader("🌍 Comparaison multi-pays")
country_kpi = (
    filtered_df
    .groupby("Country")
    .agg(
        Revenue=("Revenue", "sum"),
        Orders=("InvoiceNo", "nunique"),
        Customers=("Customer_ID", "nunique"),
        Quantity=("Quantity", "sum"),
    )
    .reset_index()
    .sort_values("Revenue", ascending=False)
)
st.dataframe(country_kpi, width="stretch")

# Revenues mensuels multi-pays interactifs
if len(st.session_state.selected_country) > 1:
    fig_multi_country = px.bar(
        filtered_df,
        x="InvoiceMonth",
        y="Revenue",
        color="Country",
        barmode="group",
        title="Chiffre d'affaires mensuel par pays",
        labels={"InvoiceMonth": "Mois", "Revenue": "Revenue ($)"}
    )
    st.plotly_chart(fig_multi_country, width="stretch")

# =========================================================
# VISUALISATIONS
# =========================================================
st.subheader("📈 Analyses visuelles")
st.plotly_chart(revenue_by_country(filtered_df), width="stretch")
st.plotly_chart(monthly_revenue(filtered_df), width="stretch")

# =========================================================
# RFM SEGMENTATION
# ==========================================================
st.subheader("🧠 Segmentation clients (RFM)")
try:
    rfm = compute_rfm(filtered_df)
    rfm["Recency"] = pd.to_numeric(rfm["Recency"], errors="coerce")
    rfm = rfm.dropna(subset=["Recency"])
    rfm["Recency"] = rfm["Recency"].astype(int)

    if not rfm.empty:
        rfm = rfm_scoring(rfm)
        segment_options = sorted(rfm["RFM_Score"].unique())
        selected_segments = st.sidebar.multiselect(
            "Segment RFM",
            options=segment_options,
            default=segment_options
        )
        rfm_filtered = rfm[rfm["RFM_Score"].isin(selected_segments)]

        if not rfm_filtered.empty:
            rfm_melt = rfm_filtered.melt(
                id_vars=["Customer_ID", "RFM_Score"],
                value_vars=["Recency", "Frequency", "Monetary"],
                var_name="Metric",
                value_name="Value"
            )
            fig_rfm = px.histogram(
                rfm_melt,
                x="Value",
                color="Metric",
                facet_col="Metric",
                nbins=30,
                title="Distribution Recency, Frequency, Monetary",
                marginal="box",
                hover_data=["Customer_ID"]
            )
            st.plotly_chart(fig_rfm, width="stretch")

            with st.expander("📋 Aperçu des clients segmentés"):
                st.dataframe(rfm_filtered.head(20))

except Exception as e:
    st.error(f"❌ Erreur RFM : {e}")

# =========================================================
# LTV + CHURN
# =========================================================
st.subheader("💎 Valeur client & churn")
reference_date = filtered_df["InvoiceDate"].max()
ltv = (
    filtered_df
    .groupby("Customer_ID")
    .agg(
        Total_Revenue=("Revenue", "sum"),
        Orders=("InvoiceNo", "nunique"),
        Last_Purchase=("InvoiceDate", "max"),
    )
    .reset_index()
)
ltv["LTV"] = ltv["Total_Revenue"] / ltv["Orders"]
ltv["Recency_days"] = (reference_date - ltv["Last_Purchase"]).dt.days
ltv["Churn"] = (ltv["Recency_days"] > 90).astype(int)

col_a, col_b = st.columns(2)
col_a.metric("💎 LTV moyen", f"${ltv['LTV'].mean():,.2f}")
col_b.metric("🔥 Taux de churn", f"{ltv['Churn'].mean() * 100:.1f}%")

# Heatmap LTV / Churn
ltv["LTV_bin"] = pd.qcut(ltv["LTV"], q=5, labels=False)
heatmap_data = ltv.groupby("LTV_bin").agg(
    Avg_LTV=("LTV", "mean"),
    Churn_rate=("Churn", "mean")
).reset_index()
fig_heatmap = px.imshow(
    heatmap_data[["Avg_LTV", "Churn_rate"]].T,
    labels=dict(x="LTV Bin", y="Metric", color="Value"),
    x=heatmap_data["LTV_bin"],
    y=["Avg LTV", "Churn rate"],
    color_continuous_scale="Viridis",
    title="Heatmap LTV et Churn par tranche"
)
st.plotly_chart(fig_heatmap, width="stretch")

with st.expander("📋 Clients à risque (churn)"):
    st.dataframe(
        ltv.sort_values("Recency_days", ascending=False).head(20)
    )
