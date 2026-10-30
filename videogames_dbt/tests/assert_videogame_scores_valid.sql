-- Test pour vérifier la cohérence des scores des jeux vidéo

SELECT
    videogame_id,
    score_metacritic,
    score_utilisateurs
FROM {{ ref('videogame') }}
WHERE
    (score_metacritic IS NOT NULL
     AND (score_metacritic < 0 OR score_metacritic > 100))
    OR
    (score_utilisateurs IS NOT NULL
     AND (score_utilisateurs < 0 OR score_utilisateurs > 10))
