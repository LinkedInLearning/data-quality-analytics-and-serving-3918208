WITH year_week_tickets AS (
    SELECT
        EXTRACT(year FROM issue_date) AS violation_year,
        EXTRACT(week FROM issue_date) AS week_of_year,
        COUNT(*) AS ticket_count
    FROM
        "nyc_parking_violations"."main"."silver_valid_violation_tickets"
    GROUP BY
        violation_year,
        week_of_year
),

previous_week_comparison AS (
    SELECT
        violation_year,
        week_of_year,
        ticket_count,
        LAG(ticket_count) OVER (ORDER BY week_of_year) AS previous_week_ticket_count,
        CAST(violation_year AS VARCHAR) || '-W' || LPAD(CAST(week_of_year AS VARCHAR), 2, '0') AS year_week
    FROM
        year_week_tickets
)

SELECT
    year_week,
    ticket_count,
    previous_week_ticket_count,
    ticket_count - previous_week_ticket_count AS weekly_change,
    CASE
        WHEN previous_week_ticket_count IS NULL THEN NULL
        ELSE ROUND((ticket_count - previous_week_ticket_count) * 100.0 / previous_week_ticket_count, 1)
    END AS percent_change
FROM
    previous_week_comparison
ORDER BY
    violation_year DESC,
    week_of_year DESC