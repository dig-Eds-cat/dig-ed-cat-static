import os
import jinja2
import json

templateLoader = jinja2.FileSystemLoader(searchpath=".")
templateEnv = jinja2.Environment(loader=templateLoader)

out_dir = "html"

with open("project.json", "r", encoding="utf-8") as f:
    project_data = json.load(f)

with open("./html/editions.json", "r", encoding="utf-8") as f:
    data = json.load(f)


os.makedirs(out_dir, exist_ok=True)
page_template = templateEnv.get_template("./templates/dynamic/edition_page.j2")
# browse_template = templateEnv.get_template("./templates/dynamic/browse.j2")

# print("render browse.html")
# output_path = os.path.join("html", "browse.html")
# with open(output_path, "w", encoding="utf-8") as f:
#     f.write(browse_template.render({"project_data": project_data, "browse_data": data}))


print("building document und page pages")
for x in data:
    output_path = os.path.join("html", x["resolver"])
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(
            page_template.render({"project_data": project_data, "document_data": x})
        )
