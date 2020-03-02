from discord.ext import commands


class RemoveWinnerMedKitRole(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        wasAttributed = self.client.usefulRoles['winnerRole'] in before.roles
        isAttributed = self.client.usefulRoles['winnerRole'] in after.roles
        if wasAttributed != isAttributed and isAttributed:
            if self.client.usefulRoles['medKitRole'] in after.roles:
                await after.remove_roles(self.client.usefulRoles['medKitRole'])

def setup(client):
    client.add_cog(RemoveWinnerMedKitRole(client))
