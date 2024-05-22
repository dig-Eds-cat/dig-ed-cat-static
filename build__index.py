import json
import pandas as pd
from slugify import slugify
from utils import resolve_number_codes, strip

from config import (
    EDITIONS,
    INSTITUTIONS,
    TS_CLIENT,
    TS_SCHEMA_NAME,
    MANDATORY_FIELDS,
    FACET_FIELDS,
    NO_FACET_FIELDS,
    NO_INDEX_FIELDS,
)

from utils import (
    make_schema,
    delete_and_create_schema,
)

print("hallo, lets start indexing")

print(f"fetching {EDITIONS}")
df = pd.read_csv(EDITIONS).head(-1)
df = df.astype("str")
df = df.replace(["nan", ""], "not provided")
df = df.map(strip)
df = df.map(resolve_number_codes)
objects = df.to_dict(orient="records")
labels = {slugify(x).replace("-", "_"): x for x in df.keys()}
df.columns = labels.keys()
editions = df.to_dict(orient="records")

print(f"fetching {INSTITUTIONS}")
df = pd.read_csv(INSTITUTIONS).head(-1)
df = df.astype("str")
df = df.replace(["nan", ""], "not provided")
objects = df.to_dict(orient="records")
labels = {slugify(x).replace("-", "_"): x for x in df.keys()}
df.columns = labels.keys()
orgs = {}
for i, x in enumerate(df.to_dict(orient="records"), start=1):
    orgs[x["institution_name"]] = x
    orgs[x["institution_name"]]["id"] = f"{i}"

editions_full = []
for i, x in enumerate(editions, start=1):
    x["id"] = f"{i}"
    x["resolver"] = f"entry-{i:03}.html"
    if i == 1:
        x["prev"] = ""
        x["next"] = f"entry-{i + 1:03}.html"
    elif i == len(editions):
        x["next"] = ""
        x["prev"] = f"entry-{i - 1:03}.html"
    else:
        x["prev"] = f"entry-{i - 1:03}.html"
        x["next"] = f"entry-{i + 1:03}.html"
    old_orgs = [x.strip() for x in x["institution_s"].split(";")]
    institutions = []
    for org in old_orgs:
        try:
            institutions.append(orgs[org])
        except KeyError:
            continue
    x["institution_s"] = institutions
    for f in FACET_FIELDS:
        try:
            x[f] = [x.strip() for x in x[f].split(";")]
        except AttributeError:
            continue
    editions_full.append(x)

with open("html/editions.json", "w") as f:
    json.dump(editions_full, f, ensure_ascii=False, indent=4)


print("Typesense Index")
print(f"defining Typesense collection schema with name: {TS_SCHEMA_NAME}")
ts_schema = make_schema(
    editions[0], "dig-ed-cat", MANDATORY_FIELDS, NO_FACET_FIELDS, NO_INDEX_FIELDS
)
with open("html/schema.json", "w") as f:
    json.dump(ts_schema, f, ensure_ascii=False, indent=4)

print(f"creating Typesnses Collection with schema {TS_SCHEMA_NAME}")
cur_schema = delete_and_create_schema(TS_CLIENT, TS_SCHEMA_NAME, ts_schema)
print(f"schema created at {cur_schema['created_at']}")
print(f"start to index {len(editions_full)} records")
index = TS_CLIENT.collections[TS_SCHEMA_NAME].documents.import_(
    editions_full, {"action": "create"}
)
print(f"status of index-process: {index[0]}")
