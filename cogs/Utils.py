import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord.ext.commands import has_permissions, CheckFailure

class Utils(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            return
        raise error

    @commands.command()
    async def refresh_players(self, ctx):
        signUpChan = self.client.usefulChannels["signUpChan"]
        playerRole = self.client.usefulRoles["playerRole"]
        msg = await signUpChan.fetch_message(self.client.medKitToPlayerMessageId)
        reaction = discord.utils.get(msg.reactions, emoji=self.client.usefulBasicEmotes['signUp'])
        async for user in reaction.users():
            if playerRole not in user.roles:
                await user.add_roles(playerRole)

    @commands.command()
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

    def is_not_start_a_set_msg(self, msg):
        return self.client.startASetMsg.id != msg.id

    @commands.command()
    @has_permissions(administrator=True, manage_messages=True)
    async def purge(self, ctx):
        if ctx.channel.name != self.client.usefulChannels['startSetChan'] and ctx.channel.name != self.client.usefulChannels['botCommandChan']:
            return
        try:
            await ctx.channel.purge(limit=200, check=self.is_not_start_a_set_msg)
        except Exception as e:
            print(e)

    @commands.command()
    @has_permissions(administrator=True, manage_messages=True)
    async def clear(self, ctx, args=None):
        maxNb = 50
        nbMsgToDelete = 10
        if args:
            try:
                nbMsgToDelete = int(args)
                if nbMsgToDelete > maxNb:
                    nbMsgToDelete = maxNb
            except ValueError:
                nbMsgToDelete = 10
        try:
            await ctx.channel.purge(limit=(nbMsgToDelete + 1), check=self.is_not_start_a_set_msg)
        except Exception as e:
            print(e)

    @clear.error
    async def clear_error(error, ctx):
        if isinstance(error, CheckFailure):
            await ctx.message.channel.send("Looks like you don't have the perm.")

def setup(client):
    client.add_cog(Utils(client))
