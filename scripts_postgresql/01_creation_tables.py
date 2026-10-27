import os
import psycopg2
from dotenv import load_dotenv


# Chargement des variables d'environnement
load_dotenv()

print("Database :", os.getenv("DB_NAME"))
print("User :", os.getenv("DB_USER"))
print("Password chargé :", bool(os.getenv("DB_PASSWORD")))


# Connexion PostgreSQL
conn = psycopg2.connect(
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    host=os.getenv("DB_HOST", "localhost"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT", "5432")
)


create_schemas = """
    CREATE SCHEMA IF NOT EXISTS bronze;
    CREATE SCHEMA IF NOT EXISTS silver;
    CREATE SCHEMA IF NOT EXISTS gold;
"""

# création de la table comprenant les données brut du fichier json avec des informations sur leurs sources
create_table_raw = """
    CREATE TABLE bronze.raw_videogames (
    ingestion_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source_url TEXT,
    scraped_at TIMESTAMPTZ DEFAULT NOW(),
    raw_data JSONB NOT NULL
);
"""