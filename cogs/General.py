import time

from discord.ext import commands

from main import CustomBot


async def setup(bot):
    await bot.add_cog(General(bot))


class General(commands.Cog):
    def __init__(self, bot: CustomBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('\n---------')
        print('Logged in as')
        print(self.bot.user.name)
        print(self.bot.user.id)
        print('---------')
        self.bot.start_time = int(round(time.time()))