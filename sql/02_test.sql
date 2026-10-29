-- requête pour vérifier les données dans la colonne en format JSONB 
SELECT
    ingestion_id,
    source_url,
    raw_data ->> 'titre' AS titre,
    raw_data ->> 'date' AS date_sortie,
    raw_data ->> 'plateformes' AS plateformes
FROM bronze.raw_videogames
LIMIT 10;