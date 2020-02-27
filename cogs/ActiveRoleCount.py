from discord.ext import commands


class ActiveRoleCount(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        # TODO CHECK IF rs<10
        wasActive = self.client.usefulRoles['activeRole'] in before.roles
        isActive = self.client.usefulRoles['activeRole'] in after.roles
        if wasActive != isActive:
            if isActive: # Si son bracket est plein
#                if len(self.client.usefulRoles['activeRole'].members) > 9:
                pass
            else:
                pass

def setup(client):
    client.add_cog(ActiveRoleCount(client))
