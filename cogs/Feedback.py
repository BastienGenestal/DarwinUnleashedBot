import discord
from discord.ext import commands


class Feedback(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, msg):
        if type(msg.channel) == discord.TextChannel and msg.channel.id == self.client.usefullChannels["feedbackChan"].id:
            msgcontent = msg.content
            await msg.delete()
            temp = discord.utils.get(msg.channel.guild.members, id=283236278584082432)
            await temp.send("```{} said:\n\t{}```".format(msg.author.name, msgcontent))
            receivedChan = self.client.usefullChannels["receivedFeedbackChan"]
            await receivedChan.send(msgcontent)
            await msg.author.send("Thank you for the feedback !\nYour feedback:\n```{}```".format(msgcontent))
        return


def setup(client):
    client.add_cog(Feedback(client))
