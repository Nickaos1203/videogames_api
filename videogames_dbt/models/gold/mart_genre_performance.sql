-- Table d'analyse les performances des jeux par genre
{{ config(materialized='table') }}

SELECT
    genre,
    COUNT(*) AS nombre_jeux,
    ROUND(AVG(score_metacritic), 2) AS score_metacritic_moyen,
    ROUND(AVG(score_utilisateurs), 2) AS score_utilisateurs_moyen,
    COUNT(score_metacritic) AS nombre_scores_critiques,
    COUNT(score_utilisateurs) AS nombre_scores_utilisateurs

FROM {{ ref('stg_videogames') }}

WHERE genre IS NOT NULL

GROUP BY genre
