import os

import pandas as pd
import streamlit as st
import plotly.express as px

from dotenv import load_dotenv
from sqlalchemy import create_engine, text, URL


load_dotenv()

DATABASE_URL = URL.create(
    "postgresql+psycopg2",
    username=os.environ["DB_USERNAME"],
    password=os.environ["DB_PASSWORD"],
    host=os.environ["DB_HOST"],
    port=os.environ["DB_PORT"],
    database=os.environ["DB_NAME"]
)


engine = create_engine(DATABASE_URL)


st.set_page_config(
    page_title="A Web Crawling Demo",
    page_icon="💻",
    layout="wide",
)

st.title("💻 E-commerce Price Monitoring Dashboard")


# --------------------------------
# Load data from PostgreSQL
# --------------------------------

@st.cache_data(ttl=300)
def load_data():

    query = """
        SELECT
            p.id AS product_id,
            p.title,
            p.price,
            p.price_unit,
            p.description,
            s.name AS source,
            c.name AS category
        FROM products p
        JOIN product_sources s
            ON p.source_id = s.id 
        JOIN product_categories c
            ON p.category_id = c.id 
    """

    with engine.connect() as conn:
        df = pd.read_sql(
            text(query),
            conn,
        )

    return df


df = load_data()

if df.empty:
    st.warning("No products found in the database.")
    st.stop()


# --------------------------------
# Overview metrics
# --------------------------------

total_products = df["product_id"].nunique()
total_sources = df["source"].nunique()

col1, col2, col3 = st.columns(3)

col1.metric("Total Products", total_products)
col2.metric("Websites Monitored", total_sources)

# --------------------------------
# Category selection
# --------------------------------

st.subheader("Product Categories")

product_categories = sorted(df["category"].unique())

selected_product = st.selectbox(
    "Select a category",
    product_categories,
)

filtered_df = df[
    df["category"] == selected_product
]

# --------------------------------
# Product data table
# --------------------------------

st.subheader("Price Observations")

st.dataframe(
    filtered_df,
    use_container_width=True,
)