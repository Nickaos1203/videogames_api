
import os
from pathlib import Path

import pandas as pd
import psycopg2
import streamlit as st
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")


@st.cache_data(ttl=60)
def load_gold(table_name):
    allowed_tables = {
        "mart_videogame_performance",
        "mart_genre_performance",
        "mart_platform_performance",
        "mart_editor_performance",
        "mart_data_quality",
    }

    if table_name not in allowed_tables:
        raise ValueError(f"Table Gold non autorisée : {table_name}")

    connection = psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )

    try:
        return pd.read_sql_query(
            f"SELECT * FROM gold.{table_name}",
            connection,
        )
    finally:
        connection.close()
