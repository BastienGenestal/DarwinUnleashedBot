import discord
from discord.ext import commands
import re


class CodeCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @staticmethod
    def check_code(code):
        code_regex = r'[A-Z0-9]{4}'
        return bool(re.match(code_regex, code))

    def get_set_object(self, author):
        for set in self.client.Sets:
            if set.director.id == author.id:
                return set
        return None

    @commands.Cog.listener()
    async def on_reaction_add(self, react, user):
        if user.bot:
            return
        if react == self.client.usefulBasicEmotes["cancel"] and react.message.channel == self.client.usefulChannels['startSetChan']:
            pass


    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return
        if msg.channel.id != self.client.usefulChannels["startSetChan"].id:
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
            # TODO: IF REACTION ON THIS MESSAGE REMOVE THIS MSG + CODE MSG
            return
        return await msg.channel.send("Invalid Darwin Project code : **{}**.".format(msg.content))

    async def post_code(self, rightSet, code=''):
        code_channel = self.client.usefulChannels["codesChan"]
        code_msg = await code_channel.send("**{}**\nCode : **{}**".format(rightSet.bracket.mention, code))
        # 'negative_squared_cross_mark'
        # TODO: IF REACTION ON THIS MESSAGE REMOVE ACTIVE ROLE AND CHECK rs < 10...
        await code_msg.add_reaction(self.client.usefulBasicEmotes["cancel"])
        rightSet.last_code_public_msg = code_msg


def setup(client):
    client.add_cog(CodeCog(client))
