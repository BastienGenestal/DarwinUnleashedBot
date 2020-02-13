import discord
from discord.ext import commands


class RegionChoice(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, event):
        if event.message_id != self.client.regionSelectionMessageId:
            return
        guild = discord.utils.get(self.client.guilds, id=event.guild_id)
        user = discord.utils.get(guild.members, id=event.user_id)
        for idx, emoji in enumerate(self.client.regionEmojis):
            if emoji == event.emoji.name:
                regionRole = discord.utils.get(guild.roles, name=self.client.regions[idx])
                await user.add_roles(regionRole)
                return

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, event):
        if event.message_id != self.client.regionSelectionMessageId:
            return
        guild = discord.utils.get(self.client.guilds, id=event.guild_id)
        user = discord.utils.get(guild.members, id=event.user_id)
        for idx, emoji in enumerate(self.client.regionEmojis):
            if emoji == event.emoji.name:
                regionRole = discord.utils.get(guild.roles, name=self.client.regions[idx])
                await user.remove_roles(regionRole)
                return

    @commands.command(name='.init_region_msg')
    async def init_region_msg(self, ctx):
        if ctx.channel.id != self.client.usefulChannels["botCommandChan"].id:
            return
        chan = self.client.usefulChannels["selectRegionChan"]
        self.regionMsg = await chan.send('Select your region here!')
        for react in self.client.regionEmojis:
            await self.regionMsg.add_reaction(react)


def setup(client):
    client.add_cog(RegionChoice(client))
