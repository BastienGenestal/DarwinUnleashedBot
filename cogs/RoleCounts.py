from discord.ext import commands


class RoleCounts(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def rsCmdError(self, ctx):
        return await ctx.channel.send(
            "```To get the number of members in a role :\n"
            "Exemple :\n"
            "\t.rs active organizer```"
        )

    async def whoisCmdError(self, ctx):
        return await ctx.channel.send(
            "```To get the list of members in a role :\n"
            "Exemple :\n"
            "\t.whois active organizer```"
        )

    @commands.command(name='.rs')
    async def rs(self, ctx, *args):
        if ctx.channel.name != self.client.adminBotCommandChan:
            return
        if not args:
            return await self.rsCmdError(ctx)
        msg = ''
        for arg in args:
            for r in ctx.guild.roles:
                if r.name.lower() != arg.lower():
                    continue
                msg += "{} : {} members\n".format(r.name, len(r.members))
        if not msg:
            msg = "Unknown role"
        await ctx.channel.send("```{}```".format(msg))

    @commands.command(name='.whois')
    async def whois(self, ctx, *args):
        if ctx.channel.name != self.client.adminBotCommandChan:
            return
        if not args:
            return await self.whoisCmdError(ctx)

        msg = ''
        for idx, arg in enumerate(args):
            if idx != 0:
                msg += "\n"

            for r in ctx.guild.roles:
                rmembers = []
                if r.name.lower() != arg.lower():
                    continue
                for member in r.members:
                    rmembers.append(member.name)

                msg += "{0} ({1}):\n".format(r.name, len(rmembers))
                for name in rmembers:
                    msg += "\t{}\n".format(name)

        if not msg:
            msg = "Unknown role"
        await ctx.channel.send("```{}```".format(msg))


def setup(client):
    client.add_cog(RoleCounts(client))
