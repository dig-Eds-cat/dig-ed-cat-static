import json

from config import (
    TS_CLIENT,
    TS_SCHEMA_NAME,
    MANDATORY_FIELDS,
    NO_FACET_FIELDS,
    NO_INDEX_FIELDS,
)

from utils import (
    make_schema,
    delete_and_create_schema,
)

print("hallo, lets start indexing")

with open("./html/data/editions.json", "r") as f:
    editions_full = json.load(f)
print("Typesense Index")
print(f"defining Typesense collection schema with name: {TS_SCHEMA_NAME}")
ts_schema = make_schema(
    editions_full[0], "dig-ed-cat", MANDATORY_FIELDS, NO_FACET_FIELDS, NO_INDEX_FIELDS
)
with open("html/schema.json", "w") as f:
    json.dump(ts_schema, f, ensure_ascii=False, indent=4)

print(f"creating Typesense Collection with schema {TS_SCHEMA_NAME}")
cur_schema = delete_and_create_schema(TS_CLIENT, TS_SCHEMA_NAME, ts_schema)
print(f"schema created at {cur_schema['created_at']}")
print(f"start to index {len(editions_full)} records")
index = TS_CLIENT.collections[TS_SCHEMA_NAME].documents.import_(
    editions_full, {"action": "create"}
)
print(f"status of index-process: {index[0]}")
