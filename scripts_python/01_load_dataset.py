import json
import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import Json

# Chargement des variables .env
load_dotenv()

# Vérification du chargement
print("Database :", os.getenv("DB_NAME"))
print("User :", os.getenv("DB_USER"))
print("Password chargé :", bool(os.getenv("DB_PASSWORD")))

JSON_PATH = "scripts_python" / "videogames_dataset.json"

def load_bronze():
    if not JSON_PATH.exists():
        raise FileNotFoundError(
            f"Fichier JSON introuvable : {JSON_PATH}"
        )

    with JSON_PATH.open("r", encoding="utf-8") as file:
        games = json.load(file)

    if not isinstance(games, list):
        raise ValueError(
            "Le fichier JSON doit contenir une liste de jeux."
        )

    connection = psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )

    try:
        with connection:
            with connection.cursor() as cursor:
                for game in games:
                    url = game.get("url")

                    if not url:
                        print("Jeu ignoré : URL absente")
                        continue

                    cursor.execute(
                        """
                        INSERT INTO bronze.raw_videogames
                            (source_url, raw_data)
                        VALUES (%s, %s)
                        ON CONFLICT (source_url)
                        DO UPDATE SET
                            raw_data = EXCLUDED.raw_data,
                            scraped_at = NOW();
                        """,
                        (url, Json(game)),
                    )

        print(f"Chargement terminé : {len(games)} jeux traités.")

    finally:
        connection.close()


if __name__ == "__main__":
    load_bronze()
