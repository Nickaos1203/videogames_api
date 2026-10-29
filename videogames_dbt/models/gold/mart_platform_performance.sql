-- Table d'analyse des performance en fonction des plateformes
{{ config(materialized='table') }}

SELECT
    platform AS plateforme,
    COUNT(*) AS nombre_jeux,
    ROUND(AVG(score_metacritic), 2) AS score_metacritic_moyen,
    ROUND(AVG(score_utilisateurs), 2) AS score_utilisateurs_moyen

FROM {{ ref('stg_videogames') }} AS games
CROSS JOIN LATERAL
    jsonb_array_elements_text(games.plateformes) AS platform

GROUP BY platform

ORDER BY nombre_jeux DESC
