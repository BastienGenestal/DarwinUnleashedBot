from discord.ext import commands


class SignUpReaction(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_reaction_add(self, react, user):
        if user.bot:
            return
        for set in self.client.Sets:
            if set.signUpMsg and react.message.id == set.signUpMsg.id:
                await set.add_player(self.client, user)

    @commands.Cog.listener()
    async def on_reaction_remove(self, react, user):
        if user == self.client.user:
            return
        if react.message.channel.id != self.client.usefulChannels["signUpChan"].id or not self.client.signUpMessage:
            return
        if react.message.id == self.client.signUpMessage.id:
            activeRole = self.client.usefulRoles['activeRole']
            logs = self.client.usefulChannels['logsChan']
            await logs.send('{} removed his active role'.format(user.name))
            await user.remove_roles(activeRole)


def setup(client):
    client.add_cog(SignUpReaction(client))
