import discord
from discord.ext import commands

class SignUpReaction(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_reaction_add(self, react, user):
        if user == self.client.user:
            return
        if react.message.channel.name != self.client.signUpChanName or not self.client.signUpMessage:
            return
        if self.client.signUpMessage and react.message.id == self.client.signUpMessage.id:
            activeRole = discord.utils.get(react.message.guild.roles, name=self.client.activeRoleName)
            if not self.client.fillerMsg and len(activeRole.members) >= self.client.maxActivePlayers:
                self.client.fillerMsg = await react.message.channel.send("You can react here to be a Filler")
                await self.client.fillerMsg.add_reaction(self.client.fillerReactEmoji)
            if len(activeRole.members) >= self.client.maxActivePlayers:
                await react.message.remove_reaction(self.client.signUpEmoji, user)
                await user.send("Sorry the Active role is full for now. You can react to be a Filler")
                return
            await user.add_roles(activeRole)

    @commands.Cog.listener()
    async def on_reaction_remove(self, react, user):
        if user == self.client.user:
            return
        if react.message.channel.name != self.client.signUpChanName or not self.client.signUpMessage:
            return
        if react.message.id == self.client.signUpMessage.id:
            activeRole = discord.utils.get(react.message.guild.roles, name=self.client.activeRoleName)
            logs = discord.utils.get(react.message.guild.channels, name=self.client.logsChan)
            await logs.send('{} removed his active role'.format(user.name))
            await user.remove_roles(activeRole)

def setup(client):
    client.add_cog(SignUpReaction(client))
