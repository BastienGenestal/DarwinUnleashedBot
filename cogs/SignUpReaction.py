from discord.ext import commands


class SignUpReaction(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_reaction_add(self, react, user):
        if user.bot:
            return
        for set in self.client.Sets:
            if set.signUpMsg and react.message.id == set.signUpMsg.id and not set.isFull:
                await set.add_player(self.client, user)
                if set.isFull:
                    set.complete(self.client)

    @commands.Cog.listener()
    async def on_reaction_remove(self, react, user):
        if user.bot:
            return
        for set in self.client.Sets:
            if set.signUpMsg and react.message.id == set.signUpMsg.id:
                await set.add_player(self.client, user)
                try:
                    await set.remove_player(self.client, user)
                    logs = self.client.usefulChannels['logsChan']
                    await logs.send('{} removed his active role'.format(user.name))
                except Exception:
                    print('No role to remove')

def setup(client):
    client.add_cog(SignUpReaction(client))
