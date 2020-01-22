import discord
from discord.ext import commands

class GamePrep(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='.prep')
    async def prep(self, ctx, arg=''):
        temp = ctx.message.content
        await ctx.message.delete()
        if not arg:
            return
        temp = temp[5:]
        self.client.preparing = True
        signUpMessage = await ctx.send("Sign Up here for the next set at" + temp, nonce=69420)
        await signUpMessage.add_reaction(self.client.reaction_numbers[0])

    @commands.command(name=".end")
    async def end(self, ctx):
        if ctx.channel.name == self.client.adminBotCommandChan:
            self.client.started = self.client.preparing = False
            await ctx.message.delete()

def setup(client):
    client.add_cog(GamePrep(client))
