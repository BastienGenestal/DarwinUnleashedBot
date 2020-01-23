import asyncio

import discord
from discord.ext import commands

class PlayerReaction(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.playerMessage = ''

    @commands.Cog.listener()
    async def on_reaction_add(self, react, user):
        if react.message.channel.name != self.client.signUpChanName:
            return
        if self.client.playerMessage and react.message.id == self.client.playerMessage.id:
            playerRole = discord.utils.get(react.message.guild.roles, name=self.client.playingRoleName)
            await user.add_roles(playerRole)

    @commands.Cog.listener()
    async def on_reaction_remove(self, react, user):
        if user == self.client.user:
            return
        if react.message.channel.name != self.client.signUpChanName:
            return
        if react.message.id == self.client.playerMessage.id:
            playerRole = discord.utils.get(react.message.guild.roles, name=self.client.playingRoleName)
            await user.remove_roles(playerRole)

    @commands.command(name='.init')
    async def init(self, ctx):
        if ctx.channel.name != self.client.adminBotCommandChan:
            return
        signUpChan = discord.utils.get(ctx.guild.channels, name=self.client.signUpChanName)
        self.client.playerMessage = await signUpChan.send('If you are interested in getting a notification for the next set react here to become a player (:')
        await self.client.playerMessage.add_reaction(self.client.signUpEmoji)

def setup(client):
    client.add_cog(PlayerReaction(client))
