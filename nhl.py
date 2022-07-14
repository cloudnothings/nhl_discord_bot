import json

import requests
from discord import File
from discord.ext import commands, tasks

from formatter import show_recent_results, json_to_excel, create_text_file


class NHL(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # TODO: Replace with the channel ID to send the data to (as int literal)
        self.CHANNEL_ID = 0
        self.get_nhl_data.start()

    @commands.command(name='matches')
    async def _matches(self, ctx, club_id: str = None):
        async with ctx.typing():
            data = self.get_match_data(club_id=club_id)
            message = await self.get_matches(data=data, club_id=club_id)
        await ctx.send(message)

    @commands.command(name='rawdata')
    async def _rawdata(self, ctx, club_id: str = None):
        async with ctx.typing():
            message = await self.get_match_data(club_id)
        await ctx.send(message)

    @classmethod
    async def get_match_data(cls, club_id):
        url = f'https://proclubs.ea.com/api/nhl/clubs/matches?clubIds={club_id}' \
              f'&platform=xbox-series-xs&matchType=club_private'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
        response = requests.get(url, headers=headers)
        return json.loads(response.content)

    @classmethod
    async def get_matches(cls, **kwargs):
        return show_recent_results(kwargs.get('data'), kwargs.get('club_id'))

    @tasks.loop(minutes=30)
    async def get_nhl_data(self):
        # TODO: Add clubs IDs as needed
        club_ids = [
            '21230'  # ,
            # '69420',
            # '696969,
            # '611275'
        ]
        data = await self.get_match_data(club_ids[0])
        if len(club_ids) > 1:
            for i in range(1, len(club_ids)):
                data += self.get_match_data(club_ids[i])
        # TODO: adjust line if you'd like to send a CSV to the chat instead of raw json
        data = json.dumps(data)  # or data = json_to_excel(data)
        if len(data) < 500:
            await self.send_message_to_channel(data, channel_id=self.CHANNEL_ID)
        else:
            data = create_text_file(data, 'results')
        if isinstance(data, File):
            await self.send_file_to_channel(file=data, channel_id=self.CHANNEL_ID)
        else:
            await self.send_message_to_channel('Failed to convert to file.', channel_id=self.CHANNEL_ID)

    @get_nhl_data.before_loop
    async def before_get_nhl_data(self):
        print('waiting to load get_nhl_data_periodically')
        await self.bot.wait_until_ready()

    async def send_message_to_channel(self, message, channel_id):
        channel = self.bot.get_channel(channel_id)
        await channel.send(message)

    async def send_file_to_channel(self, file, channel_id):
        channel = self.bot.get_channel(channel_id)
        await channel.send(file=file)


def setup(self):
    self.add_cog(NHL(self))
