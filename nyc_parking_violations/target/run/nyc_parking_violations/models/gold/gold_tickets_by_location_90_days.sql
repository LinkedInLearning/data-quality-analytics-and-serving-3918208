
  
    
    

    create  table
      "nyc_parking_violations"."main"."gold_tickets_by_location_90_days__dbt_tmp"
  
    as (
      SELECT
    violation_precinct,
    violation_location,
    violation_county,
    COUNT(*) AS ticket_count
FROM
    "nyc_parking_violations"."main"."silver_valid_violation_tickets"
WHERE
    issue_date >= (SELECT MAX(issue_date) - INTERVAL '90 days' FROM "nyc_parking_violations"."main"."silver_valid_violation_tickets")
GROUP BY
    violation_precinct,
    violation_location,
    violation_county
ORDER BY
    ticket_count DESC
    );
  
  