import time

import discord.ext.commands
from discord.ext import commands
from discord import app_commands
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

    @app_commands.command(name="add")
    @app_commands.describe(
        first_value='The first value you want to add something to',
        second_value='The value you want to add to the first value',
    )
    async def add(self, interaction: discord.Interaction, first_value: int, second_value: int):
        self.bot.configData.setLockTime("00")
        self.bot.configData.setUnlockTime("01")
        self.bot.configData.addLockedChannels("lol1")
        self.bot.configData.addLockedChannels("lol2")
        self.bot.configData.removeLockedChannels("lol1")
        print(self.bot.configData.getLockedChannels())

        await interaction.response.send_message(f'{first_value} + {second_value} = {first_value + second_value}')
