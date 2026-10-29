
{{ config(materialized='table') }}

SELECT
    ROW_NUMBER() OVER (
        ORDER BY platform_name
    )::INTEGER AS platform_id,
    platform_name

FROM (
    SELECT DISTINCT
        TRIM(p.platform_name) AS platform_name
    FROM {{ ref('stg_videogames') }} AS g
    CROSS JOIN LATERAL
        jsonb_array_elements_text(
            COALESCE(g.plateformes, '[]'::jsonb)
        ) AS p(platform_name)
    WHERE NULLIF(TRIM(p.platform_name), '') IS NOT NULL
) AS platforms
