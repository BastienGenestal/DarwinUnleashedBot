import asyncio
import discord
from discord.ext import commands


class StartingSet(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.signUpCmdMsg = None

    @commands.Cog.listener()
    async def on_reaction_add(self, react, user):
        if user == self.client.user or not self.client.signUpCmdMsg:
            return
        if react.message.id == self.client.signUpCmdMsg.id:
            await user.add_roles(self.client.usefullRoles["organizingRole"])

    @commands.Cog.listener()
    async def on_reaction_remove(self, react, user):
        if user == self.client.user or not self.client.signUpCmdMsg:
            return
        if react.message.id == self.client.signUpCmdMsg.id:
            await user.remove_roles(self.client.usefullRoles["organizingRole"])

    @staticmethod
    async def start_cmd_error(ctx):
        await ctx.channel.send("```Please use .start [X]\n\tX\tMinutes before the sign up message```")

    @commands.command(name='.start')
    async def start(self, ctx, mins='15'):
        if ctx.channel.id != self.client.usefullChannels["botCommandChan"].id:
            return
        try:
            minsNb = float(mins)
        except (ValueError, TypeError):
            return await self.start_cmd_error(ctx)
        self.client.signUpCmdMsg = ctx.message
        await self.client.signUpCmdMsg.add_reaction(self.client.signUpEmoji)
        sign_up_chan = self.client.usefullChannels["signUpChan"]
        players = self.client.usefullRoles["playingRole"]
        if minsNb == 0:
            self.client.signUpMessage = await sign_up_chan.send('{} games starting in 15 minutes, react to participate !'.format(players.mention))
            await self.client.signUpMessage.add_reaction(self.client.signUpEmoji)
            return
        minutesStr = 'minute' if (minsNb <= 1) else 'minutes'
        temp = await sign_up_chan.send(
            '{} Sign up for the next set in {} {} !\nBe quick or you might miss it :wink:'.format(players.mention, mins,
                                                                                                  minutesStr))
        await asyncio.sleep(60 * minsNb)
        await temp.delete()
        self.client.signUpMessage = await sign_up_chan.send('Please react here to play in the set !')
        await self.client.signUpMessage.add_reaction(self.client.signUpEmoji)


def setup(client):
    client.add_cog(StartingSet(client))
