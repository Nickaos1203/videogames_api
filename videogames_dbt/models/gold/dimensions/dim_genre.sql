
{{ config(materialized='table') }}

SELECT
    ROW_NUMBER() OVER (
        ORDER BY genre_name
    )::INTEGER AS genre_id,
    genre_name

FROM (
    SELECT DISTINCT
        TRIM(genre) AS genre_name
    FROM {{ ref('stg_videogames') }}
    WHERE NULLIF(TRIM(genre), '') IS NOT NULL
) AS genres
