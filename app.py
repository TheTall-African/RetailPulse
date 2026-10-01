import os 
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text

#PAGE CONFIGURATION
st.set_page_config(
    page_title="RetailPulse",
    page_icon="📊",
    layout="wide"
)

#LOAD ENVIRONMENT VARIABLES
load_dotenv()

#DATABASE CONNECTION
@st.cache_resource
def get_database_connection():

    database_url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME")
    )

    return create_engine(database_url)

#function call for getting the database to connect to UI
engine = get_database_connection()

#load KPI data
@st.cache_data

def load_kpis():
    query="""
    SELECT
        COUNT(DISTINCT session_id) AS total_sessions,

        COUNT(
            DISTINCT CASE
                WHEN event_type = 'purchase'
                THEN session_id
            END
        ) AS purchase,
        
        SUM(
            CASE
                WHEN event_type = 'purchase'
                THEN revenue
                ELSE 0
            END
        ) AS total_revenue
    
    FROM events;
    """

    with engine.connect() as connection:
        return pd.read_sql(query, connection)


#LOAD FUNNEL DATA
@st.cache_data

def load_funnel():
    query = """
    WITH FUNNEL AS(
        SELECT 
            COUNT(DISTINCT session_id) AS total_sessions,
            COUNT(DISTINCT CASE WHEN event_type = 'product_view' THEN session_id END) AS product_views,
            COUNT(DISTINCT CASE WHEN event_type = 'add_to_cart' THEN session_id END) AS add_to_cart,
            COUNT(DISTINCT CASE WHEN event_type = 'checkout' THEN session_id END) AS checkout,
            COUNT(DISTINCT CASE WHEN event_type = 'purchase' THEN session_id END) AS purchase
        FROM events
    )
    
    SELECT *
    FROM (
        SELECT 1 AS step_order, 'Sessions' AS step, total_sessions AS sessions
        FROM funnel
        
        UNION ALL
        
        SELECT 2, 'Product View', product_views
        FROM funnel
        
        UNION ALL
        
        SELECT 3, 'Add to Cart', add_to_cart
        FROM funnel
        
        UNION ALL
        
        SELECT 4, 'Checkout', checkout
        FROM funnel
        
        UNION ALL
        
        SELECT 5, 'Purchase', purchase
        FROM funnel
    ) funnel_steps
    
    ORDER BY step_order;
    """

    with engine.connect() as connection:
        return pd.read_sql(text(query), connection)

#APPLICATION HEADER
st.title("RetailPulse")
st.subheader("E-Commerce Product Analytics")
st.write("Analyze customer behavior, conversion, revenue, and product performance.")

#GET DATA
kpis = load_kpis().iloc[0]
funnel = load_funnel()

total_sessions = int(kpis["total_sessions"])
purchase = int(kpis["purchase"])
total_revenue = float(kpis["total_revenue"])

#Avoid division by zero error
if total_sessions>0:
    conversion_rate = (purchase/total_sessions)*100
else:
    conversion_rate = 0



#KPI CARDS
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Sessions", f"{total_sessions:,}")

with col2:
    st.metric("Purchases", f"{purchase:,}")

with col3:
    st.metric("Conversion Rate", f"{conversion_rate:.2f}%")

with col4:
    st.metric("Total Revenue", f"${total_revenue:,.2f}")


#CUSTOMER FUNNEL
st.divider()
st.subheader("Customer Conversion Funnel")

funnel_chart = (funnel[["step", "sessions"]].set_index("step"))
st.bar_chart(funnel_chart)


#FUNNEL TABLE
st.subheader("Funnel Breakdown")
st.dataframe(funnel[["step", "sessions"]], use_container_width = True, hide_index=True)
