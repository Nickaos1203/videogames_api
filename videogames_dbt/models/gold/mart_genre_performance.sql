
{{ config(materialized='table', schema='gold') }}

SELECT
    g.genre_id,
    g.genre_name,
    COUNT(v.videogame_id) AS nombre_jeux,
    ROUND(AVG(v.score_metacritic), 2)
        AS score_metacritic_moyen,
    ROUND(AVG(v.score_utilisateurs), 2)
        AS score_utilisateurs_moyen

FROM {{ ref('genre') }} AS g

LEFT JOIN {{ ref('videogame') }} AS v
    ON g.genre_id = v.genre_id

GROUP BY
    g.genre_id,
    g.genre_name

