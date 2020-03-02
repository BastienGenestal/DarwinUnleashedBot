from discord.ext import commands


class ActiveRoleCount(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        for Set in self.client.Sets:
            wasActive = Set.bracket in before.roles
            isActive = Set.bracket in after.roles
            if wasActive != isActive:
                Set.forFun = (len(Set.bracket.members) < 10)

def setup(client):
    client.add_cog(ActiveRoleCount(client))
