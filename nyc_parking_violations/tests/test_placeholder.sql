{{ config(severity = 'warn') }}

WITH this_is_a_test AS (
    SELECT
        'this is a test' AS test_value
)

SELECT
    test_value
FROM
    this_is_a_test
WHERE
    test_value != 'this is a test'