import datetime
import os
import discord
from discord.ext import commands
from pip._vendor import requests


class ImgDL(commands.Cog):
    def __init__(self, client):
        self.client = client

    ## https://github.com/PvtSeaCow/Discord-AutoDownloader/blob/10151c39b318f97c652dffc07145bdc86e12045c/auto.py#L160
    async def download_file(self, url, path, file_name, file_type='png'):
        if not os.path.exists('.\\tempFiles\\pictures\\' + path):
            os.makedirs('.\\tempFiles\\pictures\\' + path)
        headers = {
            'User-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'
        }
        r = requests.get(url, headers=headers, stream=True)
        with open('.\\tempFiles\\pictures\\' + path + '\\' + str(file_name) + '.' + str(file_type), 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.channel != self.client.usefulChannels['enterCodesChan']:
            return
        title = msg.content
        if not title:
            title = datetime.datetime.now().strftime("%H_%M_%S_%b_%d")
        if msg.attachments:
            url = msg.attachments[0].url
            try:
                await self.download_file(url, 'screenshots', title)
            except Exception as e:
                print(e)
            for img in os.listdir('./tempFiles/pictures/screenshots'):
                print(img)
                with open('./tempFiles/pictures/screenshots/{}'.format(img), 'rb') as f:
                    await self.client.usefulChannels['logsChan'].send('I stored:\n{}'.format(img), file=discord.File(f))
        ###
        # Download the image in ../tempFiles
        # Run Philipeace code with the image
        # Extract the scores from it
            #img = msg.getImg()
            #yourCode(img)



def setup(client):
    client.add_cog(ImgDL(client))
