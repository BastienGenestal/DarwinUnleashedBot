import discord
from discord.ext import commands


class PlayerReaction(commands.Cog):
    def __init__(self, client):
        self.client = client

    def getTheRightChannelAndRightMessage(self, guild, event):
        signUpChan = discord.utils.get(guild.channels, name=self.client.signUpChanName)
        return event.channel_id != signUpChan.id or event.message_id != self.client.medKitToPlayerMessageId

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, event):
        guild = discord.utils.get(self.client.guilds, id=event.guild_id)
        if self.getTheRightChannelAndRightMessage(guild, event):
            return
        playerRole = discord.utils.get(guild.roles, name=self.client.playingRoleName)
        user = discord.utils.get(guild.members, id=event.user_id)
        await user.add_roles(playerRole)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, event):
        guild = discord.utils.get(self.client.guilds, id=event.guild_id)
        if self.getTheRightChannelAndRightMessage(guild, event):
            return
        playerRole = discord.utils.get(guild.roles, name=self.client.playingRoleName)
        user = discord.utils.get(guild.members, id=event.user_id)
        await user.remove_roles(playerRole)

    @commands.command(name='.init')
    async def init(self, ctx):
        if ctx.channel.name != self.client.botCommandChan:
            return
        signUpChan = discord.utils.get(ctx.guild.channels, name=self.client.signUpChanName)
        playerMessage = await signUpChan.send(
            'If you are interested in getting a notification for the next set react here to become a player (:')
        await playerMessage.add_reaction(self.client.signUpEmoji)


def setup(client):
    client.add_cog(PlayerReaction(client))
