'''
Discord-Bot-Module template. For detailed usages,
 check https://interactions-py.github.io/interactions.py/

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
import interactions
from datetime import datetime, timedelta
import asyncio
# Use the following method to import the internal module in the current same directory
from . import load_constant
from . import jail_info
'''
Replace the ModuleName with any name you'd like
'''
class RoleManager(interactions.Extension):
    module_base: interactions.SlashCommand = interactions.SlashCommand(
        name="judge_role",
        description="Replace here for the base command descriptions"
    )
    module_group: interactions.SlashCommand = module_base.group(
        name="can",
        description="Replace here for the group command descriptions"
    )

    
    
    @module_group.subcommand("jail_member", sub_cmd_description="关押囚犯")
    @interactions.slash_option(
        name = "member",
        description='member you want to jail',
        required = True,
        opt_type = interactions.OptionType.USER
    )
    @interactions.slash_option(
    name="days",
    description='days',
    opt_type=interactions.OptionType.INTEGER,
    min_value=0
    )   
    @interactions.slash_option(
    name="hours",
    description='hours',
    opt_type=interactions.OptionType.INTEGER,
    min_value=0
    )   
    @interactions.slash_option(
    name="minutes",
    description='minutes',
    opt_type=interactions.OptionType.INTEGER,
    min_value=0
    )
    async def jail_member(self, ctx: interactions.SlashContext, member:interactions.Member,days: int = 0, hours: int = 0, minutes: int = 0):
        c, allowed_roles, log_channel_id,guild_id = load_constant.extract_bot_setup("bot_setup.json")
        if any(role.name in allowed_roles for role in ctx.author.roles):
            prisoner= interactions.utils.get(ctx.guild.roles,name = '囚犯')
            citizen = interactions.utils.get(ctx.guild.roles,name = '正式成员')
            voter = interactions.utils.get(ctx.guild.roles,name = '选民')
            if prisoner is None:
                await ctx.send("请创建囚犯身份组!")
                return
            duration_minutes = days * 24 * 60 + hours * 60 + minutes

            await member.add_role(prisoner)
            await member.remove_role(citizen)
            await member.remove_role(voter)
            
            jailed_members = jail_info.load_jailed_members()
            release_time = datetime.utcnow() + timedelta(minutes=duration_minutes)
            jailed_members[str(member.id)] = {"release_time": release_time.isoformat()}
            jail_info.save_jailed_members(jailed_members)
            await ctx.send(f"{member.mention} has been jailed for {days} days, {hours} hours, and {minutes} minutes.")
            log_channel = ctx.guild.get_channel(log_channel_id)
            embed = interactions.Embed(
        title=f"",
        description=f"{ctx.user.mention} jailed {member.mention} for {days} days, {hours} hours, and {minutes} minutes.",
        color=0xFF0000  # Replace with your desired color (red in this example)
    )

            await log_channel.send(embed=embed)
        else:
            await ctx.send('你无权这么做!')
    
    @interactions.listen(interactions.api.events.Startup)
    async def check_jailed_member():
        c, allowed_roles, log_channel_id,guild_id = load_constant.extract_bot_setup("bot_setup.json")
        guild= await interactions.Client.get_guild(guild_id)
        while True:
            jailed_members = jail_info.load_jailed_members()

            if not jailed_members:
                # The jailed_members dictionary is empty, no need to iterate
                await asyncio.sleep(5)
                continue

            for member_id, info in list(jailed_members.items()):
                release_time = datetime.fromisoformat(info["release_time"])
                if datetime.utcnow() >= release_time:
                    
                    

                        # Check if the guild is not None
                    if member_id is not None:
                        member = guild.get_member(int(member_id))

                        if member is not None:
                            prisoner = interactions.utils.get(guild.roles, name='囚犯')
                            citizen = interactions.utils.get(guild.roles, name='正式成员')
                            await member.remove_role(prisoner)
                            await member.add_role(citizen)

                        del jailed_members[member_id]
                        jail_info.save_jailed_members(jailed_members)

            await asyncio.sleep(5) # Check every 60 seconds
