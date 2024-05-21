import discord
from discord.ext import commands
import responses
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


