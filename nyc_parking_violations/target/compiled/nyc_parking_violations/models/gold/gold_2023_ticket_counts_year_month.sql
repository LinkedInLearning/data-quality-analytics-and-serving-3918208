WITH year_month_tickets AS (
    SELECT
        EXTRACT(year FROM issue_date) AS violation_year,
        EXTRACT(month FROM issue_date) AS violation_month,
        COUNT(*) AS ticket_count
    FROM
        "nyc_parking_violations"."main"."silver_valid_violation_tickets"
    GROUP BY
        violation_year,
        violation_month
),

previous_month_comparison AS (
    SELECT
        violation_year,
        violation_month,
        ticket_count,
        LAG(ticket_count) OVER (ORDER BY violation_year, violation_month) AS previous_month_ticket_count,
        CAST(violation_year AS VARCHAR) || '-' || LPAD(CAST(violation_month AS VARCHAR), 2, '0') AS year_month
    FROM
        year_month_tickets
)

SELECT
    year_month,
    ticket_count,
    previous_month_ticket_count,
    ticket_count - previous_month_ticket_count AS monthly_change,
    CASE
        WHEN previous_month_ticket_count IS NULL THEN NULL
        ELSE ROUND((ticket_count - previous_month_ticket_count) * 100.0 / previous_month_ticket_count, 1)
    END AS percent_change
FROM
    previous_month_comparison
ORDER BY
    violation_year DESC,
    violation_month DESC