# Root Cause Analysis Report
Type your findings here as you go through the course...

## **Issue Triage**
Short Term:
- Get the report working before the meeting with SQL fixes

Medium Term:
- Place DQ checks on found errors that "warn" when the pipeline runs

Long Term:
- Work with upstream teams to ensure proper data collection

## **Requirements Scoping**
For this project we will focus on short and medium term impact, but still provide suggestions for long term fix and kick off conversations.

## **Issue Replication**

Metric A
- `violation_location` went from a float to an int... strange, but probably not an issue
- `violation_county` is showing multiple new spellings for the "kings" value

Metric B
- County field changed and showing multiple spelling of "kings"
- Number of tickets are different, but unsure if it's just the repeat county names

Metric C
- `PHTO SCHOOL ZN SPEED VIOLATION` completely missing despite being the highest ticket count
- Counts are relatively the same for some, so need to looking further into the issue

Metric D
- Issue Agency `V` is missing
- New Issue Agency `XYZ` is now here, but it looks like a placeholder value (need to explore more)

Metric E
- Vehicle looks relatively the same, but ticket counts are drastically different like other graphs

Metric F
- Total ticket revenue went from ~$1.4M to ~$805k
- This is a massive difference and will cause the most alarm and need to prioritize

Metric G
- MAJOR FIND
- `Precinct 0` dropped from ~$664k to $50k while the numbers for all the precinct stayed the same
- That ~$600k difference is also about the same as the difference in Metric F

Metric H
- Relatively same distribution but the Average nearly dropped in half.

Metric I
- Distributions are relatively the same, so not worth focusing on at first

Metric J
- Seeing Agency XYZ again, and now agency V is missing

Metric K
- A complete drop off of values on Sunday

Metric L
- Similar issue for `county` value where we are seeing duplicate names but spelled differently

Metric M
- `PHTO SCHOOL ZN SPEED VIOLATION` completely missing similar to Metric C
- Notably most of the Sunday tickets are `PHTO SCHOOL ZN SPEED VIOLATION`, which may explain Metric K

## **Data Profiling**
Areas of Interest Worth Exploring:

1. Revenue and Precinct Data
    - Reasoning: Metrics F and G showed significant financial discrepancies.

    - Total ticket revenue dropped from ~$1.4M to ~$805k (Metric F).

    - Precinct 0 experienced a substantial revenue drop (~$664k to $50k) while other precincts remained stable (Metric G).

2. Violation Type Data
    - Reasoning: Metrics C and M indicate critical missing data.

    - `"PHTO SCHOOL ZN SPEED VIOLATION"` completely disappeared, significantly impacting daily counts, particularly on Sundays (Metrics C, M, K).

3. County Data
    - Reasoning: Metrics A, B, and L indicate county name inconsistencies.

    - Multiple new spellings or variations for `"Kings"` and `"Queens"` county appeared.

4. Issuing Agency Data
    - Reasoning: Metrics D and J highlight issues with issuing agencies.

    - Known agency `V` disappeared, and a new placeholder agency `XYZ` emerged.

All Gold metrics of interest are sourced from `silver_valid_violation_tickets` and `silver_parking_violation_codes`, thus those two tables and columns will be our starting point.

- `silver_valid_violation_tickets`
    - `violation_precinct`
    - `fee_usd`
    - `violation_code`
    - `violation_county`
    - `issuing_agency`

- `silver_parking_violation_codes`
    - `violation_code`
    - `definition`

We also want to explore the following pipeline chains:
- `silver_valid_violation_tickets` -> `silver_violation_tickets`

- `silver_violation_tickets` -> `silver_parking_violation_codes`

- `silver_violation_tickets` -> `silver_parking_violations`

- `silver_parking_violation_codes` -> `bronze_parking_violation_codes` (ingestion layer)

- `silver_parking_violations` -> `bronze_parking_violations` (ingestion layer)

Below are the results of that investigation:

*Comparing Key Metrics Across Pipeline Stages*

To efficiently profile data and identify discrepancies, I combined critical metrics into unified tables. These tables help us quickly pinpoint where data issues or logical transformations occur.

Initial Pipeline Comparison:

- The significant reduction in unique values and narrowing of the date range in the `silver_valid_violation_tickets` table indicates intentional filtering or validation logic occurring between `silver_violation_tickets` and `silver_valid_violation_tickets`.

- However, the reduced counts for `violation_precinct`, `violation_code`, `violation_county`, and `issuing_agency` raise concerns about potential unintended data exclusions or transformation errors.

*Filtered Pipeline Comparison (2023 data through August)*:

After applying the proper date filters (`year = 2023, month ≤ 8`):

- Filtering improved consistency in metrics, but discrepancies in `violation_precinct`, `violation_county`, and `issuing_agency` persist, confirming these as primary areas to investigate further.

- Revenue (`fee_usd`) will not be explored at this stage due to multiple potential influencing factors.

*Detailed Checks of Problematic Columns*

`violation_precinct`:

- Precinct `0` is missing from the validated silver dataset, clearly identifying an issue in the SQL or filtering logic during the transformation.

`violation_county`:

- Recommended data normalization for immediate fix to match original report baseline:
    - `["King's", "KINGS"]` → `"Kings"`
    - `["Queens", "QNS"]` → `"Qns"`

