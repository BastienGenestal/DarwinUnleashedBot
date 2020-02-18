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

    def is_it_for_winner(self, emoji):
        if emoji == self.client.usefulBasicEmotes["signUpWinner"]:
            return True
        elif emoji == self.client.usefulBasicEmotes["signUpNoWinner"]:
            return False
        return None

    async def react_on_start_a_set(self, react, user):
        forWinner = self.is_it_for_winner(react.emoji)
        new_set = None
        try:
            new_set = await GameSet.create(GameSet(), self.client, user, forWinner)
        except Exception as e:
            await react.message.remove_reaction(react.emoji, user)
            print(e)
        if not new_set:
            return
        # TODO: Timer blocks the code in GameSet.create()
        print(new_set.director, new_set.forWinner, new_set.bracket, new_set.signUpMsg)

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
