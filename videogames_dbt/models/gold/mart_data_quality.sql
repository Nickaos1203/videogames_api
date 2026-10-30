
{{ config(
    materialized='table',
    schema='gold'
) }}

WITH
videogames AS (
    SELECT * FROM {{ ref('videogame') }}
),

platform_links AS (
    SELECT * FROM {{ ref('videogame_platform') }}
),

duplicate_urls AS (
    SELECT url
    FROM videogames
    WHERE url IS NOT NULL
    GROUP BY url
    HAVING COUNT(*) > 1
),

duplicate_platform_links AS (
    SELECT videogame_id, platform_id
    FROM platform_links
    GROUP BY videogame_id, platform_id
    HAVING COUNT(*) > 1
),

checks AS (

    -- Complétude : titre
    SELECT
        'missing_game_title' AS check_name,
        'completeness' AS quality_dimension,
        'videogame' AS table_name,
        COUNT(*)::BIGINT AS total_records,
        COUNT(*) FILTER (
            WHERE titre IS NULL OR TRIM(titre) = ''
        )::BIGINT AS failed_records
    FROM videogames

    UNION ALL

    -- Complétude : URL
    SELECT
        'missing_game_url',
        'completeness',
        'videogame',
        COUNT(*)::BIGINT,
        COUNT(*) FILTER (
            WHERE url IS NULL OR TRIM(url) = ''
        )::BIGINT
    FROM videogames

    UNION ALL

    -- Unicité : URL
    SELECT
        'duplicate_game_url',
        'uniqueness',
        'videogame',
        COUNT(*)::BIGINT,
        COUNT(*) FILTER (
            WHERE url IN (SELECT url FROM duplicate_urls)
        )::BIGINT
    FROM videogames

    UNION ALL

    -- Validité : score Metacritic
    SELECT
        'invalid_metacritic_score',
        'validity',
        'videogame',
        COUNT(*)::BIGINT,
        COUNT(*) FILTER (
            WHERE score_metacritic IS NOT NULL
              AND (
                  score_metacritic < 0
                  OR score_metacritic > 100
              )
        )::BIGINT
    FROM videogames

    UNION ALL

    -- Validité : score utilisateurs
    SELECT
        'invalid_user_score',
        'validity',
        'videogame',
        COUNT(*)::BIGINT,
        COUNT(*) FILTER (
            WHERE score_utilisateurs IS NOT NULL
              AND (
                  score_utilisateurs < 0
                  OR score_utilisateurs > 10
              )
        )::BIGINT
    FROM videogames

    UNION ALL

    -- Unicité : relation jeu-plateforme
    SELECT
        'duplicate_game_platform',
        'uniqueness',
        'videogame_platform',
        COUNT(*)::BIGINT,
        COALESCE(SUM(
            CASE
                WHEN (videogame_id, platform_id) IN (
                    SELECT videogame_id, platform_id
                    FROM duplicate_platform_links
                ) THEN 1
                ELSE 0
            END
        ), 0)::BIGINT
    FROM platform_links
)

SELECT
    check_name,
    quality_dimension,
    table_name,
    total_records,
    failed_records,

    ROUND(
        100.0 * (total_records - failed_records)
        / NULLIF(total_records, 0),
        2
    ) AS quality_rate_pct,

    CASE
        WHEN total_records = 0 THEN 'WARNING'
        WHEN failed_records = 0 THEN 'PASS'
        ELSE 'FAIL'
    END AS status

FROM checks
