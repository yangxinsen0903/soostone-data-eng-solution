# init_duckdb.py
# Initialize a DuckDB database from the raw NYC sales CSV.
# Reads CSV
# Normalizes column names to snake_case
# Creates a DuckDB file with table nyc_sales
import duckdb
import pandas as pd

CSV = "nyc-rolling-sales.csv"   # Input CSV (must be in same directory as script)
DB  = "nyc.duckdb"              # Output DuckDB file to be created

# Step 1: Normalize column names (to snake_case for easier SQL usage)
def norm(c):
    return (c.strip().lower()
              .replace(" ", "_")
              .replace("-", "_")
              .replace("/", "_"))

df = pd.read_csv(CSV)
df.columns = [norm(c) for c in df.columns]

# Step 2: Create DuckDB database and load table
con = duckdb.connect(DB)
con.register("t_raw", df)
con.execute("CREATE OR REPLACE TABLE nyc_sales AS SELECT * FROM t_raw")
con.close()

print("created", DB, "with table nyc_sales and snake_case columns.")