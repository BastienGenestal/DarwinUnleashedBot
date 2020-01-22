import discord
from discord.ext import commands

codesChannelName = "codes"

class ReactionManagement(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.codeMessages = []

    async def getEmojiIdx(self, cmp):
        for idx, emoji in enumerate(self.client.reaction_numbers):
            if emoji == cmp:
                return idx

    async def getPlayingRoleAndBracket(self, reaction):
        guild = reaction.message.guild
        roles = guild.roles
        playingRole = discord.utils.get(roles, name=self.client.playingRoleName)
        idx = await self.getEmojiIdx(reaction.emoji)
        bracket = "Bracket " + self.client.BRACKETS[idx]
        bracketRole = discord.utils.get(roles, name=bracket)
        return [playingRole, bracketRole]

    async def resetSignUpReactions(self, reactions):
        for react in reactions:
            for idx, numEmoji in enumerate(self.client.reaction_numbers):
                if react.emoji == numEmoji:
                    self.client.signUpReactions[idx] = react.count
                    continue

    async def on_reaction_add(self, reaction, user):
        if reaction.message.nonce == 69420:
            await self.resetSignUpReactions(reaction.message.reactions)
            if user == reaction.message.author:
                return
            roles = await self.getPlayingRoleAndBracket(reaction)
            for role in roles:
                await user.add_roles(role)
            for idx, i in enumerate(self.client.signUpReactions):
                if i > 1:
                    try:
                        await reaction.message.remove_reaction(self.client.reaction_numbers[idx], reaction.message.author)
                    except:
                        print("No reaction")
                if i > self.client.NB_PLAYERS_PER_GAME and idx < 10:
                    await reaction.message.add_reaction(self.client.reaction_numbers[idx + 1])

    async def on_reaction_remove(self, reaction, user):
        if reaction.message.channel.name == codesChannelName and reaction.message.startsWith("Code"):
            if user == reaction.message.author:
                return
            roles = await self.getPlayingRoleAndBracket(reaction)
            for role in roles:
                await user.remove_roles(role)
            if user == reaction.message.author:
                return
            for idx, i in enumerate(self.client.signUpReactions):
                if i == 1:
                    await reaction.message.add_reaction(self.client.reaction_numbers[idx])

    @commands.command(name='.code')
    async def code(self, ctx, args):
        codeChan = discord.utils.get(ctx.guild.channels, name=codesChannelName)
        await ctx.message.delete()
        msg = await codeChan.send('Code : ' + args + ' Please react with the class you will use.')
        for react in self.client.classEmojis:
            await msg.add_reaction(react)
        self.client.codeMessages.append(ctx.message)



def setup(client):
    client.add_cog(ReactionManagement(client))
