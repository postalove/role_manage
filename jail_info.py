import json
jail_file = "jailed_members.json"
def load_jailed_members():
    try:
        with open(jail_file, 'w') as f:
            return json.load(f)
    except FileNotFoundError:
        print('file not found!')
        return {}

# Save jailed members to the file
def save_jailed_members(jailed_members):
    with open(jail_file, 'w') as f:
        json.dump(jailed_members, f, indent=2)