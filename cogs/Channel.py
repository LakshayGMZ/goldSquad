from discord.ext import commands
from main import CustomBot

async def setup(bot):
    await bot.add_cog(General(bot))


class General(commands.Cog):
    def __init__(self, bot: CustomBot):
        self.bot = bot