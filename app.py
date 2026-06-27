# app.py — Islamabad Flowers Main App

import streamlit as st
import mysql.connector
import streamlit as st

def get_connection():
    connection = mysql.connector.connect(
        host     = st.secrets["host"],
        port     = st.secrets["port"],
        database = st.secrets["database"],
        user     = st.secrets["user"],
        password = st.secrets["password"],
        ssl_disabled = False
    )
    return connection
# ── Page Config ──────────────────────────
st.set_page_config(
    page_title="Islamabad Flowers",
    page_icon="🌸",
    layout="wide"
)

st.title("🌸 Islamabad Flowers Management System")
st.markdown("---")

# ── Sidebar Navigation ────────────────────
menu = st.sidebar.selectbox("📋 Select Section", [
    "🏠 Home",
    "🌿 Suppliers",
    "🌺 Flowers",
    "🚚 Deliveries",
    "💐 Bouquets",
    "📊 Sales Report"
])

# ── Connect to Database ───────────────────
conn = get_connection()
cursor = conn.cursor()

# ══════════════════════════════════════════
# HOME PAGE
# ══════════════════════════════════════════
if menu == "🏠 Home":
    st.subheader("Welcome to Islamabad Flowers 🌸")
    st.write("Use the sidebar to navigate between sections.")

    col1, col2, col3 = st.columns(3)

    cursor.execute("SELECT COUNT(*) FROM SUPPLIER")
    col1.metric("Total Suppliers", cursor.fetchone()[0])

    cursor.execute("SELECT COUNT(*) FROM FLOWER")
    col2.metric("Total Flowers", cursor.fetchone()[0])

    cursor.execute("SELECT COUNT(*) FROM BOUQUET")
    col3.metric("Total Bouquets", cursor.fetchone()[0])

# ══════════════════════════════════════════
# SUPPLIERS PAGE
# ══════════════════════════════════════════
elif menu == "🌿 Suppliers":
    st.subheader("🌿 All Suppliers")

    cursor.execute("SELECT * FROM SUPPLIER")
    rows = cursor.fetchall()

    st.table({
        "Supplier ID"    : [r[0] for r in rows],
        "Supplier Name"  : [r[1] for r in rows],
        "Contact Number" : [r[2] for r in rows]
    })

# ══════════════════════════════════════════
# FLOWERS PAGE
# ══════════════════════════════════════════
elif menu == "🌺 Flowers":
    st.subheader("🌺 Flower Inventory")

    cursor.execute("SELECT * FROM FLOWER")
    rows = cursor.fetchall()

    st.table({
        "Flower ID"    : [r[0] for r in rows],
        "Common Name"  : [r[1] for r in rows],
        "Cost Per Stem": [r[2] for r in rows]
    })

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

    st.table({
        "Item ID"          : [r[0] for r in rows],
        "Supplier"         : [r[1] for r in rows],
        "Flower"           : [r[2] for r in rows],
        "Delivery Date"    : [r[3] for r in rows],
        "Qty Delivered"    : [r[4] for r in rows],
        "Bulk Price Paid"  : [r[5] for r in rows]
    })

# ══════════════════════════════════════════
# BOUQUETS PAGE
# ══════════════════════════════════════════
elif menu == "💐 Bouquets":
    st.subheader("💐 Bouquet Designs & Recipes")

    # Show all bouquets
    cursor.execute("SELECT * FROM BOUQUET")
    bouquets = cursor.fetchall()

    st.write("### All Bouquets")
    st.table({
        "Bouquet ID"  : [r[0] for r in bouquets],
        "Bouquet Name": [r[1] for r in bouquets],
        "Retail Price": [r[2] for r in bouquets]
    })

    # Show bouquet recipes
    st.write("### Bouquet Recipes")
    cursor.execute("""
        SELECT 
            B.BouquetName,
            F.CommonName,
            BR.StemCount
        FROM BOUQUET_RECIPE BR
        JOIN BOUQUET B ON BR.BouquetID = B.BouquetID
        JOIN FLOWER  F ON BR.FlowerID  = F.FlowerID
    """)
    rows = cursor.fetchall()

    st.table({
        "Bouquet Name": [r[0] for r in rows],
        "Flower"      : [r[1] for r in rows],
        "Stem Count"  : [r[2] for r in rows]
    })

# ══════════════════════════════════════════
# SALES REPORT PAGE
# ══════════════════════════════════════════
elif menu == "📊 Sales Report":
    st.subheader("📊 Sales Analysis Report")

    # Report 1 — Total stock delivered per flower
    st.write("### 🌺 Total Stock Delivered Per Flower")
    cursor.execute("""
        SELECT 
            F.CommonName,
            SUM(DI.QuantityDelivered) AS TotalStock,
            SUM(DI.BulkPricePaid)     AS TotalCost
        FROM DELIVERY_ITEM DI
        JOIN FLOWER F ON DI.FlowerID = F.FlowerID
        GROUP BY F.CommonName
    """)
    rows = cursor.fetchall()
    st.table({
        "Flower"      : [r[0] for r in rows],
        "Total Stock" : [r[1] for r in rows],
        "Total Cost"  : [r[2] for r in rows]
    })

    # Report 2 — Most expensive bouquets
    st.write("### 💐 Bouquets by Retail Price")
    cursor.execute("""
        SELECT BouquetName, RetailPrice
        FROM BOUQUET
        ORDER BY RetailPrice DESC
    """)
    rows = cursor.fetchall()
    st.table({
        "Bouquet Name" : [r[0] for r in rows],
        "Retail Price" : [r[1] for r in rows]
    })

    # Report 3 — Supplier delivery count
    st.write("### 🚚 Deliveries Per Supplier")
    cursor.execute("""
        SELECT 
            S.SupplierName,
            COUNT(D.DeliveryID) AS TotalDeliveries
        FROM DELIVERY D
        JOIN SUPPLIER S ON D.SupplierID = S.SupplierID
        GROUP BY S.SupplierName
    """)
    rows = cursor.fetchall()
    st.table({
        "Supplier"          : [r[0] for r in rows],
        "Total Deliveries"  : [r[1] for r in rows]
    })

# ── Close Connection ──────────────────────
cursor.close()
conn.close()