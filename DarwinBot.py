import os
from discord.ext import commands
from const import *


class DarwinBot(commands.Bot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)
        # Now self has client

        # Initializing constants
        self.adminBotCommandChan = adminBotCommandChan
        self.signUpChanName = signUpChanName
        self.codesChannelName = codesChannelName
        self.selectPlatform = selectPlatform
        self.selectRegion = selectRegion
        self.platformEmojis = platformEmojis
        self.regionEmojis = regionEmojis

        self.medKitRoleName = medKitRoleName
        self.playingRoleName = playingRoleName
        self.activeRoleName = activeRoleName
        self.fillerRoleName = fillerRoleName
        self.logsChan = logsChan

        self.classEmojis = classEmojis
        self.signUpEmoji = signUpEmoji
        self.fillerReactEmoji = fillerReactEmoji

        self.minutesToChoseAClass = minutesToChoseAClass
        self.maxActivePlayers = maxActivePlayers

        self.regions = regions
        self.platforms = platforms
        self.feedback = feedback
        self.receivedFeedback = receivedFeedback

        self.medKitToPlayerMessageId = medKitToPlayerMessageId
        self.regionSelectionMessageId = regionSelectionMessage
        self.platformSelectionMessageId = platformSelectionMessage

        # Loading cogs
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                self.load_extension('cogs.{}'.format(filename[:-3]))

    @commands.command()
    async def load(self, ext):
        for filename in os.listdir('./cogs'):
            if filename == ext:
                self.load_extension('cogs.{}'.format(filename[:-3]))

    @commands.command()
    async def unload(self, ext):
        for filename in os.listdir('./cogs'):
            if filename == ext:
                self.unload_extension('cogs.{}'.format(filename[:-3]))

    @commands.command()
    async def reload(self, ext):
        for filename in os.listdir('./cogs'):
            if filename == ext:
                self.unload_extension('cogs.{}'.format(filename[:-3]))
                self.load_extension('cogs.{}'.format(filename[:-3]))
