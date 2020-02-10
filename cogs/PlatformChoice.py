import discord
from discord.ext import commands


class PlatformChoice(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, event):
        if event.message_id != self.client.platformSelectionMessageId:
            return
        user = discord.utils.get(self.client.server.members, id=event.user_id)
        for idx, emoji in enumerate(self.client.platformEmojis):
            if emoji == event.emoji.name:
                platformRole = discord.utils.get(self.client.server.roles, name=self.client.platforms[idx])
                await user.add_roles(platformRole)
                return

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, event):
        if event.message_id != self.client.platformSelectionMessageId:
            return
        user = discord.utils.get(self.client.server.members, id=event.user_id)
        for idx, emoji in enumerate(self.client.platformEmojis):
            if emoji == event.emoji.name:
                platformRole = discord.utils.get(self.client.server.roles, name=self.client.platforms[idx])
                await user.remove_roles(platformRole)
                return

    @commands.command(name='.init_platform_msg')
    async def init_platform_msg(self, ctx):
        if ctx.channel.id != self.client.usefullChannels["botCommandChan"].id:
            return
        chan = self.client.usefullChannels['selectPlatformChan']
        self.platformMsg = await chan.send('Select your platform here!')
        for react in self.client.platformEmojis:
            await self.platformMsg.add_reaction(react)


def setup(client):
    client.add_cog(PlatformChoice(client))
