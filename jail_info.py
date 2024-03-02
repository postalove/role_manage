import json
import os
 
def load_jailed_members():
    filename = f'{os.path.dirname(__file__)}/jailed_members.json'
    with open(filename, 'w+') as f:
        return json.load(f)


# Save jailed members to the file
def save_jailed_members(jailed_members):
    with open(f'{os.path.dirname(__file__)}/jailed_members.json', 'w') as f:
        json.dump(jailed_members, f, indent=2)
