import os
from discord.ext import commands
from const import codesChannelName, minutesToChoseAClass, medKitRoleName, BRACKETS, reaction_numbers, adminBotCommandChan, classEmojis

class DarwinBot(commands.Bot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)
        # Now self has client

        # Initializing constants
        self.BRACKETS = BRACKETS
        self.reaction_numbers = reaction_numbers
        self.classEmojis = classEmojis
        self.adminBotCommandChan = adminBotCommandChan
        self.medKitRoleName = medKitRoleName
        self.minutesToChoseAClass = minutesToChoseAClass
        self.codesChannelName = codesChannelName

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
