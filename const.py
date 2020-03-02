ServerId = 669299962336772126

### Text-channels names

UsefulChannelNames = {
    ("startSetChan", "start-a-set"),
    ("funGames", "fun-games"),
    ("logsChan", "bot-commands"),
    ("signUpChan", "sign-up"),
    ("botCommandChan", "bot-commands"),
    ("codesChan", "codes-and-class-reactions"),
    ("selectRegionChan", "about-you"),
    ("selectPlatformChan", "about-you"),
    ("startASetChan", "start-a-set"),
    ("feedbackChan", "feedback"),
    ("receivedFeedbackChan", "received-feedback")
}

### Roles names

UsefulRoles = {
    ("medKitRole", "Medkit"),
    ("winnerRole", "Winner"),
    ("playerRole", "Players"),
    ("activeRole", "Active"),
    ("organizingRole", "Active-Organizer")
}

BracketRoles = {
    ("A", "Bracket A"),
    ("B", "Bracket B"),
    ("C", "Bracket C"),
    ("D", "Bracket D"),
    ("E", "Bracket E"),
    ("F", "Bracket F")
}

### Emotes

classEmojis = ["<:wings:671004464974397443>", "<:grapple:671004444204466176>", "<:birdrone:671004417356595233>"]
classEmojisId = [671004464974397443, 671004444204466176, 671004417356595233]

regionEmojis =["🇪🇺", "🇺🇸", "🇧🇷", "🇦🇺", "🏳️", "㊙️"]
regions = ["EU",  "NA-East", "SA", "AP(Sydney)", "NA-West", "AP(Singapore)"]

platformEmojis =  ["🖱️", "❌", "🎮"]
platforms = ["PC", "Xbox", "PS4"]

UsefulCustomEmotes = {
    ("unleashed", "unleashed"),
    ("wings", "wings"),
    ("grapple", "grapple"),
    ("birdrone", "birdrone"),
}

UsefulBasicEmotes = {
    ("signUpWinner", "🎖️"),
    ("signUpNoWinner", "⚽"),
    ("signUp", "✅"),
    ("cancel", "❎"),
}

#("signUpWinnerEmote", "🎖"),("signUpNotWinnerEmote️e", "⚽"),

signUpEmoji = '✅'

### Const IDs

medKitToPlayerMessageId = 669847178419896322
regionSelectionMessage = 670266247023427594
platformSelectionMessage = 670262105060147207

### Other values

minutesToChoseAClass = 3

MAX_NB_PLAYER_PER_GAME = 10

"""
    def isItStartASetChan(self, event):
        guild = discord.utils.get(self.client.guilds, id=event.guild_id)
        if guild != self.client.server:
            return False
        startASetChan = self.client.usefulChannels["startASetChan"]
        if not event.emoji:
            return False
        return event.channel_id == startASetChan.id and event.emoji.name == self.client.signUpEmoji

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, event):
        if not self.isItStartASetChan(event):
            return
        print("Starting a set")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, event):
        if not self.isItStartASetChan(event):
            return

    @commands.command(name='.start')
    async def start(self, ctx, mins='15'):
        if ctx.channel.id != self.client.usefulChannels["botCommandChan"].id:
            return
        try:
            minsNb = float(mins)
        except (ValueError, TypeError):
            return await self.start_cmd_error(ctx)
        self.client.signUpCmdMsg = ctx.message
        await self.client.signUpCmdMsg.add_reaction(self.client.signUpEmoji)
        sign_up_chan = self.client.usefulChannels["signUpChan"]
        players = self.client.usefulRoles["playerRole"]
        if minsNb == 0:
            self.client.signUpMessage = await sign_up_chan.send('{} games starting in 15 minutes, react to participate !'.format(players.mention))
            await self.client.signUpMessage.add_reaction(self.client.signUpEmoji)
            return
        minutesStr = 'minute' if (minsNb <= 1) else 'minutes'
        temp = await sign_up_chan.send(
            '{} Sign up for the next set in {} {} !\nBe quick or you might miss it :wink:'.format(players.mention, mins, minutesStr))
        await asyncio.sleep(60 * minsNb)
        await temp.delete()
        self.client.signUpMessage = await sign_up_chan.send('Please react here to play in the set !')
        await self.client.signUpMessage.add_reaction(self.client.signUpEmoji)

"""