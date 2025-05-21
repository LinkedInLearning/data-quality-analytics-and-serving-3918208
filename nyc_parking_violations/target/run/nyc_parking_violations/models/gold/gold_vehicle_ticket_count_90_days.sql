
  
    
    

    create  table
      "nyc_parking_violations"."main"."gold_vehicle_ticket_count_90_days__dbt_tmp"
  
    as (
      WITH valid_vehicle_tickets AS (
    SELECT
        silver_valid_violation_tickets.summons_number,
        silver_violation_vehicles.vehicle_make,
        silver_violation_vehicles.plate_type,
        silver_violation_vehicles.registration_state
    FROM
        "nyc_parking_violations"."main"."silver_valid_violation_tickets"
    INNER JOIN
        "nyc_parking_violations"."main"."silver_violation_vehicles"
        ON silver_valid_violation_tickets.summons_number = silver_violation_vehicles.summons_number
    WHERE
        silver_valid_violation_tickets.issue_date >= (SELECT MAX(issue_date) - INTERVAL '90 days' FROM "nyc_parking_violations"."main"."silver_valid_violation_tickets")
)

SELECT
    vehicle_make,
    plate_type,
    registration_state,
    COUNT(*) AS ticket_count
FROM
    valid_vehicle_tickets
GROUP BY
    vehicle_make,
    plate_type,
    registration_state
ORDER BY
    ticket_count DESC
    );
  
  