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
            await user.add_roles(activeRole)

    @commands.Cog.listener()
    async def on_reaction_remove(self, react, user):
        if user == self.client.user:
            return
        if react.message.channel.name != self.client.signUpChanName or not self.client.signUpMessage:
            return
        if react.message.id == self.client.signUpMessage.id:
            activeRole = discord.utils.get(react.message.guild.roles, name=self.client.activeRoleName)
            logs = discord.utils.get(react.message.guild.channels, name=self.client.logsChanName)
            await logs.send('{} removed his active role'.format(user.name))
            await user.remove_roles(activeRole)


def setup(client):
    client.add_cog(SignUpReaction(client))
