from feast import Entity, ValueType

product_entity = Entity(
    name="product_entity",
    join_keys=["product_id"],
    value_type=ValueType.INT64,
)

customer_entity = Entity(
    name="customer_entity",
    join_keys=["customer_id"],
    value_type=ValueType.INT64,
)
