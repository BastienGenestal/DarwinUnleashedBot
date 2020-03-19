import os
from discord.ext import commands
from const import *


class DarwinBot(commands.Bot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)
        # Now self has client

        # Initializing constants
        self.server = None
        self.usefulChannels = {}
        self.usefulRoles = {}
        self.BracketRoles = {}
        self.usefulCustomEmotes = {}
        self.usefulBasicEmotes = {}
        self.usefulCogs = {}
        self.Sets = []

        self.medKitToPlayerMessageId = medKitToPlayerMessageId

        self.MAX_NB_PLAYER_PER_GAME = MAX_NB_PLAYER_PER_GAME

        # Non - constant variable initialization

        self.startASetMsg = None

        # Loading the server, channels, roles...
        for filename in os.listdir('./init'):
            if filename.endswith('.py'):
                self.load_extension('init.{}'.format(filename[:-3]))

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