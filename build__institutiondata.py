import json

print("gathering institution data")
with open("html/editions.json", "r") as f:
    data = json.load(f)

institutions = {}
for x in data:
    for y in x["institution_s"]:
        y["editions"] = []
        institutions[y["id"]] = y

for x in data:
    for y in x["institution_s"]:
        inst_id = y["id"]
        institutions[inst_id]["resolver"] = f"institution-{int(inst_id):03}.html"
        institutions[inst_id]["editions"].append(
            {"edition_name": x["edition_name"], "edition_resolver": x["resolver"]}
        )

with open("./html/institutions.json", "w", encoding="utf-8") as f:
    json.dump(
        [value for _, value in institutions.items()], f, ensure_ascii=False, indent=4
    )
