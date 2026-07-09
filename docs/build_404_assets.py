import json
import sys

# Ensure the target dir argument was provided
if len(sys.argv) < 2:
    print("Error: Missing argument. Usage: build_404_assets.py <target_dir>", file=sys.stderr)
    sys.exit(1)

target_dir = sys.argv[1]

with open("./docs/versions.json", "r") as f:
    version_data = json.load(f)

with open(f"{target_dir}/search.json", "r") as f:
    search_data = json.load(f)

# Build new version data
for i, version in enumerate(version_data):
    version_data[i]["version"] = "pygame-topdownengine/" + version["version"]

# Build new search data
for i, entry in enumerate(search_data["items"]):
    search_data["items"][i]["location"] = "pygame-topdownengine/latest/" + entry["location"]

with open(f"{target_dir}/search-404.json", "w") as f:
    json.dump(search_data, f)

with open(f"{target_dir}/versions-404.json", "w") as f:
    json.dump(version_data, f)