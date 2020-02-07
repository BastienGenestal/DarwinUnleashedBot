import discord
from discord.ext import commands
from const import UsefullChannelNames

class Prep(commands.Cog):
    def __init__(self, client):
        self.client = client


    async def init_server(self):
        server = discord.utils.get(self.client.guilds, id=self.client.ServerId)
        if not server:
            raise self.client.MissingSomething("Discord server not found")
        self.client.server = server

    async def init_channels(self):
        for (var, chanName) in UsefullChannelNames:
            channel = discord.utils.get(self.client.server.channels, name=chanName)
            if not channel:
                raise self.client.MissingSomething("{} channel is missing".format(chanName))
            self.client.usefullChannels[var] = channel

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            await self.init_server()
            await self.init_channels()
        except self.client.MissingSomething as e:
            print(e)
            print("The bot will shut down, please check the discord server for whatever is missing.")
            exit(84)



    @commands.command(name='.prep')
    async def prep(self, ctx):
        await ctx.channel.send("pong")


def setup(client):
    client.add_cog(Prep(client))
