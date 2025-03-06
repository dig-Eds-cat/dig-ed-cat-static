import os
import jinja2
import json
import markdown

templateLoader = jinja2.FileSystemLoader(searchpath=".")
templateEnv = jinja2.Environment(loader=templateLoader)

out_dir = "html"

with open("project.json", "r", encoding="utf-8") as f:
    project_data = json.load(f)

print("#########################")
print("building edition pages")

with open("html/data/fields.json", "r", encoding="utf-8") as fp:
    fields_list = json.load(fp)
fields = {}
for x in fields_list:
    fields[x["name"]] = x
    if "help_text" in x:
        x["help_text"] = markdown.markdown(x["help_text"])

with open("./html/data/editions.json", "r", encoding="utf-8") as f:
    data = json.load(f)

os.makedirs(out_dir, exist_ok=True)
page_template = templateEnv.get_template("./templates/dynamic/edition_page.j2")

for x in data:
    x["fields"] = []
    for key, value in fields.items():
        obj = value.copy()
        obj["value"] = x[value["name"]]
        x["fields"].append(obj)
    output_path = os.path.join("html", x["resolver"])
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(
            page_template.render({"project_data": project_data, "document_data": x})
        )

print("#########################")
print("building institution pages")

with open("./html/data/institutions.json", "r", encoding="utf-8") as f:
    data = json.load(f)

os.makedirs(out_dir, exist_ok=True)
page_template = templateEnv.get_template("./templates/dynamic/institution_page.j2")

for x in data:
    output_path = os.path.join("html", x["resolver"])
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(
            page_template.render({"project_data": project_data, "document_data": x})
        )
print("done")
