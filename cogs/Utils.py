import discord
from discord.ext import commands

class Utils(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot Ready')

    @commands.command(name='.clear')
    async def clear(self, ctx):
        async for message in ctx.channel.history(limit=200):
            await message.delete()

def setup(client):
    client.add_cog(Utils(client))
