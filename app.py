# app.py — Islamabad Flowers Main App

import streamlit as st
import mysql.connector
import pandas as pd

# ── Page Config ──────────────────────────
st.set_page_config(
    page_title="Islamabad Flowers",
    page_icon="🌸",
    layout="wide"
)

# ── Green Theme CSS ───────────────────────
st.markdown("""
<style>
    .stApp { background-color: #f0f7f0 !important; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #1b5e20, #2e7d32) !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    h1, h2, h3 { color: #1b5e20 !important; }
    [data-testid="stMetricLabel"] { color: #2e7d32 !important; font-weight: bold !important; }
    [data-testid="stMetricValue"] { color: #1b5e20 !important; font-weight: bold !important; }
    [data-testid="metric-container"] { background: white !important; border: 2px solid #66bb6a !important; border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

# ── Database Connection ───────────────────
def get_connection():
    return mysql.connector.connect(
        host     = st.secrets["host"],
        port     = st.secrets["port"],
        database = st.secrets["database"],
        user     = st.secrets["user"],
        password = st.secrets["password"],
        ssl_disabled = False
    )

conn   = get_connection()
cursor = conn.cursor()

# ── Sidebar Navigation ────────────────────
st.sidebar.title("🌸 Islamabad Flowers")
menu = st.sidebar.selectbox("📋 Select Section", [
    "🏠 Home",
    "🌿 Suppliers",
    "🌺 Flowers",
    "🚚 Deliveries",
    "💐 Bouquets",
    "📊 Sales Report"
])

st.title("🌸 Islamabad Flowers Management System")
st.markdown("---")

# ══════════════════════════════════════════
# HOME PAGE
# ══════════════════════════════════════════
if menu == "🏠 Home":
    st.subheader("Welcome to Islamabad Flowers 🌸")
    st.write("Use the sidebar to navigate between sections.")

    col1, col2, col3 = st.columns(3)

    cursor.execute("SELECT COUNT(*) FROM SUPPLIER")
    col1.metric("🌿 Total Suppliers", cursor.fetchone()[0])

    cursor.execute("SELECT COUNT(*) FROM FLOWER")
    col2.metric("🌺 Total Flowers", cursor.fetchone()[0])

    cursor.execute("SELECT COUNT(*) FROM BOUQUET")
    col3.metric("💐 Total Bouquets", cursor.fetchone()[0])

# ══════════════════════════════════════════
# SUPPLIERS PAGE
# ══════════════════════════════════════════
elif menu == "🌿 Suppliers":
    st.subheader("🌿 All Suppliers")
    cursor.execute("SELECT * FROM SUPPLIER")
    rows = cursor.fetchall()
    st.dataframe(
        pd.DataFrame(rows, columns=["Supplier ID", "Supplier Name", "Contact Number"]),
        use_container_width=True, hide_index=True
    )

# ══════════════════════════════════════════
# FLOWERS PAGE
# ══════════════════════════════════════════
elif menu == "🌺 Flowers":
    st.subheader("🌺 Flower Inventory")
    cursor.execute("SELECT * FROM FLOWER")
    rows = cursor.fetchall()
    st.dataframe(
        pd.DataFrame(rows, columns=["Flower ID", "Common Name", "Cost Per Stem"]),
        use_container_width=True, hide_index=True
    )

# ══════════════════════════════════════════
# DELIVERIES PAGE
# ══════════════════════════════════════════
elif menu == "🚚 Deliveries":
    st.subheader("🚚 Delivery Records")
    cursor.execute("""
        SELECT
            DI.DeliveryItemID,
            S.SupplierName,
            F.CommonName,
            D.DeliveryDate,
            DI.QuantityDelivered,
            DI.BulkPricePaid
        FROM DELIVERY_ITEM DI
        JOIN DELIVERY D ON DI.DeliveryID = D.DeliveryID
        JOIN SUPPLIER S ON D.SupplierID  = S.SupplierID
        JOIN FLOWER   F ON DI.FlowerID   = F.FlowerID
    """)
    rows = cursor.fetchall()
    st.dataframe(
        pd.DataFrame(rows, columns=["Item ID", "Supplier", "Flower", "Delivery Date", "Qty Delivered", "Bulk Price Paid"]),
        use_container_width=True, hide_index=True
    )

# ══════════════════════════════════════════
# BOUQUETS PAGE
# ══════════════════════════════════════════
elif menu == "💐 Bouquets":
    st.subheader("💐 Bouquet Designs & Recipes")

    st.write("### All Bouquets")
    cursor.execute("SELECT * FROM BOUQUET")
    rows = cursor.fetchall()
    st.dataframe(
        pd.DataFrame(rows, columns=["Bouquet ID", "Bouquet Name", "Retail Price"]),
        use_container_width=True, hide_index=True
    )

    st.write("### Bouquet Recipes")
    cursor.execute("""
        SELECT B.BouquetName, F.CommonName, BR.StemCount
        FROM BOUQUET_RECIPE BR
        JOIN BOUQUET B ON BR.BouquetID = B.BouquetID
        JOIN FLOWER  F ON BR.FlowerID  = F.FlowerID
    """)
    rows = cursor.fetchall()
    st.dataframe(
        pd.DataFrame(rows, columns=["Bouquet Name", "Flower", "Stem Count"]),
        use_container_width=True, hide_index=True
    )

# ══════════════════════════════════════════
# SALES REPORT PAGE
# ══════════════════════════════════════════
elif menu == "📊 Sales Report":
    st.subheader("📊 Sales Analysis Report")

    st.write("### 🌺 Total Stock Delivered Per Flower")
    cursor.execute("""
        SELECT F.CommonName,
               SUM(DI.QuantityDelivered) AS TotalStock,
               SUM(DI.BulkPricePaid)     AS TotalCost
        FROM DELIVERY_ITEM DI
        JOIN FLOWER F ON DI.FlowerID = F.FlowerID
        GROUP BY F.CommonName
    """)
    rows = cursor.fetchall()
    st.dataframe(
        pd.DataFrame(rows, columns=["Flower", "Total Stock", "Total Cost"]),
        use_container_width=True, hide_index=True
    )

    st.write("### 💐 Bouquets by Retail Price")
    cursor.execute("SELECT BouquetName, RetailPrice FROM BOUQUET ORDER BY RetailPrice DESC")
    rows = cursor.fetchall()
    st.dataframe(
        pd.DataFrame(rows, columns=["Bouquet Name", "Retail Price"]),
        use_container_width=True, hide_index=True
    )

    st.write("### 🚚 Deliveries Per Supplier")
    cursor.execute("""
        SELECT S.SupplierName, COUNT(D.DeliveryID) AS TotalDeliveries
        FROM DELIVERY D
        JOIN SUPPLIER S ON D.SupplierID = S.SupplierID
        GROUP BY S.SupplierName
    """)
    rows = cursor.fetchall()
    st.dataframe(
        pd.DataFrame(rows, columns=["Supplier", "Total Deliveries"]),
        use_container_width=True, hide_index=True
    )

    st.write("### 🌸 Most Used Flowers in Bouquets")
    cursor.execute("""
        SELECT F.CommonName, COUNT(BR.RecipeID) AS UsedInBouquets, SUM(BR.StemCount) AS TotalStems
        FROM BOUQUET_RECIPE BR
        JOIN FLOWER F ON BR.FlowerID = F.FlowerID
        GROUP BY F.CommonName
        ORDER BY TotalStems DESC
    """)
    rows = cursor.fetchall()
    st.dataframe(
        pd.DataFrame(rows, columns=["Flower", "Used In Bouquets", "Total Stems"]),
        use_container_width=True, hide_index=True
    )

# ── Close Connection ──────────────────────
cursor.close()
conn.close()