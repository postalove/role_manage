import json
import os
 
def load_jailed_members():
    try:
        with open(f'{os.path.dirname(__file__)}/jailed_members.json', 'w+') as f:
            return json.load(f)
    except FileNotFoundError:
        print('file not found!')
        return {}

# Save jailed members to the file
def save_jailed_members(jailed_members):
    with open(f'{os.path.dirname(__file__)}/jailed_members.json', 'w+') as f:
        json.dump(jailed_members, f, indent=2)