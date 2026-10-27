import os
import psycopg2
from dotenv import load_dotenv

# Chargement des variables .env
load_dotenv()

# Vérification du chargement
print("Database :", os.getenv("DB_NAME"))
print("User :", os.getenv("DB_USER"))
print("Password chargé :", bool(os.getenv("DB_PASSWORD")))


