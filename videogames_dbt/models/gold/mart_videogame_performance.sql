
{{ 
    config(
        materialized='table', 
        schema='gold') 
}}

SELECT
    v.videogame_id,
    v.url,
    v.titre,
    v.date_sortie,
    e.editor_name,
    g.genre_name,
    v.score_metacritic,
    v.score_utilisateurs

FROM {{ ref('videogame') }} AS v

LEFT JOIN {{ ref('editor') }} AS e
    ON v.editor_id = e.editor_id

LEFT JOIN {{ ref('genre') }} AS g
    ON v.genre_id = g.genre_id
