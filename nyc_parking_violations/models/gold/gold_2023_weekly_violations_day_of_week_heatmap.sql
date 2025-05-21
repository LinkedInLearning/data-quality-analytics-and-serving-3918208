WITH tickets_by_weekday AS (
    SELECT
        CAST(EXTRACT(year FROM issue_date) AS VARCHAR) || '-W' || LPAD(CAST(EXTRACT(week FROM issue_date) AS VARCHAR), 2, '0') AS year_week,
        CAST(SUM(CASE WHEN EXTRACT(dow FROM issue_date) = 0 THEN 1 ELSE 0 END) AS INTEGER) AS sunday,
        CAST(SUM(CASE WHEN EXTRACT(dow FROM issue_date) = 1 THEN 1 ELSE 0 END) AS INTEGER) AS monday,
        CAST(SUM(CASE WHEN EXTRACT(dow FROM issue_date) = 2 THEN 1 ELSE 0 END) AS INTEGER) AS tuesday,
        CAST(SUM(CASE WHEN EXTRACT(dow FROM issue_date) = 3 THEN 1 ELSE 0 END) AS INTEGER) AS wednesday,
        CAST(SUM(CASE WHEN EXTRACT(dow FROM issue_date) = 4 THEN 1 ELSE 0 END) AS INTEGER) AS thursday,
        CAST(SUM(CASE WHEN EXTRACT(dow FROM issue_date) = 5 THEN 1 ELSE 0 END) AS INTEGER) AS friday,
        CAST(SUM(CASE WHEN EXTRACT(dow FROM issue_date) = 6 THEN 1 ELSE 0 END) AS INTEGER) AS saturday
    FROM
        {{ref('silver_valid_violation_tickets')}}
    WHERE
        issue_date >= (SELECT MAX(issue_date) - INTERVAL '365 days' FROM {{ref('silver_valid_violation_tickets')}})
    GROUP BY
        year_week
)

SELECT
    year_week,
    sunday,
    monday,
    tuesday,
    wednesday,
    thursday,
    friday,
    saturday
FROM
    tickets_by_weekday
ORDER BY
    year_week DESC