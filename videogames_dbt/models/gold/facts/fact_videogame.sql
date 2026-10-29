
{{ config(
    materialized='table',
    schema='gold'
) }}

SELECT
    ROW_NUMBER() OVER (
        ORDER BY v.url, p.platform_id
    ) AS videogame_id,

    p.platform_id,
    g.genre_id,
    e.editor_id,

    v.url,
    v.titre,
    v.date_sortie,
    v.score_metacritic,
    v.score_utilisateurs,

    1 AS game_count

FROM {{ ref('stg_videogames') }} AS v

CROSS JOIN LATERAL
    jsonb_array_elements_text(
        COALESCE(v.plateformes, '[]'::jsonb)
    ) AS plateforme(platform_name)

LEFT JOIN {{ ref('dim_plateforme') }} AS p
    ON TRIM(plateforme.platform_name) = p.platform_name

LEFT JOIN {{ ref('dim_genre') }} AS g
    ON TRIM(v.genre) = g.genre_name

LEFT JOIN {{ ref('dim_editor') }} AS e
    ON TRIM(v.editeur) = e.editor_name
