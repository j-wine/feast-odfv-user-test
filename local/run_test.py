from feast import FeatureStore
from datetime import datetime, timedelta
import pandas as pd

store = FeatureStore("../feature_repo")

now = pd.Timestamp.now(tz="UTC")

push_df = pd.DataFrame({
    "product_id": [58],
    "price": [9.0],
    "customer_id": [74],
    "revenue": [41.0],
    "event_timestamp": [now]
})


print("\n✅ Schritt 1: Push to basic FeatureViews")
store.push("my_push_source", push_df)

# 2. read post push(on-read + on-write ODFVs)
print("\n📤 Schritt 2: get_online_features post Push")
res_push = store.get_online_features(
    features=[
        # "write_time_price_plus_revenue:price_plus_revenue",
        "write_time_plus_one:revenue_plus_one",
        # "transformed_price_read:price_plus_rev"
    ],
    entity_rows=[{
        "product_id": 58,
        "customer_id": 74
    }]
).to_df()
print(res_push)

print("\n<UNK> Schritt 3: write_to_online_store into basic feature view")
customer_df = pd.DataFrame({
    "customer_id": [123],
    "revenue": [41.0],
    "event_timestamp": [pd.Timestamp.now(tz="UTC")],
})
store.write_to_online_store(feature_view_name="customer_stats", df=customer_df)

product_df = pd.DataFrame({
    "product_id": [123],
    "price": [9.0],
    "event_timestamp": [pd.Timestamp.now(tz="UTC")],
})
store.write_to_online_store(feature_view_name="product_prices", df=product_df)
res_write = store.get_online_features(
    features=[
        "write_time_price_plus_revenue:price_plus_revenue",
        "write_time_plus_one:revenue_plus_one",
        "transformed_price_read:price_plus_rev",
    ],
    entity_rows=[{
        "product_id": 58,
        "customer_id": 74
    }]
).to_df()
print(f"res write_to_online: {res_write}")


# 3. Materialize from offline store source
print("\n🛠️ Schritt 3: materialization")
store.materialize(
    start_date=datetime.now() - timedelta(days=1),
    end_date=datetime.now() + timedelta(minutes=5)
)

# 4. Read post materialization
print("\n📥 Schritt 4: get_online_features post materialization")
res_materialized = store.get_online_features(
    features=[
        "write_time_price_plus_revenue:price_plus_revenue",
        "write_time_plus_one:revenue_plus_one",
        "transformed_price_read:price_plus_rev",
    ],
    entity_rows=[{
        "product_id": 58,
        "customer_id": 74
    }]
).to_df()
print(res_materialized)

# 5. Evaluation of missing entitiy
print("\n Comparison Write-Time vs. Read-Time ODFV")
for col in ["price_plus_revenue", "revenue_plus_one"]:
    value = res_materialized[col].iloc[0]
    print(f"{col}: {'✅ OK' if pd.notnull(value) else '❌ Missing'} (Wert: {value})")
