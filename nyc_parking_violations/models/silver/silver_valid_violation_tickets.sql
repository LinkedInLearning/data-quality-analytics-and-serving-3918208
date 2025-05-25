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
    -- Add this CASE WHEN to standardize county values for now until we are
    -- able to implement a long-term solution and then remove.
    CASE 
        WHEN violation_county = 'King''s' THEN 'Kings'
        WHEN violation_county = 'KINGS' THEN 'Kings'
        WHEN violation_county = 'Queens' THEN 'Qns'
        WHEN violation_county = 'QNS' THEN 'Qns'
        ELSE violation_county
    END AS violation_county,
    fee_usd
FROM
    {{ref('silver_violation_tickets')}}
WHERE
    -- Meeting on August 27th, 2023 noted that we will try removing "precinct 0"
    -- until we can get a better data label for this value.
    --
    -- UPDATE September 1st, 2023: The "precinct 0" logic unexpectedly caused
    -- massive issues for the NYC Parking Violation Report as this precinct
    -- turns out not to be bad data but tied to `PHTO SCHOOL ZN SPEED VIOLATION`
    -- which is one of the largest drivers of ticket revenue.
    --
    -- We will comment out `violation_precinct != 0 AND` for now until we are
    -- able to implement a long-term solution and then remove.
    --
    -- violation_precinct != 0 AND
    EXTRACT(year FROM issue_date) == 2023 AND
    EXTRACT(month FROM issue_date) <= 8