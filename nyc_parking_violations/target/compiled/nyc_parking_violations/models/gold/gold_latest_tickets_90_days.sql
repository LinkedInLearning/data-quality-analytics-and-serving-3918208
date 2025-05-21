SELECT
    summons_number,
    issue_date,
    violation_code,
    is_manhattan_96th_st_below,
    issuing_agency,
    violation_location,
    violation_precinct,
    issuer_precinct,
    issuer_code,
    issuer_command,
    issuer_squad,
    violation_time,
    violation_county,
    fee_usd
FROM
    "nyc_parking_violations"."main"."silver_valid_violation_tickets"
WHERE
    issue_date >= (SELECT MAX(issue_date) - INTERVAL '90 days' FROM "nyc_parking_violations"."main"."silver_valid_violation_tickets")
ORDER BY
    issue_date DESC