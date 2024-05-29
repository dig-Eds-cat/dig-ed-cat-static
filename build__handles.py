import json
import os
from acdh_handle_pyutils.client import HandleClient

BASE_URL = "https://dig-ed-cat.acdh.oeaw.ac.at/"
with open("html/editions.json", "r") as f:
    data = json.load(f)
client = HandleClient(
    os.environ.get("HANDLE_USERNAME"), os.environ.get("HANDLE_PASSWORD")
)
UPDATE = os.environ.get("UPDATE_HANDLES", False)

if UPDATE:
    print("Update existing handles and create missing ones")
else:
    print("check for missing handles and create if needed")

for x in data:
    handle = False
    new_url = f"{BASE_URL}{x['resolver']}"
    try:
        handle = x["handle_pid"]
    except KeyError:
        pass
    if handle and UPDATE:
        r = client.update_handle(handle, new_url)
        print(r)
    if not handle:
        new_handle = client.register_handle(new_url, full_url=False)
        x["handle_pid"] = new_handle

with open("html/editions.json", "w") as f:
    data = json.dump(data, f, ensure_ascii=True, indent=4)
