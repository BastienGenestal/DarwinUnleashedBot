import discord
from discord.ext import commands


class FillerReaction(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_reaction_add(self, react, user):
        if user == self.client.user:
            return
        if react.message.channel.name != self.client.signUpChanName:
            return
        if self.client.fillerMsg and react.message.id == self.client.fillerMsg.id:
            activeRole = discord.utils.get(react.message.guild.roles, name=self.client.activeRoleName)
            fillerRole = discord.utils.get(react.message.guild.roles, name=self.client.fillerRoleName)
            for member in activeRole.members:
                if member.id == user.id:
                    await react.message.remove_reaction(self.client.fillerReactEmoji, user)
                    await user.send("You can not be Active and Filler")
                    return
            await user.add_roles(fillerRole)

    @commands.Cog.listener()
    async def on_reaction_remove(self, react, user):
        if user == self.client.user:
            return
        if react.message.channel.name != self.client.signUpChanName:
            return
        if self.client.fillerMsg and react.message.id == self.client.fillerMsg.id:
            fillerRole = discord.utils.get(react.message.guild.roles, name=self.client.fillerRoleName)
            await user.remove_roles(fillerRole)


def setup(client):
    client.add_cog(FillerReaction(client))
