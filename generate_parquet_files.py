import datetime
import random

import pandas as pd
import numpy as np
from pathlib import Path

CUSTOMERS = 100
PRODUCTS = 100

def generate_data(num_customers: int, num_products: int) -> pd.DataFrame:
    # Create full cross join
    customer_ids = list(range(num_customers))
    product_ids = list(range(num_products))
    df = pd.DataFrame(
        [(c, p) for c in customer_ids for p in product_ids],
        columns=["customer_id", "product_id"]
    )

    # Assign the same timestamp to all (optional: vary it slightly per row)
    df["event_timestamp"] = pd.Timestamp.now(tz="UTC")

    # Add random features
    num_rows = len(df)
    features = ["price", "revenue"]
    feature_data = np.random.randint(1, 100, size=(num_rows, 2))  # customizable range

    for i, feat in enumerate(features):
        df[feat] = feature_data[:, i]

    return df

if __name__ == "__main__":
    output_path = Path(__file__).parent / "feature_repo/offline_data/generated_data.parquet"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = generate_data(num_customers=CUSTOMERS, num_products=PRODUCTS)
    df.to_parquet(output_path, index=False)
    print(f"✅ Generated {output_path} with shape {df.shape}")
