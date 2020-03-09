import discord
from discord.ext import commands
import re

from const_messages import CODE_MESSAGE, FUN_GAMES_CODE_MSG


class CodeCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @staticmethod
    def check_code(code):
        code_regex = r'[A-Z0-9]{4}'
        return bool(re.match(code_regex, code))

    def get_set_object(self, author): # TODO: get_set_object from DIRECTOR/BRACKET/LAST_CMD_MSG/...
        for set in self.client.Sets:
            if set.director.id == author.id:
                return set
        return None

    def get_set_object_public_msg(self, last_code_public_msg): # TODO: get_set_object from DIRECTOR/BRACKET/LAST_CMD_MSG/...
        for set in self.client.Sets:
            if set.last_code_public_msg and set.last_code_public_msg.id == last_code_public_msg.id:
                return set
        return None

    @commands.Cog.listener()
    async def on_reaction_add(self, react, user):
        if user.bot:
            return
        if react.emoji != self.client.usefulBasicEmotes["cancel"]:
            return
        if react.message.channel == self.client.usefulChannels['startSetChan']:
            rightSet = self.get_set_object(react.message.author)
            if rightSet:
                await rightSet.last_code_cmd.delete()
                await rightSet.last_code_public_msg.delete()
                if rightSet.last_fun_code_public_msg:
                    await rightSet.last_fun_code_public_msg.delete()
                return
        elif react.message.channel == self.client.usefulChannels['codesChan']:
            rightSet = self.get_set_object_public_msg(react.message)
            if rightSet:
                await rightSet.director.send('{} left the set. ({})'.format(user.name, rightSet.bracket))
                return await user.remove_roles(self.client.usefulRoles['activeRole'], rightSet.bracket)
        return

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return
        if msg.channel.id != self.client.usefulChannels["startSetChan"].id:
            return
        if msg.content.startswith(self.client.command_prefix):
            return
        rightSet = self.get_set_object(msg.author)
        if not rightSet:
            await msg.author.send("You are not directing any set.")
            await msg.delete()
            return
        # if self.check_screenshot:
        #   await read_screeshot()
        if self.check_code(msg.content):
            await self.post_code(rightSet, msg.content)
            await msg.add_reaction(self.client.usefulBasicEmotes["cancel"])
            rightSet.last_code_cmd = msg
            rightSet.task.cancel()
            return
        return await msg.channel.send("Invalid Darwin Project code : **{}**.".format(msg.content))

    async def post_code(self, right_set, code=''):
        code_channel = self.client.usefulChannels["codesChan"]

        code_msg = await code_channel.send(
            CODE_MESSAGE.format(
                right_set.bracket.mention,
                code,
                self.client.usefulBasicEmotes['cancel'],
                self.client.usefulChannels['funGames']
            )
        )
        await code_msg.add_reaction(self.client.usefulBasicEmotes["cancel"])
        right_set.last_code_public_msg = code_msg
        if right_set.forFun:
            fun_code_msg = await self.client.usefulChannels['funGames'].send(
                FUN_GAMES_CODE_MSG.format(
                    right_set.bracket.name,
                    len(right_set.bracket.members),
                    code,
                    self.client.usefulBasicEmotes['signUp']
                )
            )
            await fun_code_msg.add_reaction(self.client.usefulBasicEmotes["signUp"])
            right_set.last_fun_code_public_msg = fun_code_msg



def setup(client):
    client.add_cog(CodeCog(client))
