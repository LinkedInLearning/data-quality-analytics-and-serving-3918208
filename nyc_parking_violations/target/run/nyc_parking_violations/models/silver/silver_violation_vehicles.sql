
  
    
    

    create  table
      "nyc_parking_violations"."main"."silver_violation_vehicles__dbt_tmp"
  
    as (
      SELECT
    summons_number,
    registration_state,
    plate_type,
    vehicle_body_type,
    vehicle_make,
    vehicle_expiration_date,
    vehicle_color,
    vehicle_year
FROM
    "nyc_parking_violations"."main"."silver_parking_violations"
    );
  
  