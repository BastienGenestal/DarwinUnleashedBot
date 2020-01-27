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

    def getOneConstLine(self, variableName, value):
        return '\t\t{} = {}\n'.format(variableName, value)

    @commands.command(name='.help')
    async def help(self, ctx):
        if ctx.channel.name != self.client.adminBotCommandChan:
            return
        msg = "```Constants variables:\n"
        msg += self.getOneConstLine("minutesToChoseAClass", self.client.minutesToChoseAClass)
        msg += self.getOneConstLine("playingRoleName", self.client.playingRoleName)
        msg += self.getOneConstLine("activeRoleName", self.client.activeRoleName)
        msg += self.getOneConstLine("signUpChanName", self.client.signUpChanName)
        msg += self.getOneConstLine("adminBotCommandChan", self.client.adminBotCommandChan)
        msg += self.getOneConstLine("codesChannelName", self.client.codesChannelName)
        msg += self.getOneConstLine("medKitRoleName", self.client.medKitRoleName)
        msg += '\n'
        with open('help.txt') as f:
            msg += f.read()
        msg += "```"
        await ctx.message.author.send(msg)
        await ctx.message.delete()


def setup(client):
    client.add_cog(Utils(client))
