import duckdb
import pandas as pd

csv_path = "nyc-rolling-sales.csv"
out_path = "nyc_sales_enriched.csv"

# Step 1: Load CSV into pandas
df_raw = pd.read_csv(csv_path)

# Step 2: Normalize column names (spaces -> underscores, lowercase)
def normalize(col):
    return (
        col.strip().lower()
        .replace(" ", "_")
        .replace("-", "_")
        .replace("/", "_")
    )

df_raw.columns = [normalize(c) for c in df_raw.columns]

print("✅ Normalized columns:", df_raw.columns.tolist())

# Step 3: Register with DuckDB
con = duckdb.connect()
con.register("nyc_sales", df_raw)

# Step 4: Run SQL
query = """
WITH base AS (
  SELECT
    TRY_CAST(sale_price AS DOUBLE) AS sale_price,
    TRY_CAST(total_units AS DOUBLE) AS total_units,
    TRY_CAST(gross_square_feet AS DOUBLE) AS gross_square_feet,
    neighborhood,
    COALESCE(building_class_at_time_of_sale, building_class_category) AS building_class
  FROM nyc_sales
  WHERE TRY_CAST(sale_price AS DOUBLE) > 1000
),
global_stats AS (
  SELECT
    AVG(sale_price) AS mu,
    STDDEV_POP(sale_price) AS sigma
  FROM base
),
segmented AS (
  SELECT b.*,
         (b.sale_price - gs.mu) / NULLIF(gs.sigma,0) AS sale_price_zscore,
         AVG(b.sale_price) OVER (PARTITION BY neighborhood, building_class) AS seg_mu,
         STDDEV_POP(b.sale_price) OVER (PARTITION BY neighborhood, building_class) AS seg_sigma
  FROM base b CROSS JOIN global_stats gs
)
SELECT neighborhood,
       building_class,
       sale_price,
       total_units,
       gross_square_feet,
       sale_price_zscore,
       (sale_price - seg_mu) / NULLIF(seg_sigma,0) AS sale_price_zscore_neighborhood,
       gross_square_feet / NULLIF(total_units,0) AS square_ft_per_unit,
       sale_price / NULLIF(total_units,0) AS price_per_unit
FROM segmented
"""

df = con.execute(query).fetchdf()

# Step 5: Save results
df.to_csv(out_path, index=False)
print("Enriched dataset saved to %s" % out_path)
print(df.head())
