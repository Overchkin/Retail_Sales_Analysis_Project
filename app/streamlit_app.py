# ==========================================
# STREAMLIT APP – ONLINE RETAIL DASHBOARD (PRO – UX/UI)
# ==========================================

import sys
import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
from src.visualisation import revenue_by_country, monthly_revenue, rfm_distribution

# -----------------------------
# CONFIG APP
# -----------------------------
st.set_page_config(
    page_title="Online Retail Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# HEADER
# -----------------------------
st.markdown(
    """
    <h1 style='text-align: center; color: #2F4F4F;'>📊 Online Retail – Business Intelligence Dashboard</h1>
    <p style='text-align: center; font-size: 14px; color: gray;'>
    Explorez les ventes, segments clients et performances de manière interactive.
    </p>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# LOAD DATA
# -----------------------------
PROCESSED_CSV_PATH = os.path.join(PROJECT_ROOT, "data", "processed", "online_retail_clean.csv")

@st.cache_data
def load_and_prepare_data(csv_path):
    df = pd.read_csv(csv_path, parse_dates=["InvoiceDate"])
    df = add_time_features(df)
    return df

df = load_and_prepare_data(PROCESSED_CSV_PATH)

# =========================================================
# SIDEBAR FILTERS
# =========================================================
st.sidebar.header("🎛️ Filtres interactifs")

# --- Session state ---
if "selected_country" not in st.session_state:
    st.session_state.selected_country = []
if "selected_year" not in st.session_state:
    st.session_state.selected_year = []
if "applied_filters" not in st.session_state:
    st.session_state.applied_filters = False

with st.sidebar.form("filter_form"):
    country_options = sorted(df["Country"].dropna().unique())
    year_options = sorted(df["InvoiceYear"].dropna().unique())

    selected_country = st.multiselect("Pays", country_options, default=st.session_state.selected_country)
    selected_year = st.multiselect("Année", year_options, default=st.session_state.selected_year)

    col_apply, col_reset = st.columns(2)
    apply_filters = col_apply.form_submit_button("✅ Appliquer")
    reset_filters = col_reset.form_submit_button("🔄 Réinitialiser")

# -----------------------------
# RESET / APPLY
# -----------------------------
if reset_filters:
    st.session_state.selected_country = []
    st.session_state.selected_year = []
    st.session_state.applied_filters = False
    st.info("Filtres réinitialisés. Sélectionnez de nouveaux filtres et cliquez sur ✅ Appliquer.")

if apply_filters:
    if not selected_country or not selected_year:
        st.warning("⚠️ Sélectionnez au moins un pays et une année.")
    else:
        st.session_state.selected_country = selected_country
        st.session_state.selected_year = selected_year
        st.session_state.applied_filters = True

if not st.session_state.applied_filters:
    st.info("Sélectionnez des filtres puis cliquez sur ✅ Appliquer pour afficher les données.")
    st.stop()

# -----------------------------
# FILTER DATA
# -----------------------------
filtered_df = df[
    df["Country"].isin(st.session_state.selected_country) &
    df["InvoiceYear"].isin(st.session_state.selected_year)
]

if filtered_df.empty:
    st.warning("⚠️ Aucun client ou vente disponible pour ces filtres.")
    st.stop()

st.caption(f"📍 Filtres appliqués : {len(st.session_state.selected_country)} pays · {len(st.session_state.selected_year)} années")

# =========================================================
# KPI METRICS (CARDS STYLE)
# =========================================================
st.subheader("📌 KPIs principaux")

kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

def styled_metric(label, value, delta=None):
    """Affiche un KPI stylisé avec option delta"""
    if delta:
        kpi_col1.metric(label, f"${value:,.0f}", f"{delta:+,.0f}")
    else:
        kpi_col1.metric(label, f"${value:,.0f}")

total_revenue = filtered_df['Revenue'].sum()
total_orders = filtered_df["InvoiceNo"].nunique()
total_customers = filtered_df["Customer_ID"].nunique()
total_items = int(filtered_df["Quantity"].sum())

kpi_col1.metric("💰 CA Total", f"${total_revenue:,.0f}")
kpi_col2.metric("🧾 Commandes", total_orders)
kpi_col3.metric("👥 Clients uniques", total_customers)
kpi_col4.metric("📦 Articles vendus", total_items)

# =========================================================
# VISUALISATIONS INTERACTIVES
# =========================================================
st.subheader("🌍 Analyse multi-pays")
fig_country = px.bar(
    filtered_df.groupby("Country", as_index=False)["Revenue"].sum(),
    x="Country", y="Revenue",
    color="Revenue",
    color_continuous_scale="Viridis",
    title="CA par pays"
)
st.plotly_chart(fig_country, use_container_width=True)

st.subheader("📈 Évolution mensuelle du CA")
fig_month = monthly_revenue(filtered_df)
st.plotly_chart(fig_month, use_container_width=True)

# =========================================================
# RFM SEGMENTATION (EXPANDERS)
# =========================================================
st.subheader("🧠 Segmentation clients (RFM)")
try:
    rfm = compute_rfm(filtered_df)
    rfm["Recency"] = pd.to_numeric(rfm["Recency"], errors="coerce")
    rfm = rfm.dropna(subset=["Recency"])
    rfm["Recency"] = rfm["Recency"].astype(int)

    if not rfm.empty:
        rfm = rfm_scoring(rfm)
        segment_options = sorted(rfm["RFM_Score"].unique())
        selected_segments = st.sidebar.multiselect("Segment RFM", segment_options, default=segment_options)
        rfm_filtered = rfm[rfm["RFM_Score"].isin(selected_segments)]

        if not rfm_filtered.empty:
            with st.expander("📊 Distribution RFM"):
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
                    hover_data=["Customer_ID"],
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                st.plotly_chart(fig_rfm, use_container_width=True)

            with st.expander("📋 Aperçu clients segmentés"):
                st.dataframe(rfm_filtered.head(20))

except Exception as e:
    st.error(f"❌ Erreur RFM : {e}")

# =========================================================
# LTV & CHURN (PRO)
# =========================================================
st.subheader("💎 Valeur client & churn")
reference_date = filtered_df["InvoiceDate"].max()
ltv = (
    filtered_df.groupby("Customer_ID")
    .agg(
        Total_Revenue=("Revenue", "sum"),
        Orders=("InvoiceNo", "nunique"),
        Last_Purchase=("InvoiceDate", "max")
    )
    .reset_index()
)
ltv["LTV"] = ltv["Total_Revenue"] / ltv["Orders"]
ltv["Recency_days"] = (reference_date - ltv["Last_Purchase"]).dt.days
ltv["Churn"] = (ltv["Recency_days"] > 90).astype(int)

col_ltv, col_churn = st.columns(2)
col_ltv.metric("💎 LTV moyen", f"${ltv['LTV'].mean():,.2f}")
col_churn.metric("🔥 Taux de churn", f"{ltv['Churn'].mean() * 100:.1f}%")

with st.expander("📊 Heatmap LTV / Churn"):
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
    st.plotly_chart(fig_heatmap, use_container_width=True)

with st.expander("📋 Clients à risque (churn)"):
    st.dataframe(ltv.sort_values("Recency_days", ascending=False).head(20), use_container_width=True)
