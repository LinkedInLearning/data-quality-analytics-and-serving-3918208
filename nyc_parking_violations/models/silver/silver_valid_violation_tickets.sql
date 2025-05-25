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
    {{ref('silver_violation_tickets')}}
WHERE
    EXTRACT(year FROM issue_date) == 2023 AND
    EXTRACT(month FROM issue_date) <= 8