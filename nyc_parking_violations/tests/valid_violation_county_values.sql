{{ config(severity = 'warn') }}

SELECT 
    violation_county
FROM 
    {{ ref('silver_valid_violation_tickets') }}
WHERE 
    violation_county IN ('King''s', 'KINGS', 'Queens', 'QNS')