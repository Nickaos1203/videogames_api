
{{ config(
    materialized='table',
    schema='gold'
) }}

WITH editors AS (
    SELECT DISTINCT
        TRIM(editeur) AS editor_name
    FROM {{ ref('stg_videogames') }}
    WHERE editeur IS NOT NULL
      AND TRIM(editeur) <> ''
)

SELECT
    ROW_NUMBER() OVER (
        ORDER BY editor_name
    ) AS editor_id,
    editor_name
FROM editors
