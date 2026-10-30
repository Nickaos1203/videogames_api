
{{ 
    config(materialized='table', 
    schema='silver') 
}}


WITH jeux_plateformes AS (
    SELECT DISTINCT
        v.url,
        TRIM(p.platform_name) AS platform_name
    FROM {{ ref('stg_videogames') }} AS v

    CROSS JOIN LATERAL
        jsonb_array_elements_text(
            COALESCE(v.plateformes, '[]'::jsonb)
        ) AS p(platform_name)

    WHERE TRIM(p.platform_name) <> ''
)

SELECT DISTINCT
    v.videogame_id,
    p.platform_id

FROM jeux_plateformes AS jp

INNER JOIN {{ ref('videogame') }} AS v
    ON jp.url = v.url

INNER JOIN {{ ref('platform') }} AS p
    ON jp.platform_name = p.platform_name
