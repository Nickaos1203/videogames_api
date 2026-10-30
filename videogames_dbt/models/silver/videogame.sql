
{{ config(materialized='table', schema='silver') }}

WITH jeux_doublon AS (
    SELECT
        v.*,
        ROW_NUMBER() OVER (
            PARTITION BY v.url
            ORDER BY v.scraped_at DESC
        ) AS rn
    FROM {{ ref('stg_videogames') }} AS v
)

SELECT
    ROW_NUMBER() OVER (
        ORDER BY v.url
    ) AS videogame_id,

    v.url,
    v.titre,
    v.date_sortie,
    v.description,
    v.score_metacritic,
    v.score_utilisateurs,
    e.editor_id,
    g.genre_id,
    v.scraped_at

FROM jeux_doublon AS v

LEFT JOIN {{ ref('editor') }} AS e
    ON NULLIF(TRIM(v.editeur), '') = e.editor_name

LEFT JOIN {{ ref('genre') }} AS g
    ON NULLIF(TRIM(v.genre), '') = g.genre_name

WHERE v.rn = 1
