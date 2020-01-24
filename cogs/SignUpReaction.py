import asyncio

import discord
from discord.ext import commands

class SignUpReaction(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.signUpMessage = ''

    @commands.Cog.listener()
    async def on_reaction_add(self, react, user):
        if user == self.client.user:
            return
        if react.message.channel.name != self.client.signUpChanName:
            return
        if self.client.signUpMessage and react.message.id == self.client.signUpMessage.id:
            activeRole = discord.utils.get(react.message.guild.roles, name=self.client.activeRoleName)
            await user.add_roles(activeRole)

    @commands.Cog.listener()
    async def on_reaction_remove(self, react, user):
        if user == self.client.user:
            return
        if react.message.channel.name != self.client.signUpChanName:
            return
        ## Do not remove Active role on unreact for now
        #if react.message.id == self.client.signUpMessage.id:
        #    activeRole = discord.utils.get(react.message.guild.roles, name=self.client.activeRoleName)
        #    await user.remove_roles(activeRole)

    @commands.command(name='.start')
    async def start(self, ctx):
        if ctx.channel.name != self.client.adminBotCommandChan:
            return
        signUpChan = discord.utils.get(ctx.guild.channels, name=self.client.signUpChanName)
        players = discord.utils.get(ctx.guild.roles, name=self.client.playingRoleName)
        self.client.signUpMessage = await signUpChan.send('{} games starting in 15 minutes, react to participate !'.format(players.mention))
        await self.client.signUpMessage.add_reaction(self.client.signUpEmoji)
        # For later
        # signUpChan.send('{} next match sign up open in 15 minutes'.format(players.mention))
        #await asyncio.sleep(60*15)
        #await signUpChan.send('Please react here to play in the set !'.format(players.mention))


def setup(client):
    client.add_cog(SignUpReaction(client))
