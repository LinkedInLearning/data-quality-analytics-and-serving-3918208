{{ config(severity = 'warn') }}

SELECT 0 AS violation_precinct
WHERE NOT EXISTS (
    SELECT
        1
    FROM
        {{ ref('silver_valid_violation_tickets') }}
    WHERE
        violation_precinct = 0
)