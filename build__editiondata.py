import json
import pandas as pd
from slugify import slugify
from utils import strip

from config import (
    EDITIONS,
    INSTITUTIONS,
    FACET_FIELDS,
)

print("hallo, lets create html/data/editionsjson.")

print(f"fetching {EDITIONS}")
df = pd.read_csv(EDITIONS)
df = df.astype("str")
df = df.replace(["nan", ""], "not provided")
df.to_csv("html/data/editions.csv", index=False)
df = df.map(strip)
objects = df.to_dict(orient="records")
labels = {slugify(x).replace("-", "_"): x for x in df.keys()}
df.columns = labels.keys()
editions = df.to_dict(orient="records")

print(f"fetching {INSTITUTIONS}")
df = pd.read_csv(INSTITUTIONS)
df = df.astype("str")
df = df.replace(["nan", ""], "not provided")
objects = df.to_dict(orient="records")
labels = {slugify(x).replace("-", "_"): x for x in df.keys()}
df.columns = labels.keys()
orgs = {}
institutions = df.to_dict(orient="records")
for i, x in enumerate(institutions, start=0):
    cur_id = int(x["id"])
    orgs[x["institution_name"]] = x
    orgs[x["institution_name"]]["resolver"] = f"institution-{cur_id:03}.html"
    x["next"] = ""
    x["prev"] = ""
    try:
        next_id = institutions[i + 1]["id"]
        x["next"] = f"institution-{int(next_id):03}.html"
    except IndexError:
        next_id = institutions[0]["id"]
        x["next"] = ""
    if i > 1:
        prev_id = institutions[i - 1]["id"]
        x["prev"] = f"institution-{int(prev_id):03}.html"

editions_full = []
for i, x in enumerate(editions, start=0):
    cur_id = int(x["id"])
    x["next"] = ""
    x["resolver"] = f"entry-{int(cur_id):03}.html"
    try:
        next_id = editions[i + 1]["id"]
        x["next"] = f"entry-{int(next_id):03}.html"
    except IndexError:
        next_id = editions[0]["id"]
        x["next"] = f"entry-{int(next_id):03}.html"
    prev_id = editions[i - 1]["id"]
    x["prev"] = f"entry-{int(prev_id):03}.html"

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
