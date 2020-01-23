from DarwinBot import DarwinBot
import os

client = DarwinBot(command_prefix='')

client.run(os.environ.get('BOT_TOKEN'))
#client.run('NjY5NDkxNTM0NDMyOTYwNTIy.XimSEA.pxpRGpvqPqwIH9aZ9EM3ZAzOKz8')
