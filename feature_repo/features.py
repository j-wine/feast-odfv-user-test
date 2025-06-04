from datetime import timedelta
from feast import FeatureView, Field

from data_sources import push_source  # same push_source used before

import pandas as pd
from feast import Field, RequestSource, FeatureView
from feast.on_demand_feature_view import on_demand_feature_view
from feast.types import Int64, Float32, Float64

from data_sources import offline_filesource
from entities import product_entity, customer_entity
from data_sources import push_source

# Define a request data source for request-time features
input_request = RequestSource(
    name="vals_to_add",
    schema=[
        Field(name="val_to_add", dtype=Int64),
        Field(name="val_to_add_2", dtype=Int64),
    ],
)
product_feature_view = FeatureView(
    name="product_prices",
    entities=[product_entity],
    ttl=timedelta(days=7),
    schema=[
        Field(name="price", dtype=Float32),
    ],
    online=True,
    source=push_source,
    tags={},
)


customer_feature_view = FeatureView(
    name="customer_stats",
    entities=[customer_entity],
    ttl=timedelta(days=7),
    schema=[
        Field(name="revenue", dtype=Float32),
    ],
    online=True,
    source=push_source,
    tags={},
)
@on_demand_feature_view(
    entities=[product_entity, customer_entity],
    sources=[product_feature_view, customer_feature_view],
    schema=[
        Field(name="price_plus_rev", dtype=Float64)
    ],
    mode="pandas",
    write_to_online_store=False # compute on read
)
def transformed_price_read(features_df: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame()
    df["price_plus_rev"] = features_df["price"] + features_df["revenue"]
    return df

@on_demand_feature_view(
    entities=[product_entity, customer_entity],
    sources=[product_feature_view, customer_feature_view],
    schema=[
        Field(name="price_plus_revenue", dtype=Float64),
    ],
    mode="pandas",
    write_to_online_store=True # compute on write
)
def write_time_price_plus_revenue(features_df: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame()
    df["price_plus_revenue"] = features_df["price"] + features_df["revenue"]
    return df


@on_demand_feature_view(
    sources=[customer_feature_view],
    schema=[
        Field(name="revenue_plus_one", dtype=Float64),
    ],
    mode="pandas",
    write_to_online_store=True
)
def write_time_plus_one(features_df: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame()
    df["revenue_plus_one"] = 1 + features_df["revenue"]
    return df

