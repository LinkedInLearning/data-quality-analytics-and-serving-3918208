SELECT
    issuing_agency,
    COUNT(*) AS ticket_count
FROM
    {{ref('silver_valid_violation_tickets')}}
WHERE
    issue_date >= (SELECT MAX(issue_date) - INTERVAL '90 days' FROM {{ref('silver_valid_violation_tickets')}})
GROUP BY
    issuing_agency
ORDER BY
    ticket_count DESC