import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from io import BytesIO

# ------------------------------------
# Page Config
# ------------------------------------

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

# ------------------------------------
# ADMIN LOGIN
# ------------------------------------

ADMIN_PASSWORD = "Aditya@78"      # Change this password

st.title("🔐 Admin Dashboard")

password = st.text_input(
    "Enter Admin Password",
    type="password"
)

if password != ADMIN_PASSWORD:

    st.warning("This dashboard is accessible only to administrators.")

    st.info("Please enter the administrator password.")

    st.stop()

# ------------------------------------
# Dashboard Starts
# ------------------------------------

st.success("✅ Login Successful")

st.title("📊 AI IT Support Genie Dashboard")

# ------------------------------------
# Load Database
# ------------------------------------

conn = sqlite3.connect("data/chatbot.db")

try:
    df = pd.read_sql("SELECT * FROM query_log", conn)

except:

    df = pd.DataFrame()

conn.close()

# ------------------------------------
# No Data
# ------------------------------------

if df.empty:

    st.warning("No chatbot data available.")

    st.stop()

# ------------------------------------
# Top Metrics
# ------------------------------------

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Total Queries",
        len(df)
    )

with col2:

    st.metric(
        "Categories",
        df["predicted_category"].nunique()
    )

with col3:

    st.metric(
        "SOP Recommended",
        df["sop_recommended"].replace("", pd.NA).dropna().count()
    )

st.markdown("---")

# ------------------------------------
# Category Distribution
# ------------------------------------

st.subheader("📊 Category Distribution")

category_count = (
    df["predicted_category"]
    .value_counts()
    .reset_index()
)

category_count.columns = [
    "Category",
    "Count"
]

fig = px.pie(
    category_count,
    names="Category",
    values="Count",
    hole=0.45
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ------------------------------------
# Query Trend
# ------------------------------------

st.subheader("📈 Query Trend")

trend = (
    df.groupby("timestamp")
    .size()
    .reset_index(name="Queries")
)

fig2 = px.line(
    trend,
    x="timestamp",
    y="Queries",
    markers=True
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ------------------------------------
# Recent Queries
# ------------------------------------

st.subheader("📝 Recent Queries")

st.dataframe(
    df.sort_values(
        "id",
        ascending=False
    ),
    use_container_width=True
)

# ------------------------------------
# Download Excel
# ------------------------------------

st.markdown("---")

buffer = BytesIO()

with pd.ExcelWriter(buffer, engine="openpyxl") as writer:

    df.to_excel(
        writer,
        index=False
    )

st.download_button(
    label="📥 Download Query History",
    data=buffer.getvalue(),
    file_name="Query_History.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    key="download_excel"
)

# ------------------------------------
# Delete Records
# ------------------------------------

st.markdown("---")

if st.button(
    "🗑 Delete All Records",
    key="delete_records"
):

    conn = sqlite3.connect("data/chatbot.db")

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM query_log"
    )

    conn.commit()

    conn.close()

    st.success("✅ Database Cleared Successfully")

    st.rerun()