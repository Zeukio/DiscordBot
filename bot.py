import sys
sys.path.append("./cogs")
from inspect import getmembers, isfunction
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from typing import Final
import time

import CustomHelp





def run_discrod_bot():
    #loaf tonkens
    load_dotenv()
    TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')


    #setup discord bot
    intents = discord.Intents.default()
    intents.message_content = True  # NOQA
    client = commands.Bot(command_prefix = '.' ,intents = intents ) #, help_command= CustomHelp.CustomHelpCommand())


    #events
    @client.event
    async def on_ready():
        print(f'{client.user} is now running')
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                print(f'{filename}')
                if filename[:-3] != "__init__":
                    await client.load_extension(f'cogs.{filename[:-3]}')


    @client.command(help="Load Cog")
    async def load(ctx,extension):
        if '284146826196549633' == str(ctx.message.author.id):
            await client.load_extension(f'cogs.{extension}')
            await ctx.send(f'{extension} load')

    @client.command(help="Unload Cog")
    async def unload(ctx, extension):
        if '284146826196549633' == str(ctx.message.author.id):
            await client.unload_extension(f'cogs.{extension}')
            await ctx.send(f'{extension} unload')

    @client.command(help="Update Cog")
    async def updatecog(ctx, extension):
        if '284146826196549633' == str(ctx.message.author.id):
            await ctx.send(f'{extension} start update ... ')
            await client.unload_extension(f'cogs.{extension}')
            time.sleep(5)
            await client.load_extension(f'cogs.{extension}')
            await ctx.send(f'{extension} finish update')

    @client.command(help="Download cog")
    async def downloadcog(ctx):
        if '284146826196549633' == str(ctx.message.author.id):
            if len(ctx.message.attachments) > 0:
                ctx.send(f' new cog ... ')
                for attachment in ctx.message.attachments:
                    if ".py" in attachment.filename:
                        fl = attachment.filename[:-3]
                        await ctx.send(f'{attachment.filename} download ... ')
                        await attachment.save(f'./cogs/{attachment.filename}')
                        await ctx.send(f'{attachment.filename} downloaded ... ')
                        newmodule = __import__(fl)
                        functionsinnewmodule = getmembers(newmodule, isfunction)
                        funcnames = []
                        for func in functionsinnewmodule:
                            funcnames.append(str(func[0]))

                        if "setup" in funcnames:
                            await ctx.send(funcnames)
                        else:
                            await ctx.send(funcnames)
                            await ctx.send("error in module... it will be deleted")
                            os.remove(f'./cogs/{attachment.filename}')





    @client.command(help="List all Cogs")
    async def coglist(ctx):
        if '284146826196549633' == str(ctx.message.author.id):
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    await ctx.send(f'{filename}')

    @client.command(help="Send a Private Hello")
    async def private(ctx):
        await ctx.author.send(f'Hello! {ctx.message.author.name}')




    client.run(TOKEN)


