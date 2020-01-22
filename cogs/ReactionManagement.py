import asyncio
import discord
from discord.ext import commands

class ReactionManagement(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.chosenClasses = []
        self.client.codeMessages = []

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
        if self.updateChosenClasses(react, user):
            await self.removeOtherReactions(react, user)
        return

    @commands.command(name='.code')
    async def code(self, ctx, args):
        codeChan = discord.utils.get(ctx.guild.channels, name=self.client.codesChannelName)
        await ctx.message.delete()
        msg = await codeChan.send('Code : ' + args + ' Please react with the class you will use.')
        for react in self.client.classEmojis:
            await msg.add_reaction(react)
        self.client.codeMessages.append(ctx.message)
        await asyncio.sleep(60*self.client.minutesToChoseAClass)
        await self.printClassesByPlayer(codeChan)

def setup(client):
    client.add_cog(ReactionManagement(client))
