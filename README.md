1. Project Overview

This repository contains my solution for the Soostone Data Engineer take-home assignment, which covers:

Exploratory analysis (EDA) of the raw NYC property sales dataset.

Standard SQL queries to compute required metrics (z-scores, per-unit metrics).

Python 3 + DuckDB script to generate the final enriched dataset.

2. Initial Exploratory Analysis
Dataset Overview

Raw rows: 84,548

<img width="191" height="118" alt="image" src="https://github.com/user-attachments/assets/94c17c1f-fd3f-440a-ac54-3fe00e711979" />


After filtering sale_price > 1000: 58,604 (~69% retained)

<img width="350" height="144" alt="image" src="https://github.com/user-attachments/assets/16bedf99-1456-4579-b34d-052c1641b751" />


Average sale price: $1.52M

Median sale price: $639K (distribution is heavily skewed)

95th percentile: $4.05M

~28% of rows have total_units = 0 (problematic for per-unit metrics)

~37% of rows missing gross_square_feet

Insights

Sale prices are heavy-tailed → use log scale for normalization.

Clear borough/neighborhood stratification in per-unit pricing.

Data quality issues (0 units, missing sqft) must be handled before modeling.

3. SQL Queries (EDA + Metrics)

All queries assume the CSV has been loaded into DuckDB as a table nyc_sales with snake_case column names (sale_price, total_units, etc.), please check the eda.sql

4. Running SQL in VSCode with DuckDB Extension

    1. Generate DuckDB database
    Run the bootstrap script: init_duckdb.py
    2. Configure VSCode SQLTools
    Install SQLTools and DuckDB extension
    Add new connection → DuckDB → point to nyc.duckdb.
    Save and connect
    3. Run Queries: eda.sql

5. Python Script for Enriched Dataset

The main deliverable is the Python3 script (soostone_solution.py) that:
Normalizes column names.
Filters non-sales.
Computes required metrics.
Outputs enriched dataset to CSV.
Script: soostone_solution.py

6. Deliverables

EDA SQL: eda.sql
Python script: soostone_solution.py
Enriched dataset: nyc_sales_enriched.csv
Database file (optional): nyc.duckdb

7. How to Run

-- Create virtual environment

python3 -m venv .venv
source .venv/bin/activate

-- Install dependencies

pip install duckdb pandas

-- Generate enriched dataset

python3 soostone_solution.py

8. Potential Enhancements

Enforce data quality contracts (no negative/zero units, valid sqft ranges).

Add rolling medians per neighborhood for robust trend features.

Enrich with geospatial (census tract, transit proximity, etc).

Build as-of snapshots to avoid data leakage in modeling pipelines.
