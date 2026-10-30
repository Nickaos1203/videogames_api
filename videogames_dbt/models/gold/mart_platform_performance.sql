
{{ 
    config(
        materialized='table', 
        schema='gold') 
}}

SELECT
    p.platform_id,
    p.platform_name,
    COUNT(DISTINCT v.videogame_id) AS nombre_jeux,
    ROUND(AVG(v.score_metacritic), 2)
        AS score_metacritic_moyen,
    ROUND(AVG(v.score_utilisateurs), 2)
        AS score_utilisateurs_moyen

FROM {{ ref('platform') }} AS p

LEFT JOIN {{ ref('videogame_platform') }} AS vp
    ON p.platform_id = vp.platform_id

LEFT JOIN {{ ref('videogame') }} AS v
    ON vp.videogame_id = v.videogame_id

GROUP BY
    p.platform_id,
    p.platform_name
