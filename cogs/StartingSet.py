import discord
from discord.ext import commands

from const_messages import START_A_SET_MSG, SIGN_UP_HERE_MSG


class StartingSet(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.startASetMsg = None

    @staticmethod
    async def sendStartMessage(client):
        return await client.usefullChannels['startASetChan'].send(
            START_A_SET_MSG.format(client.usefullCustomEmotes['unleashed'],
                                   client.usefullCustomEmotes['unleashed'],
                                   client.usefullBasicEmotes['signUpWinner'],
                                   client.usefullBasicEmotes['signUpNoWinner']
                                   ))

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.usefullChannels['startASetChan'].purge()
        self.client.startASetMsg = await self.sendStartMessage(self.client)
        await self.client.startASetMsg.add_reaction(self.client.usefullBasicEmotes['signUpWinner'])
        await self.client.startASetMsg.add_reaction(self.client.usefullBasicEmotes['signUpNoWinner'])

    @staticmethod
    async def start_cmd_error(ctx):
        await ctx.channel.send("```Please use .start [X]\n\tX\tMinutes before the sign up message```")

def setup(client):
    client.add_cog(StartingSet(client))
