
{{ 
    config(
        materialized='table', 
        schema='silver')
}}


WITH genres AS (
    SELECT DISTINCT
        TRIM(genre) AS genre_name
    FROM {{ ref('stg_videogames') }}
    WHERE genre IS NOT NULL
      AND TRIM(genre) <> ''
)

SELECT
    ROW_NUMBER() OVER (
        ORDER BY genre_name
    ) AS genre_id,
    genre_name
FROM genres
