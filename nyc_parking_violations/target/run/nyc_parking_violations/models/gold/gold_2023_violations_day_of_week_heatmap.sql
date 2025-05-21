
  
    
    

    create  table
      "nyc_parking_violations"."main"."gold_2023_violations_day_of_week_heatmap__dbt_tmp"
  
    as (
      WITH tickets_by_violation AS (
    SELECT
        silver_valid_violation_tickets.violation_code,
        silver_parking_violation_codes.definition AS violation_definition,
        CAST(SUM(CASE WHEN EXTRACT(dow FROM issue_date) = 0 THEN 1 ELSE 0 END) AS INTEGER) AS sunday,
        CAST(SUM(CASE WHEN EXTRACT(dow FROM issue_date) = 1 THEN 1 ELSE 0 END) AS INTEGER) AS monday,
        CAST(SUM(CASE WHEN EXTRACT(dow FROM issue_date) = 2 THEN 1 ELSE 0 END) AS INTEGER) AS tuesday,
        CAST(SUM(CASE WHEN EXTRACT(dow FROM issue_date) = 3 THEN 1 ELSE 0 END) AS INTEGER) AS wednesday,
        CAST(SUM(CASE WHEN EXTRACT(dow FROM issue_date) = 4 THEN 1 ELSE 0 END) AS INTEGER) AS thursday,
        CAST(SUM(CASE WHEN EXTRACT(dow FROM issue_date) = 5 THEN 1 ELSE 0 END) AS INTEGER) AS friday,
        CAST(SUM(CASE WHEN EXTRACT(dow FROM issue_date) = 6 THEN 1 ELSE 0 END) AS INTEGER) AS saturday
    FROM
        "nyc_parking_violations"."main"."silver_valid_violation_tickets"
    LEFT JOIN
        "nyc_parking_violations"."main"."silver_parking_violation_codes" AS silver_parking_violation_codes ON
            silver_valid_violation_tickets.violation_code = silver_parking_violation_codes.violation_code AND
            silver_valid_violation_tickets.is_manhattan_96th_st_below = silver_parking_violation_codes.is_manhattan_96th_st_below
    WHERE
        issue_date >= (SELECT MAX(issue_date) - INTERVAL '365 days' FROM silver_valid_violation_tickets)
    GROUP BY
        silver_valid_violation_tickets.violation_code,
        violation_definition
)

SELECT
    violation_code,
    violation_definition,
    sunday,
    monday,
    tuesday,
    wednesday,
    thursday,
    friday,
    saturday,
    (sunday + monday + tuesday + wednesday + thursday + friday + saturday) AS total_tickets
FROM
    tickets_by_violation
ORDER BY
    total_tickets DESC
    );
  
  