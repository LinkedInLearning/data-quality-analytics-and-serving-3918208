
  
    
    

    create  table
      "nyc_parking_violations"."main"."gold_precinct_ticket_fee_sum_90_days__dbt_tmp"
  
    as (
      WITH precinct_fees AS (
    SELECT
        silver_valid_violation_tickets.issuer_precinct,
        silver_parking_violation_codes.fee_usd
    FROM
        "nyc_parking_violations"."main"."silver_valid_violation_tickets"
    LEFT JOIN
        "nyc_parking_violations"."main"."silver_parking_violation_codes" AS silver_parking_violation_codes ON
            silver_valid_violation_tickets.violation_code = silver_parking_violation_codes.violation_code AND
            silver_valid_violation_tickets.is_manhattan_96th_st_below = silver_parking_violation_codes.is_manhattan_96th_st_below
    WHERE
        silver_valid_violation_tickets.issue_date >= (SELECT MAX(issue_date) - INTERVAL '90 days' FROM "nyc_parking_violations"."main"."silver_valid_violation_tickets")
)

SELECT
    issuer_precinct,
    SUM(fee_usd) AS total_ticket_fees_usd
FROM
    precinct_fees
GROUP BY
    issuer_precinct
ORDER BY
    total_ticket_fees_usd DESC
    );
  
  