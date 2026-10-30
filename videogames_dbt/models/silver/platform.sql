
{{ 
    config(materialized='table', 
    schema='silver') 
}}


WITH plateformes AS (
    SELECT DISTINCT
        TRIM(p.platform_name) AS platform_name
    FROM {{ ref('stg_videogames') }} AS v
    CROSS JOIN LATERAL
        jsonb_array_elements_text(
            COALESCE(v.plateformes, '[]'::jsonb)
        ) AS p(platform_name)
    WHERE TRIM(p.platform_name) <> ''
)

SELECT
    ROW_NUMBER() OVER (
        ORDER BY platform_name
    ) AS platform_id,
    platform_name
FROM plateformes
