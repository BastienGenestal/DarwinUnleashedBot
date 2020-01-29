import asyncio
import discord
from discord.ext import commands


class StartingSet(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.signUpCmdMsg = None

    @commands.Cog.listener()
    async def on_reaction_add(self, react, user):
        if user == self.client.user or not self.signUpCmdMsg:
            return
        if react.message.id == self.signUpCmdMsg.id:
            organizingRole = discord.utils.get(react.message.guild.roles, name=self.client.organizingRoleName)
            await user.add_roles(organizingRole)

    @commands.Cog.listener()
    async def on_reaction_remove(self, react, user):
        if user == self.client.user or not self.signUpCmdMsg:
            return
        if react.message.id == self.signUpCmdMsg.id:
            organizingRole = discord.utils.get(react.message.guild.roles, name=self.client.organizingRoleName)
            await user.remove_roles(organizingRole)

    @staticmethod
    async def start_cmd_error(ctx):
        await ctx.channel.send("```Please use .start [X]\n\tX\tMinutes before the sign up message```")

    @commands.command(name='.start')
    async def start(self, ctx, mins='15'):
        if ctx.channel.name != self.client.adminBotCommandChan:
            return
        try:
            minsNb = float(mins)
        except (ValueError, TypeError):
            return await self.start_cmd_error(ctx)
        self.signUpCmdMsg = ctx.message
        await self.signUpCmdMsg.add_reaction(self.client.signUpEmoji)
        signUpChan = discord.utils.get(ctx.guild.channels, name=self.client.signUpChanName)
        players = discord.utils.get(ctx.guild.roles, name=self.client.playingRoleName)
        # self.client.signUpMessage = await signUpChan.send(
        #    '{} games starting in 15 minutes, react to participate !'.format(players.mention))
        # await self.client.signUpMessage.add_reaction(self.client.signUpEmoji)
        minutesStr = 'minute' if (minsNb <= 1) else 'minutes'
        temp = await signUpChan.send(
            '{} Sign up for the next set in {} {} !\nBe quick or you might miss it :wink:'.format(players.mention, mins,
                                                                                                  minutesStr))
        await asyncio.sleep(60 * minsNb)
        await temp.delete()
        self.client.signUpMessage = await signUpChan.send('Please react here to play in the set !')
        await self.client.signUpMessage.add_reaction(self.client.signUpEmoji)


def setup(client):
    client.add_cog(StartingSet(client))
