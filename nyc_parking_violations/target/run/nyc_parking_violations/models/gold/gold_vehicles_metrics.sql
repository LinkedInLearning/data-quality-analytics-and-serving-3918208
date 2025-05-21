
  
    
    

    create  table
      "nyc_parking_violations"."main"."gold_vehicles_metrics__dbt_tmp"
  
    as (
      SELECT
    registration_state,
    COUNT(summons_number) AS ticket_count,
FROM
    "nyc_parking_violations"."main"."silver_violation_vehicles"
WHERE
    registration_state != 'NY'
GROUP BY
    registration_state
ORDER BY
    ticket_count DESC
    );
  
  