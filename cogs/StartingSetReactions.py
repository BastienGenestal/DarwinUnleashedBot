import discord
from discord.ext import commands

from GameSet import GameSet
from const_messages import SIGN_UP_HERE_MSG


class StartingReactionsSet(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.signUpMsg = None

    async def create_sign_up_msg(self, react, user):
        mentionPlayers = self.client.usefulRoles['playerRole'].mention
        msg = SIGN_UP_HERE_MSG.format(mentionPlayers, user.mention, react.emoji, react.emoji)
        signUpMsg = await self.client.usefulChannels['signUpChan'].send(msg)
        await signUpMsg.add_reaction(self.client.signUpEmoji)
        return signUpMsg

    async def react_on_start_a_set(self, react, user):
        forWinner = None
        if react.emoji == self.client.usefulBasicEmotes["signUpWinner"]:
            forWinner = True
        elif react.emoji == self.client.usefulBasicEmotes["signUpNoWinner"]:
            forWinner = False
        else:
            return
        signUpMsg = await self.create_sign_up_msg(react, user)
        try:
            new_set = GameSet(self.client, user, forWinner, signUpMsg)
            await new_set.director.add_roles(self.client.usefulRoles["organizingRole"])
        except Exception as e:
            await react.message.remove_reaction(react.emoji, user)
            await signUpMsg.delete()
            print(e)

    async def react_on_sign_up(self, react, user):
        await user.add_roles(self.client.usefulRoles["activeRole"])

    @commands.Cog.listener()
    async def on_reaction_add(self, react, user):
        if user == self.client.user:
            return
        if self.client.startASetMsg and react.message.id == self.client.startASetMsg.id:
            await self.react_on_start_a_set(react, user)
        return


    @commands.Cog.listener()
    async def on_reaction_remove(self, react, user):
        if user == self.client.user:
            return

def setup(client):
    client.add_cog(StartingReactionsSet(client))
