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

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author == self.client.user:
            return
        if type(msg.channel) != discord.TextChannel or \
                msg.channel.id != self.client.usefulChannels["enterCodesChan"].id:
            return
        code = msg.content
        if not self.check_code(code):
            return await msg.channel.send("Invalid Darwin Project code : **{}**.".format(code))
        await self.post_code(code)

    async def post_code(self, code=''):
        code_channel = self.client.usefulChannels["codesChan"]
        code_msg = await code_channel.send("Code : **{}**".format(code))
        # 'negative_squared_cross_mark'
        await code_msg.add_reaction(self.client.usefulBasicEmotes["cancel"])


def setup(client):
    client.add_cog(CodeCog(client))
