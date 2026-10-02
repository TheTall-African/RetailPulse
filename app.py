import os

import pandas as pd
import streamlit as st

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text

from queries import (
    KPI_QUERY,
    FUNNEL_QUERY,
    DEVICE_QUERY,
    PRODUCT_QUERY,
    DAILY_QUERY,
    CUSTOMER_SEGMENT_QUERY
)


# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------
st.set_page_config(
    page_title="RetailPulse",
    page_icon="📊",
    layout="wide"
)


# -------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# -------------------------------------------------
load_dotenv()


# -------------------------------------------------
# DATABASE CONNECTION
# -------------------------------------------------
@st.cache_resource
def get_database_connection():

    database_url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("DB_NAME")
    )

    return create_engine(database_url)


engine = get_database_connection()


# -------------------------------------------------
# GENERIC QUERY FUNCTION
# -------------------------------------------------
@st.cache_data
def run_query(query):

    with engine.connect() as connection:

        return pd.read_sql(
            text(query),
            connection
        )


# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
kpi_data = run_query(KPI_QUERY)

funnel_data = run_query(FUNNEL_QUERY)

device_data = run_query(DEVICE_QUERY)

product_data = run_query(PRODUCT_QUERY)

daily_data = run_query(DAILY_QUERY)

customer_data = run_query(
    CUSTOMER_SEGMENT_QUERY
)


# -------------------------------------------------
# APPLICATION HEADER
# -------------------------------------------------
st.title("RetailPulse")

st.subheader(
    "E-Commerce Product Analytics Platform"
)

st.caption(
    "SQL-driven analysis of customer behavior, "
    "conversion, revenue, products, and customer segments."
)


# -------------------------------------------------
# KPI CARDS
# -------------------------------------------------
kpis = kpi_data.iloc[0]


col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        "Sessions",
        f"{int(kpis['total_sessions']):,}"
    )


with col2:

    st.metric(
        "Purchases",
        f"{int(kpis['purchases']):,}"
    )


with col3:

    st.metric(
        "Conversion Rate",
        f"{kpis['conversion_rate']:.2f}%"
    )


with col4:

    st.metric(
        "Revenue",
        f"${kpis['total_revenue']:,.2f}"
    )


with col5:

    st.metric(
        "Average Order Value",
        f"${kpis['average_order_value']:,.2f}"
    )


st.divider()


# -------------------------------------------------
# NAVIGATION TABS
# -------------------------------------------------
overview_tab, funnel_tab, device_tab, product_tab, customer_tab = st.tabs(
    [
        "Overview",
        "Conversion Funnel",
        "Devices",
        "Products",
        "Customers"
    ]
)


# -------------------------------------------------
# OVERVIEW TAB
# -------------------------------------------------
with overview_tab:

    st.header(
        "Performance Overview"
    )

    st.subheader(
        "Daily Conversion Rate"
    )

    daily_conversion = (
        daily_data[
            [
                "event_date",
                "conversion_rate"
            ]
        ]
        .set_index("event_date")
    )

    st.line_chart(
        daily_conversion
    )


    st.subheader(
        "Daily Revenue"
    )

    daily_revenue = (
        daily_data[
            [
                "event_date",
                "revenue"
            ]
        ]
        .set_index("event_date")
    )

    st.line_chart(
        daily_revenue
    )


    st.subheader(
        "Daily Performance"
    )

    st.dataframe(
        daily_data,
        use_container_width=True,
        hide_index=True
    )


# -------------------------------------------------
# FUNNEL TAB
# -------------------------------------------------
with funnel_tab:

    st.header(
        "Customer Conversion Funnel"
    )


    funnel_chart = (
        funnel_data[
            [
                "step",
                "sessions"
            ]
        ]
        .set_index("step")
    )


    st.bar_chart(
        funnel_chart
    )


    st.subheader(
        "Funnel Performance"
    )


    st.dataframe(
        funnel_data[
            [
                "step",
                "sessions",
                "overall_conversion_pct",
                "step_conversion_pct",
                "dropoff_sessions",
                "dropoff_pct"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


    # Identify largest funnel loss
    funnel_losses = (
        funnel_data[
            funnel_data["step_order"] > 1
        ]
        .sort_values(
            "dropoff_pct",
            ascending=False
        )
    )


    if not funnel_losses.empty:

        largest_loss = (
            funnel_losses.iloc[0]
        )


        st.info(
            f"Largest funnel drop-off occurs at "
            f"{largest_loss['step']}: "
            f"{largest_loss['dropoff_pct']:.2f}% "
            f"of users from the previous stage "
            f"did not continue."
        )


# -------------------------------------------------
# DEVICE TAB
# -------------------------------------------------
with device_tab:

    st.header(
        "Device Performance"
    )


    st.write(
        "Compare customer behavior and "
        "commercial performance across devices."
    )


    device_conversion = (
        device_data[
            [
                "device",
                "conversion_rate"
            ]
        ]
        .set_index("device")
    )


    st.subheader(
        "Conversion Rate by Device"
    )


    st.bar_chart(
        device_conversion
    )


    st.subheader(
        "Device Metrics"
    )


    st.dataframe(
        device_data,
        use_container_width=True,
        hide_index=True
    )


# -------------------------------------------------
# PRODUCT TAB
# -------------------------------------------------
with product_tab:

    st.header(
        "Product Performance"
    )


    st.write(
        "Analyze which products convert "
        "customer interest into purchases and revenue."
    )


    top_products = (
        product_data
        .head(10)
    )


    st.subheader(
        "Top Products by Revenue"
    )


    product_revenue_chart = (
        top_products[
            [
                "product_id",
                "revenue"
            ]
        ]
        .set_index("product_id")
    )


    st.bar_chart(
        product_revenue_chart
    )


    st.subheader(
        "Product Metrics"
    )


    st.dataframe(
        product_data,
        use_container_width=True,
        hide_index=True
    )


# -------------------------------------------------
# CUSTOMER TAB
# -------------------------------------------------
with customer_tab:

    st.header(
        "Customer Segmentation"
    )


    st.write(
        "Understand how browsing and purchasing "
        "behavior differs across customer groups."
    )


    customer_revenue = (
        customer_data[
            [
                "customer_segment",
                "revenue"
            ]
        ]
        .set_index("customer_segment")
    )


    st.subheader(
        "Revenue by Customer Segment"
    )


    st.bar_chart(
        customer_revenue
    )


    st.subheader(
        "Customer Segment Metrics"
    )


    st.dataframe(
        customer_data,
        use_container_width=True,
        hide_index=True
    )