import discord
from discord.ext import commands


class SignUpReaction(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_reaction_add(self, react, user):
        if user == self.client.user:
            return
        if react.message.channel.id != self.client.usefullChannels["signUpChan"].id or not self.client.signUpMessage:
            return
        if self.client.signUpMessage and react.message.id == self.client.signUpMessage.id:
            activeRole = self.client.usefullRoles['activeRole']
            await user.add_roles(activeRole)

    @commands.Cog.listener()
    async def on_reaction_remove(self, react, user):
        if user == self.client.user:
            return
        if react.message.channel.id != self.client.usefullChannels["signUpChan"].id or not self.client.signUpMessage:
            return
        if react.message.id == self.client.signUpMessage.id:
            activeRole = self.client.usefullRoles['activeRole']
            logs = self.client.usefullChannels['logsChan']
            await logs.send('{} removed his active role'.format(user.name))
            await user.remove_roles(activeRole)


def setup(client):
    client.add_cog(SignUpReaction(client))
