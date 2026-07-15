import json
import sys
import copy

# Ensure the required arguments were provided
if len(sys.argv) < 4:
    print("Error: Missing arguments. Usage: build_static_assets.py <target_dir> <version> <is_latest>", file=sys.stderr)
    sys.exit(1)

target_dir = sys.argv[1]
version = sys.argv[2]
is_latest = sys.argv[3].lower() == "true"

# Patch the versioned search.json
versioned_search_path = f"{target_dir}/{version}/search.json"
with open(versioned_search_path, "r") as f:
    versioned_search_data = json.load(f)

for i, entry in enumerate(versioned_search_data["items"]):
    location = entry["location"]
    if location.startswith("changelog/") or location == "changelog":
        versioned_search_data["items"][i]["location"] = "../" + location

with open(versioned_search_path, "w") as f:
    json.dump(versioned_search_data, f)

print(f"Patched {versioned_search_path}")

# Build root static assets (only for latest version deploys)
if not is_latest:
    print("Not the latest version — skipping search-404.json and versions-404.json.")
    sys.exit(0)

with open("./docs/versions.json", "r") as f:
    version_data = json.load(f)

# Re-read the now-patched versioned search.json to use as the base for search-404.json and search-changelog.json.
with open(versioned_search_path, "r") as f:
    search_data = json.load(f)
    changelog_search_data = copy.deepcopy(search_data)

# Build search-404.json.
for i, entry in enumerate(search_data["items"]):
    location = entry["location"]
    # Rewrite URLs as absolute paths.
    if location.startswith("../changelog/") or location == "../changelog":
        relative = location[len("../"):]  # strip leading "../"
        search_data["items"][i]["location"] = f"/pygame-topdownengine/{relative}"
    else:
        search_data["items"][i]["location"] = f"/pygame-topdownengine/{version}/{location}"

with open(f"{target_dir}/search-404.json", "w") as f:
    json.dump(search_data, f)

print(f"Written {target_dir}/search-404.json")

# Build search-changelog.json.
for i, entry in enumerate(changelog_search_data["items"]):
    location = entry["location"]
    # Rewrite URLs so that changelog search links dont have /pygame-topdownengine/ twice.
    if location.startswith("../changelog/") or location == "../changelog":
        relative = location[len("../"):]  # strip leading "../"
        changelog_search_data["items"][i]["location"] = f"{relative}"
    else:
        changelog_search_data["items"][i]["location"] = f"{version}/{location}"

with open(f"{target_dir}/search-changelog.json", "w") as f:
    json.dump(changelog_search_data, f)

print(f"Written {target_dir}/search-changelog.json")

# Build versions-404.json.
for i, v in enumerate(version_data):
    version_data[i]["version"] = "pygame-topdownengine/" + v["version"]

with open(f"{target_dir}/versions-404.json", "w") as f:
    json.dump(version_data, f)

print(f"Written {target_dir}/versions-404.json")