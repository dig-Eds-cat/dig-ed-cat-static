import json
import pandas as pd
from slugify import slugify
from utils import resolve_number_codes, strip

from config import (
    EDITIONS,
    INSTITUTIONS,
    FACET_FIELDS,
)

print("hallo, lets create html/data/editionsjson.")

print(f"fetching {EDITIONS}")
df = pd.read_csv(EDITIONS).head(-1)
df = df.astype("str")
df = df.replace(["nan", ""], "not provided")
df.to_csv("html/data/editions.csv", index=False)
df = df.map(strip)
df = df.map(resolve_number_codes)
df.to_csv("html/data/editions_decoded.csv", index=False)
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
    orgs[x["institution_name"]]["resolver"] = f"institution-{i:03}.html"

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

with open("html/data/editions.json", "w") as f:
    json.dump(editions_full, f, ensure_ascii=False, indent=4)
