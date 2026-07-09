import sys
import json

def verify_latest_alias(target_version):
    try:
        with open("docs-versions.json", 'r') as f:
            data = json.load(f)
        
        for version in data:
            if version["version"] != target_version:
                continue

            if "latest" in version["aliases"]:
                return True
                
        return False
    except Exception:
        return False

# Ensure the version argument was provided
if len(sys.argv) < 2:
    print("Error: Missing argument. Usage: check_latest.py <version>", file=sys.stderr)
    sys.exit(1)

version_arg = sys.argv[1]

if verify_latest_alias(version_arg):
    sys.exit(0) # True
else:
    sys.exit(1) # False