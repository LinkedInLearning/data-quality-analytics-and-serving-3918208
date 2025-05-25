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

## **Data Profiling**

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

## **Downstream Pipeline Investigation**
Write your notes here...

**Implement DQ Fix**
Write your notes here...

## **Stakeholder Communication**
Write your notes here...