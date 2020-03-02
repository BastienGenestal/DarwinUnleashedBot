from discord.ext import commands


class SignUpReaction(commands.Cog):
    def __init__(self, client):
        self.client = client

    def is_it_reaction_to_sign_up(self, set, messageId):
        if set.signUpMsg and messageId == set.signUpMsg.id:
            return True
        if set.last_fun_code_public_msg and messageId == set.last_fun_code_public_msg.id:
            return True
        return False

    @commands.Cog.listener()
    async def on_reaction_add(self, react, user):
        if user.bot:
            return
        for set in self.client.Sets:
            if self.is_it_reaction_to_sign_up(set, react.message.id) and not set.isFull:
                await set.add_player(self.client, user)
                if set.isFull:
                    set.complete(self.client)

    @commands.Cog.listener()
    async def on_reaction_remove(self, react, user):
        if user.bot:
            return
        for set in self.client.Sets:
            if self.is_it_reaction_to_sign_up(set, react.message.id):
                await set.add_player(self.client, user)
                try:
                    await set.remove_player(self.client, user)
                    logs = self.client.usefulChannels['logsChan']
                    await logs.send('{} removed his active role'.format(user.name))
                except Exception:
                    print('No role to remove')

def setup(client):
    client.add_cog(SignUpReaction(client))
