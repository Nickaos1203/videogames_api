
{{ 
    config(
    materialized='view',
    schema='silver'
    ) 
}}

SELECT
    ingestion_id,
    NULLIF(TRIM(raw_data ->> 'titre'), '') AS titre,

    CASE
        WHEN TRIM(raw_data ->> 'date') ~ '^[A-Z][a-z]{2} [0-9]{1,2}, [0-9]{4}$'
        THEN TO_DATE(TRIM(raw_data ->> 'date'), 'Mon DD, YYYY')
        ELSE NULL
    END AS date_sortie,

    raw_data -> 'plateformes' AS plateformes,
    NULLIF(TRIM(raw_data ->> 'editeur'), '') AS editeur,
    NULLIF(TRIM(raw_data ->> 'url'), '') AS url,
    NULLIF(TRIM(raw_data ->> 'genre'), '') AS genre,
    NULLIF(TRIM(raw_data ->> 'description'), '') AS description,

    CASE
        WHEN TRIM(raw_data ->> 'score_metacritic') ~ '^[0-9]+$'
        THEN (raw_data ->> 'score_metacritic')::INTEGER
        ELSE NULL
    END AS score_metacritic,

    CASE
        WHEN NULLIF(TRIM(raw_data->>'score_utilisateurs'), '') IS NULL
            THEN NULL
        WHEN (raw_data->>'score_utilisateurs')::NUMERIC BETWEEN 0 AND 10
            THEN (raw_data->>'score_utilisateurs')::NUMERIC
        ELSE NULL
    END AS score_utilisateurs,
    
    source_url,
    scraped_at

FROM {{ source('bronze', 'raw_videogames') }}
