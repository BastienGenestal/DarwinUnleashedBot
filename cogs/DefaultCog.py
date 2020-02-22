from discord.ext import commands


class DefaultCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot Ready')

    @commands.command(name='.ping')
    async def ping(self, ctx):
        await ctx.channel.send("pong")

def setup(client):
    client.add_cog(DefaultCog(client))
