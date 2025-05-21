
  
    
    

    create  table
      "nyc_parking_violations"."main"."gold_tickets_by_agency_90_days__dbt_tmp"
  
    as (
      SELECT
    issuing_agency,
    COUNT(*) AS ticket_count
FROM
    "nyc_parking_violations"."main"."silver_valid_violation_tickets"
WHERE
    issue_date >= (SELECT MAX(issue_date) - INTERVAL '90 days' FROM "nyc_parking_violations"."main"."silver_valid_violation_tickets")
GROUP BY
    issuing_agency
ORDER BY
    ticket_count DESC
    );
  
  