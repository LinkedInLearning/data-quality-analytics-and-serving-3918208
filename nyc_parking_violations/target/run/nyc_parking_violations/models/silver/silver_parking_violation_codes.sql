
  
    
    

    create  table
      "nyc_parking_violations"."main"."silver_parking_violation_codes__dbt_tmp"
  
    as (
      WITH manhattan_violation_codes AS (
    SELECT
        violation_code,
        definition,
        TRUE AS is_manhattan_96th_st_below,
        manhattan_96th_st_below AS fee_usd,
    FROM
        "nyc_parking_violations"."main"."bronze_parking_violation_codes"
),

all_other_violation_codes AS (
    SELECT
        violation_code,
        definition,
        FALSE AS is_manhattan_96th_st_below,
        all_other_areas AS fee_usd,
    FROM
        "nyc_parking_violations"."main"."bronze_parking_violation_codes"
)

SELECT * FROM manhattan_violation_codes
UNION ALL
SELECT * FROM all_other_violation_codes
ORDER BY violation_code ASC
    );
  
  