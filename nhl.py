import json

import requests
from discord import File
from discord.ext import commands, tasks

from formatter import json_to_csv, create_text_file


async def get_match_data(club_id):
    """Returns json of last 5 games of specified club_id"""
    url = 'https://proclubs.ea.com/api/nhl/clubs/matches'
    query = f'?clubIds={club_id}&platform=xbox-series-xs&matchType=club_private'
    headers = {  # user agent of browser seems to work
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    response = requests.get(url + query, headers=headers)
    return json.loads(response.content)


class NHL(commands.Cog):
    def __init__(self, bot):
        """NHL Constructor"""
        self.bot = bot
        # TODO: Replace with the channel ID to send the data to (as int literal)
        self.CHANNEL_ID = 0
        # TODO: Add clubs IDs as needed
        self.CLUB_IDS = [
            '21230'  # ,
            # '69420',
            # '696969,
            # '611275'
        ]
        self.sync_nhl_data.start()

    @commands.command(name='rawdata')
    async def _rawdata(self, ctx, club_id):
        """rawdata command takes in a club ID as its sole argument.
        sends results.json file of the clubs 5 most recent matches to the calling user's chat"""
        async with ctx.typing():
            data_as_json = await get_match_data(club_id)
            data_as_string = json.dumps(data_as_json)
            data_as_file = create_text_file(data_as_string, 'results.json')
        if isinstance(data_as_file, File):
            await ctx.send(file=data_as_file)
        else:
            await ctx.send('Failed to convert to file.')

    async def get_data_all_clubs(self):
        """Returns json obj of last 5 matches of all clubs in CLUB_IDS"""
        data = await get_match_data(self.CLUB_IDS[0])
        if len(self.CLUB_IDS) > 1:
            for i in range(1, len(self.CLUB_IDS)):
                data += get_match_data(self.CLUB_IDS[i])
        return data

    # TODO: Feel free to adjust the interval at which the data is synced
    @tasks.loop(minutes=30)
    async def sync_nhl_data(self):
        """Intended use is as follows:
        1. Periodically pulls recent matches from all defined clubs as json
        2. Process the json to get only necessary data
        3. Upload data to Google Sheets API"""
        data = await self.get_data_all_clubs()
        # TODO: Implement json to csv function
        data = json.dumps(data)  # data = json_to_csv(data)
        data = create_text_file(data, 'results.json')
        if isinstance(data, File):
            # TODO: Implement API call to send csv to Google Sheets, or update cells programmatically
            await self.send_file_to_channel(file=data, channel_id=self.CHANNEL_ID)
        else:
            await self.send_message_to_channel('Failed to convert to file.', channel_id=self.CHANNEL_ID)

    @sync_nhl_data.before_loop
    async def before_sync_nhl_data(self):
        print('waiting to load sync_nhl_data')
        await self.bot.wait_until_ready()

    async def send_message_to_channel(self, message, channel_id):
        """Sends any string to specific channel id"""
        channel = self.bot.get_channel(channel_id)
        await channel.send(message)

    async def send_file_to_channel(self, file, channel_id):
        """Sends any file to specified channel id"""
        channel = self.bot.get_channel(channel_id)
        await channel.send(file=file)


def setup(self):
    """initializes cog"""
    self.add_cog(NHL(self))
