
SELECT *
FROM {{ ref('mart_data_quality') }}
WHERE
    failed_records < 0
    OR failed_records > total_records
    OR (
        total_records > 0
        AND (
            quality_rate_pct < 0
            OR quality_rate_pct > 100
        )
    )
