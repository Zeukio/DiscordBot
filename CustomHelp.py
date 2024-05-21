from typing import Mapping, Optional, List, Any

import discord
from discord.ext import commands
from discord.ext.commands import Cog, Command, Group


class CustomHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping: Mapping[Optional[Cog], List[Command[Any, ..., Any]]], /) -> None:
        embed = discord.Embed(title="Help")
        for cog, commands in mapping.items():
            command_signatures = [self.get_command_signature(c) for c in commands]
            if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)
        return

    async def send_cog_help(self, cog: Cog, /) -> None:
        return await super().send_cog_help(cog)

    async def send_group_help(self, group: Group[Any, ..., Any], /) -> None:
        return await super().send_group_help(group)

    async def send_command_help(self, command: Command[Any, ..., Any], /) -> None:
        return await super().send_command_help(command)