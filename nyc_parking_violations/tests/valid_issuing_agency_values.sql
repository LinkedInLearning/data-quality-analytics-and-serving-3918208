{{ config(severity = 'warn') }}

SELECT 
    issuing_agency
FROM 
    {{ ref('silver_valid_violation_tickets') }}
WHERE 
    issuing_agency IN ('XYZ')