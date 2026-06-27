# app.py — Islamabad Flowers Management System
# Green/Floral Theme + Full CRUD

import streamlit as st
import mysql.connector
from datetime import date

# ── Page Config ──────────────────────────────────────────
st.set_page_config(
    page_title="Islamabad Flowers",
    page_icon="🌸",
    layout="wide"
)

# ── Custom CSS — Green Floral Theme ──────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #f0f7f0 0%, #e8f5e9 100%);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1b5e20 0%, #2e7d32 50%, #388e3c 100%);
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    [data-testid="stSidebar"] .stSelectbox label {
        color: #c8e6c9 !important;
        font-weight: bold;
    }

    /* Metric cards */
    [data-testid="metric-container"] {
        background: white;
        border: 2px solid #a5d6a7;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 4px 12px rgba(46,125,50,0.15);
    }
    [data-testid="metric-container"] label {
        color: #2e7d32 !important;
        font-weight: bold !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #1b5e20 !important;
        font-size: 2rem !important;
        font-weight: bold !important;
    }

    /* Headers */
    h1 { color: #1b5e20 !important; }
    h2 { color: #2e7d32 !important; }
    h3 { color: #388e3c !important; }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #2e7d32, #43a047);
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 8px 24px;
        font-weight: bold;
        transition: all 0.3s;
        width: 100%;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #1b5e20, #2e7d32);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(46,125,50,0.4);
    }

    /* Input fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stDateInput > div > div > input,
    .stSelectbox > div > div {
        border: 2px solid #a5d6a7 !important;
        border-radius: 8px !important;
        background: white !important;
    }

    /* Tables */
    .stDataFrame {
        border: 2px solid #a5d6a7;
        border-radius: 8px;
        overflow: hidden;
    }

    /* Success/Error messages */
    .stSuccess {
        background: #e8f5e9 !important;
        border-left: 4px solid #2e7d32 !important;
        border-radius: 8px !important;
    }
    .stError {
        border-radius: 8px !important;
    }

    /* Divider */
    hr {
        border-color: #a5d6a7;
    }

    /* Form container */
    .form-card {
        background: white;
        padding: 24px;
        border-radius: 12px;
        border: 2px solid #c8e6c9;
        box-shadow: 0 4px 12px rgba(46,125,50,0.1);
        margin-bottom: 20px;
    }

    /* Section banner */
    .banner {
        background: linear-gradient(90deg, #2e7d32, #66bb6a);
        color: white;
        padding: 16px 24px;
        border-radius: 12px;
        margin-bottom: 20px;
        font-size: 1.3rem;
        font-weight: bold;
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

# ── Helper: run SELECT query ──────────────────────────────
def run_query(sql, params=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, params or ())
    rows = cursor.fetchall()
    cols = [d[0] for d in cursor.description]
    cursor.close()
    conn.close()
    return rows, cols

# ── Helper: run INSERT query ──────────────────────────────
def run_insert(sql, params):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    conn.commit()
    cursor.close()
    conn.close()

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
st.sidebar.markdown("### 📌 Quick Info")
rows, _ = run_query("SELECT COUNT(*) FROM SUPPLIER")
st.sidebar.metric("Suppliers", rows[0][0])
rows, _ = run_query("SELECT COUNT(*) FROM FLOWER")
st.sidebar.metric("Flowers", rows[0][0])
rows, _ = run_query("SELECT COUNT(*) FROM BOUQUET")
st.sidebar.metric("Bouquets", rows[0][0])

# ══════════════════════════════════════════════════════════
# 🏠 DASHBOARD
# ══════════════════════════════════════════════════════════
if menu == "🏠 Dashboard":
    st.markdown('<div class="banner">🌸 Islamabad Flowers — Management Dashboard</div>', unsafe_allow_html=True)
    st.markdown("Welcome! Use the sidebar to manage your flower shop.")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    rows, _ = run_query("SELECT COUNT(*) FROM SUPPLIER")
    col1.metric("🌿 Suppliers", rows[0][0])
    rows, _ = run_query("SELECT COUNT(*) FROM FLOWER")
    col2.metric("🌺 Flower Types", rows[0][0])
    rows, _ = run_query("SELECT COUNT(*) FROM BOUQUET")
    col3.metric("💐 Bouquets", rows[0][0])
    rows, _ = run_query("SELECT COUNT(*) FROM DELIVERY")
    col4.metric("🚚 Deliveries", rows[0][0])

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🌺 Top Flowers by Stock")
        rows, cols = run_query("""
            SELECT F.CommonName, SUM(DI.QuantityDelivered) AS TotalStock
            FROM DELIVERY_ITEM DI JOIN FLOWER F ON DI.FlowerID = F.FlowerID
            GROUP BY F.CommonName ORDER BY TotalStock DESC LIMIT 5
        """)
        if rows:
            import pandas as pd
            df = pd.DataFrame(rows, columns=cols)
            st.dataframe(df, use_container_width=True, hide_index=True)

    with col2:
        st.markdown("### 💐 Most Expensive Bouquets")
        rows, cols = run_query("""
            SELECT BouquetName, RetailPrice
            FROM BOUQUET ORDER BY RetailPrice DESC LIMIT 5
        """)
        if rows:
            import pandas as pd
            df = pd.DataFrame(rows, columns=cols)
            st.dataframe(df, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════
# 🌿 SUPPLIERS
# ══════════════════════════════════════════════════════════
elif menu == "🌿 Suppliers":
    st.markdown('<div class="banner">🌿 Supplier Management</div>', unsafe_allow_html=True)

    # View
    st.markdown("### 📋 All Suppliers")
    rows, cols = run_query("SELECT * FROM SUPPLIER")
    import pandas as pd
    st.dataframe(pd.DataFrame(rows, columns=cols), use_container_width=True, hide_index=True)

    st.markdown("---")

    # Add New
    st.markdown("### ➕ Add New Supplier")
    with st.form("add_supplier"):
        col1, col2, col3 = st.columns(3)
        sid  = col1.text_input("Supplier ID (e.g. S05)")
        name = col2.text_input("Supplier Name")
        contact = col3.text_input("Contact Number")
        submitted = st.form_submit_button("✅ Add Supplier")
        if submitted:
            if sid and name and contact:
                try:
                    run_insert("INSERT INTO SUPPLIER VALUES (%s, %s, %s)", (sid, name, contact))
                    st.success(f"✅ Supplier '{name}' added successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")
            else:
                st.warning("⚠️ Please fill all fields!")

# ══════════════════════════════════════════════════════════
# 🌺 FLOWERS
# ══════════════════════════════════════════════════════════
elif menu == "🌺 Flowers":
    st.markdown('<div class="banner">🌺 Flower Inventory</div>', unsafe_allow_html=True)

    # View
    st.markdown("### 📋 Current Inventory")
    rows, cols = run_query("SELECT * FROM FLOWER")
    import pandas as pd
    st.dataframe(pd.DataFrame(rows, columns=cols), use_container_width=True, hide_index=True)

    st.markdown("---")

    # Add New
    st.markdown("### ➕ Add New Flower")
    with st.form("add_flower"):
        col1, col2, col3 = st.columns(3)
        fid  = col1.text_input("Flower ID (e.g. F06)")
        name = col2.text_input("Common Name")
        cost = col3.number_input("Cost Per Stem (Rs)", min_value=0.0, step=0.5)
        submitted = st.form_submit_button("✅ Add Flower")
        if submitted:
            if fid and name and cost:
                try:
                    run_insert("INSERT INTO FLOWER VALUES (%s, %s, %s)", (fid, name, cost))
                    st.success(f"✅ Flower '{name}' added successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")
            else:
                st.warning("⚠️ Please fill all fields!")

# ══════════════════════════════════════════════════════════
# 🚚 DELIVERIES
# ══════════════════════════════════════════════════════════
elif menu == "🚚 Deliveries":
    st.markdown('<div class="banner">🚚 Delivery Management</div>', unsafe_allow_html=True)

    # View
    st.markdown("### 📋 All Delivery Records")
    rows, cols = run_query("""
        SELECT DI.DeliveryItemID, S.SupplierName, F.CommonName,
               D.DeliveryDate, DI.QuantityDelivered, DI.BulkPricePaid
        FROM DELIVERY_ITEM DI
        JOIN DELIVERY D ON DI.DeliveryID = D.DeliveryID
        JOIN SUPPLIER S ON D.SupplierID  = S.SupplierID
        JOIN FLOWER   F ON DI.FlowerID   = F.FlowerID
    """)
    import pandas as pd
    st.dataframe(pd.DataFrame(rows, columns=cols), use_container_width=True, hide_index=True)

    st.markdown("---")

    # Add New Delivery
    st.markdown("### ➕ Record New Delivery")

    # Get suppliers and flowers for dropdowns
    sup_rows, _ = run_query("SELECT SupplierID, SupplierName FROM SUPPLIER")
    flo_rows, _ = run_query("SELECT FlowerID, CommonName FROM FLOWER")
    del_rows, _ = run_query("SELECT DeliveryID FROM DELIVERY ORDER BY DeliveryID DESC LIMIT 1")
    di_rows,  _ = run_query("SELECT DeliveryItemID FROM DELIVERY_ITEM ORDER BY DeliveryItemID DESC LIMIT 1")

    sup_options = {f"{r[0]} — {r[1]}": r[0] for r in sup_rows}
    flo_options = {f"{r[0]} — {r[1]}": r[0] for r in flo_rows}

    with st.form("add_delivery"):
        col1, col2 = st.columns(2)
        did      = col1.text_input("Delivery ID (e.g. D05)")
        sel_sup  = col2.selectbox("Select Supplier", list(sup_options.keys()))
        col3, col4 = st.columns(2)
        del_date = col3.date_input("Delivery Date", value=date.today())
        di_id    = col4.text_input("Delivery Item ID (e.g. DI06)")
        col5, col6, col7 = st.columns(3)
        sel_flo  = col5.selectbox("Select Flower", list(flo_options.keys()))
        qty      = col6.number_input("Quantity Delivered", min_value=1, step=1)
        price    = col7.number_input("Bulk Price Paid (Rs)", min_value=0.0, step=0.5)
        submitted = st.form_submit_button("✅ Record Delivery")
        if submitted:
            if did and di_id:
                try:
                    run_insert("INSERT INTO DELIVERY VALUES (%s, %s, %s)",
                               (did, sup_options[sel_sup], del_date))
                    run_insert("INSERT INTO DELIVERY_ITEM VALUES (%s, %s, %s, %s, %s)",
                               (di_id, did, flo_options[sel_flo], qty, price))
                    st.success("✅ Delivery recorded successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")
            else:
                st.warning("⚠️ Please fill all fields!")

# ══════════════════════════════════════════════════════════
# 💐 BOUQUETS
# ══════════════════════════════════════════════════════════
elif menu == "💐 Bouquets":
    st.markdown('<div class="banner">💐 Bouquet Designs & Recipes</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📋 All Bouquets")
        rows, cols = run_query("SELECT * FROM BOUQUET")
        import pandas as pd
        st.dataframe(pd.DataFrame(rows, columns=cols), use_container_width=True, hide_index=True)

    with col2:
        st.markdown("### 📋 Bouquet Recipes")
        rows, cols = run_query("""
            SELECT B.BouquetName, F.CommonName, BR.StemCount
            FROM BOUQUET_RECIPE BR
            JOIN BOUQUET B ON BR.BouquetID = B.BouquetID
            JOIN FLOWER  F ON BR.FlowerID  = F.FlowerID
        """)
        st.dataframe(pd.DataFrame(rows, columns=cols), use_container_width=True, hide_index=True)

    st.markdown("---")

    # Add New Bouquet
    st.markdown("### ➕ Add New Bouquet")
    with st.form("add_bouquet"):
        col1, col2, col3 = st.columns(3)
        bid   = col1.text_input("Bouquet ID (e.g. B05)")
        bname = col2.text_input("Bouquet Name")
        price = col3.number_input("Retail Price (Rs)", min_value=0.0, step=50.0)
        submitted = st.form_submit_button("✅ Add Bouquet")
        if submitted:
            if bid and bname and price:
                try:
                    run_insert("INSERT INTO BOUQUET VALUES (%s, %s, %s)", (bid, bname, price))
                    st.success(f"✅ Bouquet '{bname}' added successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")
            else:
                st.warning("⚠️ Please fill all fields!")

    st.markdown("---")

    # Add Recipe
    st.markdown("### ➕ Add Bouquet Recipe")
    bou_rows, _ = run_query("SELECT BouquetID, BouquetName FROM BOUQUET")
    flo_rows, _ = run_query("SELECT FlowerID, CommonName FROM FLOWER")
    bou_options = {f"{r[0]} — {r[1]}": r[0] for r in bou_rows}
    flo_options = {f"{r[0]} — {r[1]}": r[0] for r in flo_rows}

    with st.form("add_recipe"):
        col1, col2, col3, col4 = st.columns(4)
        rid      = col1.text_input("Recipe ID (e.g. R06)")
        sel_bou  = col2.selectbox("Select Bouquet", list(bou_options.keys()))
        sel_flo  = col3.selectbox("Select Flower", list(flo_options.keys()))
        stems    = col4.number_input("Stem Count", min_value=1, step=1)
        submitted = st.form_submit_button("✅ Add Recipe")
        if submitted:
            if rid:
                try:
                    run_insert("INSERT INTO BOUQUET_RECIPE VALUES (%s, %s, %s, %s)",
                               (rid, bou_options[sel_bou], flo_options[sel_flo], stems))
                    st.success("✅ Recipe added successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")
            else:
                st.warning("⚠️ Please fill Recipe ID!")

# ══════════════════════════════════════════════════════════
# 📊 SALES REPORTS
# ══════════════════════════════════════════════════════════
elif menu == "📊 Sales Reports":
    st.markdown('<div class="banner">📊 Sales Analysis Reports</div>', unsafe_allow_html=True)

    import pandas as pd

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🌺 Total Stock Per Flower")
        rows, cols = run_query("""
            SELECT F.CommonName AS Flower,
                   SUM(DI.QuantityDelivered) AS TotalStock,
                   SUM(DI.BulkPricePaid) AS TotalCost
            FROM DELIVERY_ITEM DI
            JOIN FLOWER F ON DI.FlowerID = F.FlowerID
            GROUP BY F.CommonName
            ORDER BY TotalStock DESC
        """)
        st.dataframe(pd.DataFrame(rows, columns=cols), use_container_width=True, hide_index=True)

    with col2:
        st.markdown("### 💐 Bouquets by Price")
        rows, cols = run_query("""
            SELECT BouquetName AS Bouquet, RetailPrice AS Price
            FROM BOUQUET ORDER BY RetailPrice DESC
        """)
        st.dataframe(pd.DataFrame(rows, columns=cols), use_container_width=True, hide_index=True)

    st.markdown("---")

    st.markdown("### 🚚 Deliveries Per Supplier")
    rows, cols = run_query("""
        SELECT S.SupplierName AS Supplier,
               COUNT(D.DeliveryID) AS TotalDeliveries,
               SUM(DI.QuantityDelivered) AS TotalFlowersReceived
        FROM DELIVERY D
        JOIN SUPPLIER S ON D.SupplierID = S.SupplierID
        JOIN DELIVERY_ITEM DI ON D.DeliveryID = DI.DeliveryID
        GROUP BY S.SupplierName
        ORDER BY TotalDeliveries DESC
    """)
    st.dataframe(pd.DataFrame(rows, columns=cols), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("### 🌸 Most Used Flowers in Bouquets")
    rows, cols = run_query("""
        SELECT F.CommonName AS Flower,
               COUNT(BR.RecipeID) AS UsedInBouquets,
               SUM(BR.StemCount) AS TotalStems
        FROM BOUQUET_RECIPE BR
        JOIN FLOWER F ON BR.FlowerID = F.FlowerID
        GROUP BY F.CommonName
        ORDER BY TotalStems DESC
    """)
    st.dataframe(pd.DataFrame(rows, columns=cols), use_container_width=True, hide_index=True)