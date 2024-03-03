import json
from json.decoder import JSONDecodeError
import os
import aiofiles
import asyncio
 
async def load_jailed_members():
    try:
        async with aiofiles.open(f'{os.path.dirname(__file__)}/jailed_members.json', 'r') as f:
            temp_str: str = await f.read()
            ret_str: str = json.loads(temp_str)
            return ret_str
    except FileNotFoundError or JSONDecodeError: #这里注意要有针对空字符串的错误handle
        return {}


# Save jailed members to the file
async def save_jailed_members(jailed_members):
    async with aiofiles.open(f'{os.path.dirname(__file__)}/jailed_members.json', 'w') as f:
        temp_str: str = json.dumps(jailed_members, indent=2)
        await f.write(temp_str)