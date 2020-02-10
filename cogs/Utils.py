import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound


class Utils(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            return
        raise error

    @commands.Cog.listener()
    async def on_member_join(self, member):
        role = discord.utils.get(member.guild.roles, name=self.client.medKitRoleName)
        await member.add_roles(role)

    @commands.command(name='.refresh_players')
    async def refresh_players(self, ctx):
        signUpChan = discord.utils.get(ctx.guild.text_channels, name=self.client.signUpChanName)
        playerRole = discord.utils.get(ctx.guild.roles, name=self.client.playingRoleName)
        msg = await signUpChan.fetch_message(self.client.medKitToPlayerMessageId)
        reaction = discord.utils.get(msg.reactions, emoji=self.client.signUpEmoji)
        async for user in reaction.users():
            if playerRole not in user.roles:
                await user.add_roles(playerRole)

    @commands.command(name='.clear')
    async def clear(self, ctx):
        if ctx.channel.name != self.client.adminBotCommandChan:
            return
        await ctx.channel.purge(limit=200)

def setup(client):
    client.add_cog(Utils(client))
