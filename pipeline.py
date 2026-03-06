"""ETL pipeline — extract, transform, load."""

import sys
import pandas as pd
from pathlib import Path


def extract(filepath: str) -> pd.DataFrame:
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Source not found: {filepath}")
    df = pd.read_csv(filepath)
    print(f"[EXTRACT] {len(df)} rows from {filepath}")
    return df


def transform(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(subset=["customer_name", "product", "region"]).copy()
    df = df[df["quantity"] > 0]
    df["order_date"] = pd.to_datetime(df["order_date"], format="mixed", dayfirst=False)
    df["status"] = df["status"].str.strip().str.lower()
    df["total_price"] = (df["quantity"] * df["unit_price"]).round(2)
    print(f"[TRANSFORM] {len(df)} rows after cleaning")
    return df.reset_index(drop=True)


def load(df: pd.DataFrame, output_path: str) -> str:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path, index=False, engine="pyarrow")
    print(f"[LOAD] Wrote {len(df)} rows to {output_path}")
    return output_path


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "data/sample/sales_raw.csv"
    dst = sys.argv[2] if len(sys.argv) > 2 else "data/output/sales_clean.parquet"
    load(transform(extract(src)), dst)
