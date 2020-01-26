import asyncio
import discord
from discord.ext import commands
import time

class CodeAndClassManagement(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.init_set()

    def init_set(self):
        self.nbGamePerSet = 5
        self.lastMessage = 0
        self.cancelledMsg = []
        self.client.chosenClasses = []
        self.client.fillerMsg = ''

    def translate_react_to_class(self, react):
        for idx, r in enumerate(self.client.classEmojis):
            if r == react.emoji:
                if idx == 0:
                    return 'Wings'
                if idx == 1:
                    return 'Grapple'
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

    async def removeSignUpMessages(self):
        current_time = time.strftime("%H:%M:%S", time.localtime())
        await self.client.signUpMessage.delete()
        self.client.signUpMessage = await self.client.signUpMessage.channel.send('Set is running... First game started at ' + current_time)

    async def printClassesByPlayer(self, codeChan):
        msg = 'Registered classes by player are:\n'
        for choice in self.client.chosenClasses:
            msg += '\t\t<@{}>\t:\t{}\n'.format(choice['user'].id, choice['class'])
        msg += "Please if there is a mistake, contact an organizer with a proof as soon as possible !\n"
        await codeChan.send(msg)
        self.client.chosenClasses = []

    @commands.Cog.listener()
    async def on_reaction_add(self, react, user):
        if user == self.client.user:
            return
        if react.message.channel.name != self.client.codesChannelName:
            return
        if self.updateChosenClasses(react, user):
            await self.removeOtherReactions(react, user)
        return

    @commands.Cog.listener()
    async def on_message_delete(self, msg):
        if msg.id == self.lastMessage:
            self.cancelledMsg.append(msg.id)
            self.client.chosenClasses = []
        return

    async def runCodeCmdError(self, ctx):
        await ctx.channel.send('```Please use .code [Game X/5] [CODE]\nExemple:\n\t.code 1 CG3C\nUse .help for more```')

    async def sendAndReactCodeAndClassMsg(self, ctx, game, code, codeChan, activeRole):
        msg = await codeChan.send(
            'Game ' + game + '\t-\tCode : ' + code + '\n{} Please react with the class you will use.'.format(activeRole.mention))
        for react in self.client.classEmojis:
            await msg.add_reaction(react)
        self.lastMessage = msg.id
        return msg.id

    async def sleepButCheck(self, reactTime, msgId, codeChan):
        for i in range(reactTime):
            await asyncio.sleep(1)
            if msgId in self.cancelledMsg:
                return True
        return False

    async def checkCodeCmd(self, ctx, game, code):
        if not game or not code or len(code) != 4:
            await self.runCodeCmdError(ctx)
            return 0
        gameNb = int(game)
        if not gameNb or gameNb > self.nbGamePerSet:
            print(gameNb, ">", self.nbGamePerSet)
            await self.runCodeCmdError(ctx)
            return 0
        return gameNb

    @commands.command(name='.code')
    async def code(self, ctx, game='', code=''):
        if ctx.channel.name != self.client.adminBotCommandChan:
            return
        gameNb = await self.checkCodeCmd(ctx, game, code)
        if not gameNb:
            return
        #if ctx.message:
        #   await ctx.message.delete()
        codeChan = discord.utils.get(ctx.guild.channels, name=self.client.codesChannelName)
        activeRole = discord.utils.get(ctx.guild.roles, name=self.client.activeRoleName)
        msgId = await self.sendAndReactCodeAndClassMsg(ctx, game, code, codeChan, activeRole)
        if await self.sleepButCheck(60*self.client.minutesToChoseAClass, msgId, codeChan):
            print("Cancelling print")
            await ctx.message.author.send("Cancelled Game {} with code {}".format(game, code))
            return
        if gameNb == 1:
            await self.removeSignUpMessages()
        await self.printClassesByPlayer(codeChan)


    @commands.command(name='.end')
    async def end(self, ctx, arg=''):
        if ctx.channel.name != self.client.adminBotCommandChan:
            return
        activeRole = discord.utils.get(ctx.guild.roles, name=self.client.activeRoleName)
        fillRole = discord.utils.get(ctx.guild.roles, name=self.client.fillerRoleName)
        for member in activeRole.members:
            await member.remove_roles(activeRole)
        for member in fillRole.members:
            await member.remove_roles(fillRole)
        if self.client.signUpMessage:
            await self.client.signUpMessage.delete()
        self.init_set()
        if arg != 'clear':
            return
        codesChan = discord.utils.get(ctx.guild.channels, name=self.client.codesChannelName)
        await codesChan.purge(limit=50)

def setup(client):
    client.add_cog(CodeAndClassManagement(client))
