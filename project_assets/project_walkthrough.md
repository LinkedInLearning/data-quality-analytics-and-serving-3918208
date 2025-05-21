# LinkedIn Learning: Data Quality Downstream Project Walkthrough

### Scenario:

In this project you are a data engineer that's been tasked with resolving data quality issues found by your business stakeholders downstream. Specifically, your stakeholders are in the middle of monthly reporting that relies heavily on NYC parking violations data and thus need an urgent fix.

Your previous implementation of dbt was a huge success and everyone in the dept uses assets off of it. Unfortunately, your department has been plagued by data quality issues lately, and the department's main report that leadership reads is completely wrong. Last week the report was perfect, but today it's a complete mess

Thankfully your manager saved a report from right before the issues showed up, thus your goal is to get the report back to the accurate state before the major dept meeting next week. You also need to create a RCA report to share with the data team to help prevent future issues.

By the end of this project, you should be able to conduct a root cause analysis on data quality issues, clearly communicate the issues and potential solution to relevant parties, and implement a data quality fix.

### Data:

This project utilizes two public government datasets sourced from NYC Open Data:

**1. [NYC Parking Violations Issued - Fiscal Year 2023](https://data.cityofnewyork.us/City-Government/Parking-Violations-Issued-Fiscal-Year-2023/pvqr-7yc4)**  
> Parking Violations Issuance datasets contain violations issued during the respective fiscal year. The Issuance datasets are not updated to reflect violation status, the information only represents the violation(s) at the time they are issued. Since appearing on an issuance dataset, a violation may have been paid, dismissed via a hearing, statutorily expired, or had other changes to its status. To see the current status of outstanding parking violations, please look at the Open Parking & Camera Violations dataset.

Note that this dataset is rather large for this project, so we will use a sample of 100K records.

**2. [NYC Department of Finance Parking Violation Codes](https://data.cityofnewyork.us/Transportation/DOF-Parking-Violation-Codes/ncbg-6agr)**  
> This dataset defines the parking violation codes in New York City and lists the fines. Each fine amount includes a $15 New York State Criminal Justice surcharge.

### Project Structure:
```
linkedin-learning-dq-downstream/
├── nyc_parking_violations/                    # Main DBT project directory
│ ├── models/                                  # Database models organized in medallion architecture
│ │ ├── bronze/                                # Raw data ingestion layer
│ │ ├── silver/                                # Data transformation and cleansing layer
│ │ ├── gold/                                  # Analytics and reporting layer
│ │ └── docs/                                  # Documentation for the models
│ ├── tests/                                   # DBT tests directory
├── data/                                      # Raw data directory
├── project_assets/                            # Additional project documentation
│ |── project_walkthrough.md                   # Project walkthrough documentation
│ └── NYC_Parking_Violations_Report            # Original Report Without Data Quality Issues
├── scripts/                                   # Python scripts directory
│ ├── create_nyc_parking_violations_report.py  # Report generation script
│ └── utils.py                                 # Utility functions
├── notebooks/                               # Notebooks to run code
│ ├── 1_run_data_pipelines_here.ipynb        # Jupyter notebook for data pipeline execution
│ ├── 2_run_report_here.ipynb                    # Jupyter notebook for report execution
│ ├── 3_run_sql_queries_here.ipynb               # Jupyter notebook for SQL queries
│ └── 4_root_cause_analysis_report.md            # Markdown to document root cause analysis
└── requirements.txt                           # Python dependencies
```

# Part 1 - Intro

### 1.1 - Project Scenario
- Video intro (live action)
- Explain the project (show recordings of doing the course)
- Introduction to Chaos Engineering
- What to expect for this project

### 1.2 - Overview of Coding Environment and Repository
- GitHub Codespaces introduction
- Project repo navigation
- Using the CLI
- Navigating dbt docs

### 1.3 - Overview of Data Architecture and Assets
- Data infrastructure overview
- Available datasets and report
- Running the report script
- Querying the database

### 1.4 - The 9 Data Quality Dimensions
- Validity
- Completeness
- Consistency
- Integrity
- Timeliness
- Currency
- Reasonableness
- Uniqueness
- Accuracy

### 1.5 - The Data Quality Resolution Process (Downstream)
https://dataproducts.substack.com/p/the-data-quality-resolution-process
- 0. Stakeholder Surfaces Issue
- 1. Issue Triage
- 2. Requirements Scoping
- 3. Issue Replication
- 4. Data Profiling
- 5. Downstream Pipeline Investigation
- 6. Implement DQ Fix
- 7. Stakeholder Communication

# Part 2 - Exercise 1 (Validity, Completeness, and Consistency)

### 2.1 - Issue Replication

### 2.2 - Data Profiling

### 2.3 - Downstream Pipeline Investigation

### 2.4 - Downstream Pipeline Investigation

### 2.5 - Implement DQ Fix

### 2.6 - Stakeholder Communication

# Part 3 - Exercise 2 (Integrity, Timeliness, and Currency)

### 3.1 - Issue Replication

### 3.2 - Data Profiling

### 3.3 - Downstream Pipeline Investigation

### 3.4 - Downstream Pipeline Investigation

### 3.5 - Implement DQ Fix

### 3.6 - Stakeholder Communication

# Part 4 - Exercise 3 (Reasonableness, Uniqueness, and Accuracy)

### 4.1 - Issue Replication

### 4.2 - Data Profiling

### 4.3 - Downstream Pipeline Investigation

### 4.4 - Downstream Pipeline Investigation

### 4.5 - Implement DQ Fix

### 4.6 - Stakeholder Communication