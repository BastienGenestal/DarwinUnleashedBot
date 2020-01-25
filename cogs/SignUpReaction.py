import discord
from discord.ext import commands

class SignUpReaction(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.signUpMessage = ''

    @commands.Cog.listener()
    async def on_reaction_add(self, react, user):
        if user == self.client.user:
            return
        if react.message.channel.name != self.client.signUpChanName:
            return
        if self.client.signUpMessage and react.message.id == self.client.signUpMessage.id:
            activeRole = discord.utils.get(react.message.guild.roles, name=self.client.activeRoleName)
            if not self.client.fillerMsg and len(activeRole.members) >= self.client.maxActivePlayers:
                self.client.fillerMsg = await react.message.channel.send("You can react here to be a Filler")
                await self.client.fillerMsg.add_reaction(self.client.fillerReactEmoji)
            if len(activeRole.members) >= self.client.maxActivePlayers:
                await react.message.remove_reaction(self.client.signUpEmoji, user)
                await user.send("Sorry the Active role is full for now. You can react to be a Filler")
                return
            await user.add_roles(activeRole)

    @commands.Cog.listener()
    async def on_reaction_remove(self, react, user):
        if user == self.client.user:
            return
        if react.message.channel.name != self.client.signUpChanName:
            return
        if react.message.id == self.client.signUpMessage.id:
            activeRole = discord.utils.get(react.message.guild.roles, name=self.client.activeRoleName)
            logs = discord.utils.get(react.message.guild.channels, name=self.client.logsChan)
            await logs.send('{} removed his active role'.format(user.name))
            await user.remove_roles(activeRole)

    @commands.command(name='.start')
    async def start(self, ctx):
        if ctx.channel.name != self.client.adminBotCommandChan:
            return
        signUpChan = discord.utils.get(ctx.guild.channels, name=self.client.signUpChanName)
        players = discord.utils.get(ctx.guild.roles, name=self.client.playingRoleName)
        self.client.signUpMessage = await signUpChan.send('{} games starting in 15 minutes, react to participate !'.format(players.mention))
        await self.client.signUpMessage.add_reaction(self.client.signUpEmoji)
        # For later
        # signUpChan.send('{} next match sign up open in 15 minutes'.format(players.mention))
        #await asyncio.sleep(60*15)
        #await signUpChan.send('Please react here to play in the set !'.format(players.mention))


def setup(client):
    client.add_cog(SignUpReaction(client))
