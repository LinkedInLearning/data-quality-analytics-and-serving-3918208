SELECT
    violation_county,
    COUNT(*) AS ticket_count
FROM
    {{ref('silver_valid_violation_tickets')}}
WHERE
    issue_date >= (SELECT MAX(issue_date) - INTERVAL '90 days' FROM {{ref('silver_valid_violation_tickets')}})
GROUP BY
    violation_county
ORDER BY
    ticket_count DESC