- NOTE:
    - According to the [NYC official website](https://portal.311.nyc.gov/article/?kanumber=KA-02877) there are only 5 boroughs and matching counties; which means we also just found a data quality issue in the original report.

    - Given our main task was to align the data to the original report, we will instead match the data to the report to get back to baseline, but I suggest to fix this later.

`issuing_agency`:

Distinct agency codes and ticket counts reveal a suspicious placeholder value:

- Agency `XYZ` appears to be a data quality anomaly:

  - Not visible in the original clean data visualizations.

  - Uses a three-character code, while all other agencies use a single-character code.

- Recommendation to explicitly flag agency `XYZ` to get back close to baseline report, but further validation is needed from the upstream data providers.

    - This will unfortunately not be able to be solved in the report because there is no way to know if `XYZ` is valid, and if valid, if it's replacing existing values.

    - Thus this will require downstream stakeholder communication of a limitation, how widespread the impact is, and escalation to the upstream data providers.

*Summary of Data Profiling Findings*:
- **`violation_precinct`**: Precinct `0` data missing from final silver stage indicates a business logic/filter issue.

- **`violation_county`**: Multiple inconsistent spellings clearly indicate upstream or ingestion data quality issues.

- **`issuing_agency`**: Agency `XYZ` suspected to be an erroneous placeholder value, requiring stakeholder validation.

## **Downstream Pipeline Investigation**
```sql
WHERE
    -- Meeting on August 27th, 2023 noted that we will try removing "precinct 0"
    -- until we can get a better data label for this value.
    --
    -- UPDATE September 1st, 2023: The "precinct 0" logic unexpectedly caused
    -- massive issues for the NYC Parking Violation Report as this precinct
    -- turns out not to be bad data but tied to `PHTO SCHOOL ZN SPEED VIOLATION`
    -- which is one of the largest drivers of ticket revenue.
    --
    -- We will comment out `violation_precinct != 0 AND` for now until we are
    -- able to implement a long-term solution and then remove.
    --
    -- violation_precinct != 0 AND
    EXTRACT(year FROM issue_date) == 2023 AND
    EXTRACT(month FROM issue_date) <= 8
```

**Implement DQ Fix**
Below are the three data quality check tests we implemented:

`nyc_parking_violations/tests/valid_issuing_agency_values.sql`
```sql
{{ config(severity = 'warn') }}

SELECT 
    issuing_agency
FROM 
    {{ ref('silver_valid_violation_tickets') }}
WHERE 
    issuing_agency IN ('XYZ')
```

`nyc_parking_violations/tests/valid_silver_precinct_0_exists.sql`
```sql
{{ config(severity = 'warn') }}

SELECT 0 AS violation_precinct
WHERE NOT EXISTS (
    SELECT
        1
    FROM
        {{ ref('silver_valid_violation_tickets') }}
    WHERE
        violation_precinct = 0
)
```

`nyc_parking_violations/tests/valid_violation_county_values.sql`
```sql
{{ config(severity = 'warn') }}

SELECT 
    violation_county
FROM 
    {{ ref('silver_valid_violation_tickets') }}
WHERE 
    violation_county IN ('King''s', 'KINGS', 'Queens', 'QNS')
```

Implemented fix for `nyc_parking_violations/models/silver/silver_valid_violation_tickets.sql`:
```sql
SELECT
    summons_number,
    issue_date,
    violation_code,
    is_manhattan_96th_st_below,
    issuing_agency,
    violation_location,
    violation_precinct,
    issuer_precinct,
    issuer_code,
    issuer_command,
    issuer_squad,
    violation_time,
    -- Add this CASE WHEN to standardize county values for now until we are
    -- able to implement a long-term solution and then remove.
    CASE 
        WHEN violation_county = 'King''s' THEN 'Kings'
        WHEN violation_county = 'KINGS' THEN 'Kings'
        WHEN violation_county = 'Queens' THEN 'Qns'
        WHEN violation_county = 'QNS' THEN 'Qns'
        ELSE violation_county
    END AS violation_county,
    fee_usd
FROM
    {{ref('silver_violation_tickets')}}
WHERE
    -- Meeting on August 27th, 2023 noted that we will try removing "precinct 0"
    -- until we can get a better data label for this value.
    --
    -- UPDATE September 1st, 2023: The "precinct 0" logic unexpectedly caused
    -- massive issues for the NYC Parking Violation Report as this precinct
    -- turns out not to be bad data but tied to `PHTO SCHOOL ZN SPEED VIOLATION`
    -- which is one of the largest drivers of ticket revenue.
    --
    -- We will comment out `violation_precinct != 0 AND` for now until we are
    -- able to implement a long-term solution and then remove.
    --
    -- violation_precinct != 0 AND
    EXTRACT(year FROM issue_date) == 2023 AND
    EXTRACT(month FROM issue_date) <= 8
```

## **Stakeholder Communication**

SBAR Communication: Data Quality Issue in NYC Parking Violation Report

*Situation*
- Significant discrepancies in NYC Parking Violation Report metrics.
- Revenue dropped drastically (~$1.4M → ~$805k).
- Missing critical data (`Precinct 0`, `PHTO SCHOOL ZN SPEED VIOLATION`).

*Background*
- Issue tied to recent data pipeline transformation.
- `Precinct 0` incorrectly excluded, impacting major revenue driver.
- Inconsistent county spellings (`Kings`, `Queens`).
- Unexpected agency code (`XYZ`).

*Assessment*
- Revenue drop primarily due to exclusion of `Precinct 0`.
- "PHTO SCHOOL ZN SPEED VIOLATION" disappearance affecting counts, especially Sundays.
- County name variations indicate upstream data quality issues.
- Agency `XYZ` likely placeholder or erroneous entry.

*Recommendation*
- *Immediate & Medium-Term Actions (Completed):*
  - Reverted exclusion of `Precinct 0`.
  - Implemented data normalization for county names.
  - DQ checks established for agency `XYZ`, county consistency, and precinct presence to provide warnings so we no longer have a silent failure.

- *Long-Term Actions:*
  - Engage upstream teams to improve data collection and validate agency `XYZ` authenticity.
