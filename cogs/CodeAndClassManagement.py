import asyncio
import discord
from discord.ext import commands

class CodeAndClassManagement(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.chosenClasses = []

    def translate_react_to_class(self, react):
        for idx, r in enumerate(self.client.classEmojis):
            if r == react.emoji:
                if idx == 0:
                    return 'Wings'
                if idx == 1:
                    return 'Grappin'
                if idx == 2:
                    return 'Drone'
        return ''

    def updateChosenClasses(self, react, user):
        className = self.translate_react_to_class(react)
        found = False
        for idx, choice in enumerate(self.client.chosenClasses):
            if not choice:
                continue
            if choice['user'] == user:
                self.client.chosenClasses[idx]['class'] = className
                found = True
                break
        if not found:
            self.client.chosenClasses.append({'user': user, 'class': className})
        return found

    async def removeOtherReactions(self, react, user):
        for emoji in self.client.classEmojis:
            if emoji != react.emoji:
                try:
                    await react.message.remove_reaction(emoji, user)
                except:
                    print("No reaction")

    async def printClassesByPlayer(self, codeChan):
        msg = 'Registered classes by player are:\n'
        for choice in self.client.chosenClasses:
            msg += '\t\t<@{}>\t:\t{}\n'.format(choice['user'].id, choice['class'])
        msg += "Please, if there is a mistake, contact an organizer with a proof as soon as possible !\n"
        await codeChan.send(msg)

    @commands.Cog.listener()
    async def on_reaction_add(self, react, user):
        if user == self.client.user:
            return
        if react.message.channel.name != self.client.codesChannelName:
            return
        if self.updateChosenClasses(react, user):
            await self.removeOtherReactions(react, user)
        return

    async def runCodeCmdError(self, ctx):
        await ctx.message.delete()
        await ctx.channel.send('```Please use .code [Game X/5] [CODE]\nExemple:\n\t.code 1 CG3C\nUse .help for more```')

    @commands.command(name='.code')
    async def code(self, ctx, game='', code=''):
        if ctx.channel.name != self.client.adminBotCommandChan:
            return
        if not game or not code:
            await self.runCodeCmdError(ctx)
            return
        codeChan = discord.utils.get(ctx.guild.channels, name=self.client.codesChannelName)
        await ctx.message.delete()
        msg = await codeChan.send('Game ' + game + '\t-\tCode : ' + code + '\nPlease react with the class you will use.')
        for react in self.client.classEmojis:
            await msg.add_reaction(react)
        await asyncio.sleep(60*self.client.minutesToChoseAClass)
        await self.printClassesByPlayer(codeChan)

def setup(client):
    client.add_cog(CodeAndClassManagement(client))
