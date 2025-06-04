from datetime import timedelta

from feast import KafkaSource, FileSource, PushSource, RequestSource, Field
from feast.data_format import JsonFormat, FileFormat, ParquetFormat
from feast.types import Int64

BENCHMARK_TOPIC = "benchmark_entity_topic"
def generate_schema_json(num_features: int) -> str:
    base_fields = [
        "benchmark_entity int",
        "event_timestamp timestamp"
    ]
    feature_fields = [f"feature_{i} int" for i in range(num_features)]
    return ", ".join(base_fields + feature_fields)

offline_filesource = FileSource(file_format=ParquetFormat(), path="offline_data/generated_data.parquet")

push_source = PushSource(
    name="my_push_source",
    batch_source=offline_filesource
)


# Define a request data source for request-time features
input_request = RequestSource(
    name="vals_to_add",
    schema=[
        Field(name="val_to_add", dtype=Int64),
        Field(name="val_to_add_2", dtype=Int64),
    ],
)
