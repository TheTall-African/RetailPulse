import os
import random
from datetime import datetime, timedelta

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text


# -------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# -------------------------------------------------
load_dotenv()


# -------------------------------------------------
# CREATE DATABASE CONNECTION
# -------------------------------------------------
database_url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    database=os.getenv("DB_NAME")
)

engine = create_engine(database_url)


# -------------------------------------------------
# CREATE EVENTS TABLE
# -------------------------------------------------
create_table_query = """
CREATE TABLE IF NOT EXISTS events (
    event_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    session_id VARCHAR(50) NOT NULL,
    event_time TIMESTAMP NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    product_id VARCHAR(50),
    device VARCHAR(20),
    revenue NUMERIC(10, 2) DEFAULT 0
);
"""


with engine.begin() as connection:

    connection.execute(text(create_table_query))

    # Clear old sample data every time we reseed
    connection.execute(
        text("TRUNCATE TABLE events RESTART IDENTITY;")
    )


# -------------------------------------------------
# GENERATE SAMPLE E-COMMERCE DATA
# -------------------------------------------------
random.seed(42)

rows = []

start_date = datetime(2026, 9, 1, 10, 0, 0)

devices = [
    "mobile",
    "desktop",
    "tablet"
]

products = [
    f"P{i:03d}"
    for i in range(1, 51)
]


# Create 500 shopping sessions
for session_number in range(1, 501):

    session_id = f"S{session_number:04d}"

    user_id = random.randint(1, 300)

    device = random.choices(
        devices,
        weights=[0.60, 0.35, 0.05]
    )[0]

    event_time = start_date + timedelta(
        minutes=random.randint(
            0,
            60 * 24 * 14
        )
    )

    product_id = random.choice(products)


    # ---------------------------------------------
    # HOMEPAGE VIEW
    # ---------------------------------------------
    rows.append({
        "user_id": user_id,
        "session_id": session_id,
        "event_time": event_time,
        "event_type": "homepage_view",
        "product_id": None,
        "device": device,
        "revenue": 0
    })


    # ---------------------------------------------
    # PRODUCT VIEW
    # ---------------------------------------------
    if random.random() < 0.82:

        event_time += timedelta(minutes=1)

        rows.append({
            "user_id": user_id,
            "session_id": session_id,
            "event_time": event_time,
            "event_type": "product_view",
            "product_id": product_id,
            "device": device,
            "revenue": 0
        })


        # -----------------------------------------
        # ADD TO CART
        # -----------------------------------------
        if random.random() < 0.38:

            event_time += timedelta(minutes=2)

            rows.append({
                "user_id": user_id,
                "session_id": session_id,
                "event_time": event_time,
                "event_type": "add_to_cart",
                "product_id": product_id,
                "device": device,
                "revenue": 0
            })


            # -------------------------------------
            # CHECKOUT
            # -------------------------------------
            if random.random() < 0.72:

                event_time += timedelta(minutes=2)

                rows.append({
                    "user_id": user_id,
                    "session_id": session_id,
                    "event_time": event_time,
                    "event_type": "checkout",
                    "product_id": product_id,
                    "device": device,
                    "revenue": 0
                })


                # ---------------------------------
                # PURCHASE
                # ---------------------------------
                if random.random() < 0.74:

                    event_time += timedelta(minutes=2)

                    revenue = round(
                        random.uniform(30, 180),
                        2
                    )

                    rows.append({
                        "user_id": user_id,
                        "session_id": session_id,
                        "event_time": event_time,
                        "event_type": "purchase",
                        "product_id": product_id,
                        "device": device,
                        "revenue": revenue
                    })


# -------------------------------------------------
# CONVERT TO DATAFRAME
# -------------------------------------------------
events_df = pd.DataFrame(rows)


# -------------------------------------------------
# LOAD DATA INTO POSTGRESQL
# -------------------------------------------------
events_df.to_sql(
    "events",
    engine,
    if_exists="append",
    index=False,
    method="multi"
)


print(
    f"Database seeded successfully with "
    f"{len(events_df)} events."
)