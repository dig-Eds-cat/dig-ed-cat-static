import json

print("gathering institution data")
with open("html/data/editions.json", "r") as f:
    data = json.load(f)

institutions = {}
for x in data:
    for y in x["institution_s"]:
        y["editions"] = []
        institutions[y["id"]] = y

for x in data:
    for y in x["institution_s"]:
        inst_id = y["id"]
        institutions[inst_id]["editions"].append(
            {"edition_name": x["edition_name"], "edition_resolver": x["resolver"]}
        )
for key, value in institutions.items():
    value["edition_counter"] = f"{len(value['editions'])}"

with open("./html/data/institutions.json", "w", encoding="utf-8") as f:
    json.dump(
        [value for _, value in institutions.items()], f, ensure_ascii=False, indent=4
    )
