
import os
from pathlib import Path

import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

ALLOWED_TABLES = {
    "mart_videogame_performance",
    "mart_genre_performance",
    "mart_platform_performance",
    "mart_editor_performance",
    "mart_data_quality",
}


def get_connection():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        connect_timeout=5,
    )


def fetch_gold_table(
    table_name: str,
    limit: int = 100,
    offset: int = 0,
    search_column: str | None = None,
    search: str | None = None,
):
    if table_name not in ALLOWED_TABLES:
        raise ValueError("Table non autorisée.")

    query = f'SELECT * FROM gold."{table_name}"'
    params = []

    if search and search_column:
        # Les colonnes de recherche sont elles aussi contrôlées.
        allowed_search_columns = {
            "titre",
            "genre_name",
            "platform_name",
            "editor_name",
        }

        if search_column not in allowed_search_columns:
            raise ValueError("Colonne de recherche non autorisée.")

        query += f' WHERE "{search_column}" ILIKE %s'
        params.append(f"%{search}%")

    query += " LIMIT %s OFFSET %s"
    params.extend([limit, offset])

    connection = get_connection()

    try:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    finally:
        connection.close()


def check_database():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            return True
    finally:
        connection.close()
