import os
from discord.ext import commands
from const import *


class DarwinBot(commands.Bot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)
        # Now self has client

        # Initializing constants
        self.ServerId = ServerId
        self.usefullChannels = {}
        self.usefullRoles = {}
        self.platformEmojis = platformEmojis
        self.regionEmojis = regionEmojis

        self.classEmojis = classEmojis
        self.classEmojisId = classEmojisId
        self.signUpEmoji = signUpEmoji

        self.minutesToChoseAClass = minutesToChoseAClass
        self.maxActivePlayers = maxActivePlayers

        self.regions = regions
        self.platforms = platforms

        self.medKitToPlayerMessageId = medKitToPlayerMessageId
        self.regionSelectionMessageId = regionSelectionMessage
        self.platformSelectionMessageId = platformSelectionMessage

        # Non - constant variable initialization

        self.signUpMessage = None
        self.server = None

        # Loading cogs
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                self.load_extension('cogs.{}'.format(filename[:-3]))

    class MissingSomething(Exception):
        def __init__(self, *args):
            if args:
                self.message = args[0]
            else:
                self.message = None

        def __str__(self):
            if self.message:
                return 'MissingSomething, {0} '.format(self.message)
            else:
                return 'MissingSomething has been raised'