from DarwinBot import DarwinBot
import os

client = DarwinBot(command_prefix='')
client.run(os.environ.get('TOKEN'))
