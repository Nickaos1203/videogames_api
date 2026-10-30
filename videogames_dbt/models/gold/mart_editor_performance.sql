
{{ config(materialized='table', schema='gold') }}

SELECT
    e.editor_id,
    e.editor_name,
    COUNT(v.videogame_id) AS nombre_jeux,
    ROUND(AVG(v.score_metacritic), 2)
        AS score_metacritic_moyen,
    ROUND(AVG(v.score_utilisateurs), 2)
        AS score_utilisateurs_moyen

FROM {{ ref('editor') }} AS e

LEFT JOIN {{ ref('videogame') }} AS v
    ON e.editor_id = v.editor_id

GROUP BY
    e.editor_id,
    e.editor_name
