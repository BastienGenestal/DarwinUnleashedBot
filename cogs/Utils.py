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
        role = self.client.usefullRoles["medKitRole"]
        await member.add_roles(role)

    @commands.command(name='.refresh_players')
    async def refresh_players(self, ctx):
        signUpChan = self.client.usefullChannels["signUpChan"]
        playerRole = self.client.usefullRoles["playingRole"]
        msg = await signUpChan.fetch_message(self.client.medKitToPlayerMessageId)
        reaction = discord.utils.get(msg.reactions, emoji=self.client.signUpEmoji)
        async for user in reaction.users():
            if playerRole not in user.roles:
                await user.add_roles(playerRole)

    @commands.command(name='.clear')
    async def clear(self, ctx):
        if ctx.channel.id != self.client.usefullChannels["botCommandChan"].id:
            return
        try:
            await ctx.channel.purge(limit=200)
        except Exception as e:
            print(e)

    def getOneConstLine(self, variableName, value):
        return '\t\t{} = {}\n'.format(variableName, value)

    @commands.command(name='.help')
    async def help(self, ctx):
        if ctx.channel.id != self.client.usefullChannels["botCommandChan"].id:
            return
        msg = "```Constants variables:\n"
        for (var, chan) in self.client.usefullChannels:
            msg += "{}\t=\t{}".format(var, chan.name)
        for (var, role) in self.client.usefullRoles:
            msg += "{}\t=\t{}".format(var, role.name)
        msg += '\n'
        with open('help.txt') as f:
            msg += f.read()
        msg += "```"
        await ctx.message.author.send(msg)
        await ctx.message.delete()


def setup(client):
    client.add_cog(Utils(client))
