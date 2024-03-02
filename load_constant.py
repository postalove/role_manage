'''
Copyright (C) 2024  __retr0.init__

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''

import json
import os
censor_roles=['入群审核员']
allowed_roles = ["典狱长", "议员","法官"]
log_channel_id=1166627731916734504
guild_id = 1150630510696075404

data = {
    "censor_roles": censor_roles,
    "allowed_roles": allowed_roles,
    "log_channel_id": log_channel_id,
    "guild_id" : guild_id
}

with open(f'{os.path.dirname(__file__)}/bot_setup.json', "w") as file:
    json.dump(data, file)

def extract_bot_setup(filename):
    with open(filename, "r") as file:
        data = json.load(file)
        censor_roles = data.get("censor_roles", [])
        allowed_roles = data.get("allowed_roles", [])
        log_channel_id = data.get("log_channel_id", None)
        guild_id = data.get("guild_id",None)
        return censor_roles, allowed_roles, log_channel_id,guild_id
