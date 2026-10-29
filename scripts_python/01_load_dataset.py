# Script de chargement des données brutes en json du dataset dans bronze.raw_videogames 
import json
import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import Json

# Chemins absolus calculés à partir de l'emplacement du script
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

# Chargement du .env situé à la racine du projet
load_dotenv(PROJECT_ROOT / ".env")

# Fichier JSON situé dans scripts_python
JSON_FILE = SCRIPT_DIR / "videogames_dataset.json"


def load_bronze():
    if not JSON_FILE.exists():
        raise FileNotFoundError(
            f"Fichier JSON introuvable : {JSON_FILE}"
        )

    with JSON_FILE.open("r", encoding="utf-8") as file:
        games = json.load(file)

    # Accepte une liste de jeux ou un objet unique
    if isinstance(games, dict):
        games = [games]

    if not isinstance(games, list):
        raise ValueError(
            "Le fichier JSON doit contenir une liste de jeux."
        )

    print("Database :", os.getenv("DB_NAME"))
    print("User :", os.getenv("DB_USER"))
    print("Password chargé :", bool(os.getenv("DB_PASSWORD")))

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
                processed = 0

                for game in games:
                    url = game.get("url")

                    if not url:
                        print(
                            f"Jeu ignoré : URL absente "
                            f"(id={game.get('id')})"
                        )
                        continue

                    cursor.execute(
                        """
                        INSERT INTO bronze.raw_videogames
                            (source_url, raw_data)
                        VALUES (%s, %s)
                        """,
                        ("https://www.metacritic.com", Json(game)),
                    )

                    processed += 1

        print(
            f"Chargement terminé : {processed} jeux traités."
        )

    finally:
        connection.close()


if __name__ == "__main__":
    load_bronze()
