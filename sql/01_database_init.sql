-- Création de la base de données sur PostgreSQL
CREATE DATABASE videogames_database;


-- Création des schémas representant l'architecture en médaillon
CREATE SCHEMA bronze;
CREATE SCHEMA silver;
CREATE SCHEMA gold;


-- Création de la table comprenant les données brut en json + informations sur la source
CREATE TABLE bronze.raw_videogames (
    ingestion_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source_url TEXT,
    scraped_at TIMESTAMPTZ DEFAULT NOW(),
    raw_data JSONB NOT NULL
);


-- Autorisation sur la base de données, remplacez [USER] par le nom de l'utilisateur
GRANT USAGE, CREATE ON SCHEMA bronze TO [USER];
GRANT USAGE, CREATE ON SCHEMA silver TO [USER];
GRANT USAGE, CREATE ON SCHEMA gold TO [USER];