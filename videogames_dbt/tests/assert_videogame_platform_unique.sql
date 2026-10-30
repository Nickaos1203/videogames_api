-- test pour vérifier que les relations videogame et platform apparaissent qu'une fois
SELECT
    videogame_id,
    platform_id
FROM {{ ref('videogame_platform') }}
GROUP BY
    videogame_id,
    platform_id
HAVING COUNT(*) > 1
