import json
# run the shell in manage.py and IMPORT this script
path_to_file = "permissions.json"
file = json.load(open(path_to_file))

def print_meta():
    print("permissions = (")
    for perm in file["permissions"]:
        codename = perm["codename"]
        name = perm["name"]
        print(f"(\"{codename}\",\"{name}\")")
    print(")")

print_meta()