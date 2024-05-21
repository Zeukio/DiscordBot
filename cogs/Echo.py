import discord
from discord.ext import commands
class Echo(commands.Cog):
    #echo
    def __init__(self,client):

        self.client = client
    @commands.command()
    async def echo(self, ctx):
        ctx.send('Echo test')

async def setup(client):
    await client.add_cog(Echo(client))