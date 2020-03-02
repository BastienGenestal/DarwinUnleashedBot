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
        role = self.client.usefulRoles["medKitRole"]
        await member.add_roles(role)

    @commands.command(name='.refresh_players')
    async def refresh_players(self, ctx):
        signUpChan = self.client.usefulChannels["signUpChan"]
        playerRole = self.client.usefulRoles["playerRole"]
        msg = await signUpChan.fetch_message(self.client.medKitToPlayerMessageId)
        reaction = discord.utils.get(msg.reactions, emoji=self.client.signUpEmoji)
        async for user in reaction.users():
            if playerRole not in user.roles:
                await user.add_roles(playerRole)

    @commands.command(name='.end')
    async def end(self, ctx, arg=''):
        if ctx.channel.id != self.client.usefulChannels["botCommandChan"].id:
            return
        activeRole = self.client.usefulRoles["activeRole"]
        organizingRole = self.client.usefulRoles["organizingRole"]
        for member in activeRole.members:
            await member.remove_roles(activeRole)
        for member in organizingRole.members:
            await member.remove_roles(organizingRole)
        for role in self.client.BracketRoles:
            if not len(self.client.BracketRoles[role].members):
                continue
            for member in self.client.BracketRoles[role].members:
                try:
                    await member.remove_roles(self.client.BracketRoles[role])
                except Exception as e:
                    print(e)
        if arg != 'clear':
            return
        codeChan = self.client.usefulChannels["codesChan"]
        await codeChan.purge(limit=50)


    @commands.command(name='.clear')
    async def clear(self, ctx):
        if ctx.channel.name != self.client.usefulChannels['startSetChan'] and ctx.channel.name != self.client.usefulChannels['botCommandChan']:
            return
        try:
            await ctx.channel.purge(limit=200)
        except Exception as e:
            print(e)

def setup(client):
    client.add_cog(Utils(client))
