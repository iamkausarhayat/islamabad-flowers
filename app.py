# app.py — Islamabad Flowers Management System
# Clean Read-Only | Green Floral Theme

import streamlit as st
import mysql.connector
import pandas as pd

# ── Page Config ───────────────────────────────────────────
st.set_page_config(
    page_title="Islamabad Flowers",
    page_icon="🌸",
    layout="wide"
)

# ── Custom CSS ────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #f0f7f0 0%, #e8f5e9 100%);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1b5e20 0%, #2e7d32 100%);
    }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div {
        color: white !important;
    }

    /* Metric cards — fix visibility */
    [data-testid="metric-container"] {
        background: white !important;
        border: 2px solid #66bb6a;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(46,125,50,0.15);
    }
    [data-testid="stMetricLabel"] {
        color: #2e7d32 !important;
        font-size: 1rem !important;
        font-weight: bold !important;
    }
    [data-testid="stMetricValue"] {
        color: #1b5e20 !important;
        font-size: 2.5rem !important;
        font-weight: bold !important;
    }

    /* Headings */
    h1, h2, h3 { color: #1b5e20 !important; }

    /* Banner */
    .banner {
        background: linear-gradient(90deg, #2e7d32, #66bb6a);
        color: white !important;
        padding: 18px 28px;
        border-radius: 12px;
        margin-bottom: 24px;
        font-size: 1.4rem;
        font-weight: bold;
    }

    /* Dataframe */
    [data-testid="stDataFrame"] {
        border: 2px solid #a5d6a7 !important;
        border-radius: 10px !important;
        overflow: hidden;
        background: white;
    }

    /* Divider */
    hr { border-color: #a5d6a7 !important; }

    /* Sidebar metrics */
    [data-testid="stSidebar"] [data-testid="stMetricValue"] {
        color: #c8e6c9 !important;
    }
    [data-testid="stSidebar"] [data-testid="stMetricLabel"] {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# ── Database Connection ───────────────────────────────────
def get_connection():
    return mysql.connector.connect(
        host     = st.secrets["host"],
        port     = st.secrets["port"],
        database = st.secrets["database"],
        user     = st.secrets["user"],
        password = st.secrets["password"],
        ssl_disabled = False
    )

def run_query(sql):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cols = [d[0] for d in cursor.description]
    cursor.close()
    conn.close()
    return pd.DataFrame(rows, columns=cols)

# ── Sidebar ───────────────────────────────────────────────
st.sidebar.markdown("## 🌸 Islamabad Flowers")
st.sidebar.markdown("---")
menu = st.sidebar.selectbox("📋 Navigate", [
    "🏠 Dashboard",
    "🌿 Suppliers",
    "🌺 Flowers",
    "🚚 Deliveries",
    "💐 Bouquets",
    "📊 Sales Reports"
])
st.sidebar.markdown("---")
st.sidebar.markdown("### 📌 Quick Stats")
st.sidebar.metric("🌿 Suppliers", run_query("SELECT COUNT(*) FROM SUPPLIER").iloc[0,0])
st.sidebar.metric("🌺 Flowers",   run_query("SELECT COUNT(*) FROM FLOWER").iloc[0,0])
st.sidebar.metric("💐 Bouquets",  run_query("SELECT COUNT(*) FROM BOUQUET").iloc[0,0])
st.sidebar.metric("🚚 Deliveries",run_query("SELECT COUNT(*) FROM DELIVERY").iloc[0,0])

# ══════════════════════════════════════════════════════════
# 🏠 DASHBOARD
# ══════════════════════════════════════════════════════════
if menu == "🏠 Dashboard":
    st.markdown('<div class="banner">🌸 Islamabad Flowers — Management Dashboard</div>',
                unsafe_allow_html=True)
    st.markdown("Welcome to **Islamabad Flowers** Management System.")
    st.markdown("---")

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🌿 Suppliers",  run_query("SELECT COUNT(*) FROM SUPPLIER").iloc[0,0])
    col2.metric("🌺 Flower Types",run_query("SELECT COUNT(*) FROM FLOWER").iloc[0,0])
    col3.metric("💐 Bouquets",   run_query("SELECT COUNT(*) FROM BOUQUET").iloc[0,0])
    col4.metric("🚚 Deliveries", run_query("SELECT COUNT(*) FROM DELIVERY").iloc[0,0])

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🌺 Top Flowers by Stock")
        df = run_query("""
            SELECT F.CommonName AS Flower,
                   SUM(DI.QuantityDelivered) AS Total_Stock
            FROM DELIVERY_ITEM DI
            JOIN FLOWER F ON DI.FlowerID = F.FlowerID
            GROUP BY F.CommonName
            ORDER BY Total_Stock DESC
        """)
        st.dataframe(df, use_container_width=True, hide_index=True)

    with col2:
        st.markdown("### 💐 Most Expensive Bouquets")
        df = run_query("""
            SELECT BouquetName AS Bouquet,
                   RetailPrice AS Price_Rs
            FROM BOUQUET
            ORDER BY RetailPrice DESC
        """)
        st.dataframe(df, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════
# 🌿 SUPPLIERS
# ══════════════════════════════════════════════════════════
elif menu == "🌿 Suppliers":
    st.markdown('<div class="banner">🌿 Supplier Information</div>',
                unsafe_allow_html=True)
    st.markdown("### 📋 All Registered Suppliers")
    df = run_query("SELECT * FROM SUPPLIER")
    st.dataframe(df, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════
# 🌺 FLOWERS
# ══════════════════════════════════════════════════════════
elif menu == "🌺 Flowers":
    st.markdown('<div class="banner">🌺 Flower Inventory</div>',
                unsafe_allow_html=True)
    st.markdown("### 📋 Current Flower Inventory")
    df = run_query("SELECT * FROM FLOWER")
    st.dataframe(df, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════
# 🚚 DELIVERIES
# ══════════════════════════════════════════════════════════
elif menu == "🚚 Deliveries":
    st.markdown('<div class="banner">🚚 Delivery Records</div>',
                unsafe_allow_html=True)
    st.markdown("### 📋 All Delivery Records")
    df = run_query("""
        SELECT
            DI.DeliveryItemID  AS Item_ID,
            S.SupplierName     AS Supplier,
            F.CommonName       AS Flower,
            D.DeliveryDate     AS Delivery_Date,
            DI.QuantityDelivered AS Quantity,
            DI.BulkPricePaid   AS Bulk_Price_Rs
        FROM DELIVERY_ITEM DI
        JOIN DELIVERY D ON DI.DeliveryID = D.DeliveryID
        JOIN SUPPLIER S ON D.SupplierID  = S.SupplierID
        JOIN FLOWER   F ON DI.FlowerID   = F.FlowerID
        ORDER BY D.DeliveryDate DESC
    """)
    st.dataframe(df, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════
# 💐 BOUQUETS
# ══════════════════════════════════════════════════════════
elif menu == "💐 Bouquets":
    st.markdown('<div class="banner">💐 Bouquet Designs & Recipes</div>',
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📋 All Bouquet Designs")
        df = run_query("SELECT * FROM BOUQUET ORDER BY RetailPrice DESC")
        st.dataframe(df, use_container_width=True, hide_index=True)

    with col2:
        st.markdown("### 📋 Bouquet Recipes")
        df = run_query("""
            SELECT
                B.BouquetName AS Bouquet,
                F.CommonName  AS Flower,
                BR.StemCount  AS Stems_Required
            FROM BOUQUET_RECIPE BR
            JOIN BOUQUET B ON BR.BouquetID = B.BouquetID
            JOIN FLOWER  F ON BR.FlowerID  = F.FlowerID
            ORDER BY B.BouquetName
        """)
        st.dataframe(df, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════
# 📊 SALES REPORTS
# ══════════════════════════════════════════════════════════
elif menu == "📊 Sales Reports":
    st.markdown('<div class="banner">📊 Sales Analysis Reports</div>',
                unsafe_allow_html=True)

    # Report 1
    st.markdown("### 📦 Report 1 — Total Stock & Cost Per Flower")
    df = run_query("""
        SELECT
            F.CommonName          AS Flower,
            SUM(DI.QuantityDelivered) AS Total_Stock,
            SUM(DI.BulkPricePaid)     AS Total_Cost_Rs
        FROM DELIVERY_ITEM DI
        JOIN FLOWER F ON DI.FlowerID = F.FlowerID
        GROUP BY F.CommonName
        ORDER BY Total_Stock DESC
    """)
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("---")

    col1, col2 = st.columns(2)

    # Report 2
    with col1:
        st.markdown("### 💐 Report 2 — Bouquets by Retail Price")
        df = run_query("""
            SELECT BouquetName AS Bouquet,
                   RetailPrice AS Price_Rs
            FROM BOUQUET
            ORDER BY RetailPrice DESC
        """)
        st.dataframe(df, use_container_width=True, hide_index=True)

    # Report 3
    with col2:
        st.markdown("### 🚚 Report 3 — Deliveries Per Supplier")
        df = run_query("""
            SELECT
                S.SupplierName        AS Supplier,
                COUNT(D.DeliveryID)   AS Total_Deliveries,
                SUM(DI.QuantityDelivered) AS Total_Flowers
            FROM DELIVERY D
            JOIN SUPPLIER S     ON D.SupplierID  = S.SupplierID
            JOIN DELIVERY_ITEM DI ON D.DeliveryID = DI.DeliveryID
            GROUP BY S.SupplierName
            ORDER BY Total_Deliveries DESC
        """)
        st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("---")

    # Report 4
    st.markdown("### 🌸 Report 4 — Most Used Flowers in Bouquets")
    df = run_query("""
        SELECT
            F.CommonName       AS Flower,
            COUNT(BR.RecipeID) AS Used_In_Bouquets,
            SUM(BR.StemCount)  AS Total_Stems
        FROM BOUQUET_RECIPE BR
        JOIN FLOWER F ON BR.FlowerID = F.FlowerID
        GROUP BY F.CommonName
        ORDER BY Total_Stems DESC
    """)
    st.dataframe(df, use_container_width=True, hide_index=True)