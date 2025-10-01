-- eda.sql
-- Exploratory Data Analysis (EDA) queries for nyc_sales dataset
-- Each query addresses a specific dataset profiling metric.

-- 1. Count raw rows (total dataset size before filtering)
SELECT COUNT(*) AS n_raw
FROM nyc_sales;

-- 2. Count rows after filtering out non-sales
-- Sale price must be > 1000 to exclude deed transfers / errors
SELECT COUNT(*) AS n_clean
FROM nyc_sales
WHERE TRY_CAST(sale_price AS DOUBLE) > 1000;

-- 3. Percentage of rows retained after filtering
WITH counts AS (
  SELECT
    COUNT(*) AS n_raw,
    COUNT(*) FILTER (
      WHERE TRY_CAST(sale_price AS DOUBLE) > 1000
    ) AS n_clean
  FROM nyc_sales
)
SELECT
  n_raw,
  n_clean,
  ROUND(100.0 * n_clean / n_raw, 2) AS pct_retained
FROM counts;

-- 4. Sale price statistics:
-- Average, Median, and 95th percentile
WITH base AS (
  SELECT TRY_CAST(sale_price AS DOUBLE) AS sale_price
  FROM nyc_sales
  WHERE TRY_CAST(sale_price AS DOUBLE) > 1000
)
SELECT
  AVG(sale_price) AS avg_sale_price,
  MEDIAN(sale_price) AS median_sale_price,
  QUANTILE_CONT(sale_price, 0.95) AS p95_sale_price
FROM base;

-- 5. Percentage of rows with total_units = 0
-- These are problematic for per-unit calculations
WITH base AS (
  SELECT TRY_CAST(total_units AS DOUBLE) AS total_units
  FROM nyc_sales
  WHERE TRY_CAST(sale_price AS DOUBLE) > 1000
)
SELECT
  100.0 * SUM(CASE WHEN total_units = 0 THEN 1 ELSE 0 END) / COUNT(*) AS pct_zero_units
FROM base;

-- 6. Percentage of rows with missing gross_square_feet
-- Needed to assess data quality for unit size metrics
WITH base AS (
  SELECT TRY_CAST(gross_square_feet AS DOUBLE) AS gross_square_feet
  FROM nyc_sales
  WHERE TRY_CAST(sale_price AS DOUBLE) > 1000
)
SELECT
  100.0 * SUM(CASE WHEN gross_square_feet IS NULL THEN 1 ELSE 0 END) / COUNT(*) AS pct_missing_sqft
FROM base;