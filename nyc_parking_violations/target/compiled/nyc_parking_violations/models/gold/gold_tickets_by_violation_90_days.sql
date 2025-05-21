SELECT
    silver_valid_violation_tickets.violation_code,
    silver_parking_violation_codes.definition AS violation_definition,
    COUNT(*) AS ticket_count
FROM
    "nyc_parking_violations"."main"."silver_valid_violation_tickets"
LEFT JOIN
    "nyc_parking_violations"."main"."silver_parking_violation_codes" AS silver_parking_violation_codes ON
        silver_valid_violation_tickets.violation_code = silver_parking_violation_codes.violation_code AND
        silver_valid_violation_tickets.is_manhattan_96th_st_below = silver_parking_violation_codes.is_manhattan_96th_st_below
WHERE
    silver_valid_violation_tickets.issue_date >= (SELECT MAX(issue_date) - INTERVAL '90 days' FROM "nyc_parking_violations"."main"."silver_valid_violation_tickets")
GROUP BY
    silver_valid_violation_tickets.violation_code,
    silver_parking_violation_codes.definition
ORDER BY
    ticket_count DESC