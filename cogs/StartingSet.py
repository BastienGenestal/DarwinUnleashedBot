import asyncio
import discord
from discord.ext import commands

class DefaultCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.signUpCmdMsg = None

    @commands.Cog.listener()
    async def on_reaction_add(self, react, user):
        if user == self.client.user or not self.signUpCmdMsg:
            return
        if react.message.id == self.signUpCmdMsg.id:
            organizingRole = discord.utils.get(react.message.guild.roles, name=self.client.organizingRoleName)
            await user.add_roles(organizingRole)

    @commands.Cog.listener()
    async def on_reaction_remove(self, react, user):
        if user == self.client.user or not self.signUpCmdMsg:
            return
        if react.message.id == self.signUpCmdMsg.id:
            organizingRole = discord.utils.get(react.message.guild.roles, name=self.client.organizingRoleName)
            await user.remove_roles(organizingRole)


    @commands.command(name='.start')
    async def start(self, ctx):
        if ctx.channel.name != self.client.adminBotCommandChan:
            return
        self.signUpCmdMsg = ctx.message
        await self.signUpCmdMsg.add_reaction(self.client.signUpEmoji)
        signUpChan = discord.utils.get(ctx.guild.channels, name=self.client.signUpChanName)
        players = discord.utils.get(ctx.guild.roles, name=self.client.playingRoleName)
        #self.client.signUpMessage = await signUpChan.send(
        #    '{} games starting in 15 minutes, react to participate !'.format(players.mention))
        #await self.client.signUpMessage.add_reaction(self.client.signUpEmoji)
        temp = await signUpChan.send('{} Sign up for the next set in 15 minutes!\nBe quick or you might miss it :wink:'.format(players.mention))
        await asyncio.sleep(60)#*15)
        await temp.delete()
        self.client.signUpMessage = await signUpChan.send('Please react here to play in the set !'.format(players.mention))
        await self.client.signUpMessage.add_reaction(self.client.signUpEmoji)


def setup(client):
    client.add_cog(DefaultCog(client))
