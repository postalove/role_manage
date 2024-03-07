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
from interactions import Task,IntervalTrigger
from datetime import datetime, timedelta
import asyncio
import os
# Use the following method to import the internal module in the current same directory
from . import load_constant
from . import jail_info
'''
Replace the ModuleName with any name you'd like
'''
class RoleManager(interactions.Extension):
    module_base: interactions.SlashCommand = interactions.SlashCommand(
        name="judge",
        description="法官"
    )
    '''module_group: interactions.SlashCommand = module_base.group(
        name="can",
        description="Replace here for the group command descriptions"
    )'''

    
    
    @module_base.subcommand("jail", sub_cmd_description="关押囚犯")
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
    min_value=0,
    max_value=5000
    )   
    @interactions.slash_option(
    name="hours",
    description='hours',
    opt_type=interactions.OptionType.INTEGER,
    min_value=0,
    max_value=5000
    )   
    @interactions.slash_option(
    name="minutes",
    description='minutes',
    opt_type=interactions.OptionType.INTEGER,
    min_value=0,
    max_value=5000
    )
    async def jail_member(self, ctx: interactions.SlashContext, member:interactions.Member,days: int = 0, hours: int = 0, minutes: int = 0):
        await ctx.defer()
        c, allowed_roles, log_channel_id,guild_id = load_constant.extract_bot_setup(f'{os.path.dirname(__file__)}/bot_setup.json')
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
        if not self.check_jailed_member.running :
                self.check_jailed_member.start()
    

    
    @Task.create(IntervalTrigger(seconds=5))
    async def check_jailed_member(self):
        c, allowed_roles, log_channel_id,guild_id = load_constant.extract_bot_setup(f'{os.path.dirname(__file__)}/bot_setup.json')
        guild=self.bot.get_guild(guild_id)
        
        jailed_members = jail_info.load_jailed_members()

        if not jailed_members:
                return
        
        for member_id, info in list(jailed_members.items()):
            release_time = datetime.fromisoformat(info["release_time"])
            if datetime.utcnow() >= release_time:
                
                member = guild.get_member(int(member_id))

                if member is not None:
                    prisoner = interactions.utils.get(guild.roles, name='囚犯')
                    citizen = interactions.utils.get(guild.roles, name='正式成员')
                    await member.remove_role(prisoner)
                    await member.add_role(citizen)

                    del jailed_members[member_id]
                    jail_info.save_jailed_members(jailed_members)

    @module_base.subcommand(sub_cmd_name='start',sub_cmd_description='开始检查囚犯')
    async def start_checking_jailed_members(self,ctx:interactions.SlashContext):
        tech = interactions.utils.get(ctx.guild.roles, name='技术公务员')
        if tech not in ctx.author.roles:
            ctx.send('你无权这么做!')
            return
        if not self.check_jailed_member.running :
            self.check_jailed_member.start()
            await ctx.send('自动释放囚犯程序已启动')
            return
        else:
            await ctx.send('已启动自动释放囚犯!')

    @interactions.listen(interactions.api.events.MessageCreate)
    async def auto_check_jailed_member(self,event:interactions.api.events.MessageCreate):
         if not self.check_jailed_member.running:
              self.check_jailed_member.start()

    @module_base.subcommand("release", sub_cmd_description="手动释放囚犯")
    @interactions.slash_option(
        name = "member",
        description='member you want to release',
        required = True,
        opt_type = interactions.OptionType.USER
        )
    async def release(self,ctx: interactions.SlashContext, member:interactions.Member):
        c, allowed_roles, log_channel_id,guild_id = load_constant.extract_bot_setup(f'{os.path.dirname(__file__)}/bot_setup.json')
        if any(role.name in allowed_roles for role in ctx.author.roles):
            prisoner= interactions.utils.get(ctx.guild.roles,name = '囚犯')
            citizen = interactions.utils.get(ctx.guild.roles,name = '正式成员')
            if prisoner is None:
                    await ctx.send("Role '囚犯' not found. Please create the role first.")
                    return

        

            # Remove jailed member info from the file
            jailed_members = jail_info.load_jailed_members()
            if str(member.id) in jailed_members:
                del jailed_members[str(member.id)]
                jail_info.save_jailed_members(jailed_members)
                await member.remove_role(prisoner)
                await member.add_role(citizen)
                await ctx.send(f"{member.mention} has been manually released from jail.")
                log_channel = ctx.guild.get_channel(log_channel_id)
                embed = interactions.Embed(
        title=f"",
        description=f"{ctx.user.mention} released {member.mention}",
        color=0x00FF00
    )
                await log_channel.send(embed=embed)
            elif prisoner not in member.roles:
                await ctx.send(f"{member.display_name} is not a prisoner.")
            else:
                await member.remove_role(prisoner)
                await member.add_role(citizen)
                await ctx.send(f"{member.mention} has been manually released from jail.")

        else:
            await ctx.send('你无权这么做!')
        
