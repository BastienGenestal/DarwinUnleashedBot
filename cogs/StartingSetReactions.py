import discord
from discord.ext import commands

import GameSet
from const_messages import SIGN_UP_HERE_MSG


class StartingReactionsSet(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.signUpMsg = None

    async def create_sign_up_msg(self, react, user):
        mentionPlayers = self.client.usefullRoles['playerRole'].mention
        msg = react.emoji + '\t' + SIGN_UP_HERE_MSG.format(mentionPlayers, user.mention) + '\t' + react.emoji
        signUpMsg = await self.client.usefullChannels['signUpChan'].send(msg)
        await signUpMsg.add_reaction(self.client.signUpEmoji)
        return signUpMsg

    async def react_on_start_a_set(self, react, user):
        forWinner = None
        if react.emoji == self.client.usefullBasicEmotes["signUpWinner"]:
            forWinner = True
        elif react.emoji == self.client.usefullBasicEmotes["signUpNoWinner"]:
            forWinner = False
        else:
            return
        signUpMsg = await self.create_sign_up_msg(react, user)
        await user.add_roles(self.client.usefullRoles["organizingRole"])
        try:
            new_set = GameSet(user, forWinner, signUpMsg)
        except Exception as e:
            await user.remove_roles(self.client.usefullRoles["organizingRole"])
            signUpMsg.delete()
            print(e)


    async def react_on_sign_up(self, react, user):
        await user.add_roles(self.client.usefullRoles["activeRole"])

    @commands.Cog.listener()
    async def on_reaction_add(self, react, user):
        if user == self.client.user:
            return
        if self.client.startASetMsg and react.message.id == self.client.startASetMsg.id:
            await self.react_on_start_a_set(react, user)
        return


    @commands.Cog.listener()
    async def on_reaction_remove(self, react, user):
        if user == self.client.user or not self.client.signUpCmdMsg:
            return
        if react.message.id == self.client.signUpCmdMsg.id:
            await user.remove_roles(self.client.usefullRoles["organizingRole"])

def setup(client):
    client.add_cog(StartingReactionsSet(client))
