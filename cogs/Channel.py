import datetime
import os
import dotenv
from .scheduler import MST
import discord
import json
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Range
from main import CustomBot

dotenv.load_dotenv()


async def setup(bot):
    await bot.add_cog(Channel(bot))


def is_bot_owner():
    async def predicate(interaction: discord.Interaction):
        if interaction.user.id not in json.loads(os.environ["OWNER_IDS"]):
            raise app_commands.MissingPermissions(['Bot Owner'])
        return True

    return app_commands.check(predicate)


class Channel(commands.GroupCog, name="channel", description="Manage auto locking/unlocking of channels"):
    def __init__(self, bot: CustomBot):
        self.bot = bot
        self.timeout = 15

    @app_commands.command(name="add", description="Add a channel to the auto-lock list")
    @app_commands.describe(channel="The channel to add to the auto-lock list")
    @is_bot_owner()
    async def add_channel(self, interaction: discord.Interaction, channel: str):
        if self.bot.configData.addLockedChannels(channel):
            await interaction.response.send_message(content="Added to locked channels :white_check_mark:", ephemeral=True)
        else:
            await interaction.response.send_message(content="Channel already present in locked channels :x:", ephemeral=True)

    @add_channel.autocomplete('channel')
    async def add_channel_autocomplete(self, interaction: discord.Interaction, current: str):
        allChannels = await self.bot.fetch_guild(interaction.guild_id)
        allChannels = await allChannels.fetch_channels()
        lockedChannels = self.bot.configData.getLockedChannels()
        return [app_commands.Choice(name=chann.name, value=str(chann.id))
                for chann in allChannels if (
                        isinstance(chann, discord.TextChannel) and
                        chann.name.startswith(current) and
                        str(chann.id) not in lockedChannels
                )]

    @app_commands.command(name="remove", description="Remove a channel from the auto-lock list")
    @app_commands.describe(channel="The channel to remove from the auto-lock list")
    @is_bot_owner()
    async def remove_channel(self, interaction: discord.Interaction, channel: str):
        if self.bot.configData.removeLockedChannels(channel):
            await interaction.response.send_message(content="Removed from locked Channels :white_check_mark:", ephemeral=True)
        else:
            await interaction.response.send_message(content="Channel not in locked channels :x:", ephemeral=True)

    @remove_channel.autocomplete('channel')
    async def remove_channel_autocomplete(self, interaction: discord.Interaction, current: str):
        lockedChannels = [(await self.bot.fetch_channel(int(i))) for i in self.bot.configData.getLockedChannels()]
        return [app_commands.Choice(name=chann.name, value=str(chann.id))
                for chann in lockedChannels if chann.name.startswith(current)]

    @app_commands.command(name="add-lock-time", description="Add a time to auto-lock the channels in MST.")
    @app_commands.describe(
        hours="Enter the hour part of lock time in 24 hr format",
        minutes="Enter the minute part of lock time."
    )
    @is_bot_owner()
    async def add_lock_time(self, interaction: discord.Interaction, hours: Range[int, 0, 23],
                            minutes: Range[int, 0, 59]):
        timeObj = datetime.time(hour=hours, minute=minutes, tzinfo=MST())
        # lockChannelTask.change_interval(time=timeObj)
        self.bot.configData.setLockTime(timeObj.strftime('%H:%M'))
        await self.bot.reload_extension(f'{os.environ["COGS_PATH"]}.scheduler')
        await interaction.response.send_message(content="Lock time set successfully :white_check_mark:", ephemeral=True)

    @app_commands.command(name="add-unlock-time", description="Add a time to auto-unlock the channels in MST.")
    @app_commands.describe(
        hours="Enter the hour part of unlock time in 24 hr format",
        minutes="Enter the minute part of unlock time."
    )
    @is_bot_owner()
    async def add_unlock_time(self, interaction: discord.Interaction, hours: Range[int, 0, 23],
                              minutes: Range[int, 0, 59]):
        timeObj = datetime.time(hour=hours, minute=minutes, tzinfo=MST())
        self.bot.configData.setUnlockTime(timeObj.strftime('%H:%M'))
        await self.bot.reload_extension(f'{os.environ["COGS_PATH"]}.scheduler')
        await interaction.response.send_message(content="Unlock time set successfully :white_check_mark:", ephemeral=True)

    @app_commands.command(name="lock-message", description="Set the message that will be sent before locking the channels.")
    @is_bot_owner()
    async def set_lock_message(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f'Please Send the chanel lock message after this. You have {str(self.timeout)} seconds to repond!!')
        try:
            con = await self.bot.wait_for('message', check=lambda
                m: m.author.id == interaction.user.id and interaction.channel.id == m.channel.id, timeout=self.timeout)
        except TimeoutError:
            pass
        else:
            if not con:
                return
            await interaction.edit_original_response(content="The lock message was set Successfully :white_check_mark:")
            self.bot.configData.setLockMessageBody(con.content)

    @app_commands.command(name="unlock-message", description="Set the message that will be sent after unlocking the channels.")
    @is_bot_owner()
    async def set_unlock_message(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f'Please Send the channel unlock message after this. You have {str(self.timeout)} seconds to repond!!')
        try:
            con = await self.bot.wait_for('message', check=lambda
                m: m.author.id == interaction.user.id and interaction.channel.id == m.channel.id, timeout=self.timeout)
        except TimeoutError:
            pass
        else:
            if not con:
                return

            await interaction.edit_original_response(content="The unlock message was set Successfully :white_check_mark:")
            self.bot.configData.setUnlockMessageBody(con.content)

    async def cog_app_command_error(
            self,
            interaction: discord.Interaction,
            error: app_commands.AppCommandError
    ):
        if isinstance(error, discord.app_commands.MissingPermissions):
            await interaction.response.send_message(content=error, ephemeral=True)
