import datetime
import os

import discord.utils
from discord.ext import commands, tasks
from dotenv import load_dotenv

from config import DataStorage
from main import CustomBot

load_dotenv()
dataStore = DataStorage(filename=os.environ["CONFIG_FILE"])


async def setup(bot):
    await bot.add_cog(Scheduler(bot))


class MST(datetime.tzinfo):
    def utcoffset(self, dt):
        return datetime.timedelta(hours=-6)

    def dst(self, dt):
        return datetime.timedelta(0)

    def tzname(self, dt):
        return "MST"


timeLock = datetime.datetime.strptime(dataStore.getLockTime(), '%H:%M')
timeLock = timeLock.time().replace(tzinfo=MST())

timeUnlock = datetime.datetime.strptime(dataStore.getUnlockTime(), '%H:%M')
timeDelete = timeUnlock + datetime.timedelta(hours=1)

timeUnlock = timeUnlock.time().replace(tzinfo=MST())
timeDelete = timeDelete.time().replace(tzinfo=MST())

roles = [
    949453820893728838,
    949866744158236742,
    949433355479421008
]


@tasks.loop(time=timeLock)
async def lockChannelTask(_bot: CustomBot):
    guild = await _bot.fetch_guild(_bot.main_guild_id)
    overwriteDict = {}
    for roleID in roles:
        role = guild.get_role(roleID)
        overwriteDict[role] = discord.PermissionOverwrite(send_messages=False)

    for channelID in _bot.configData.getLockedChannels():
        try:
            channel = await _bot.fetch_channel(channelID)
            message = await channel.send(content=_bot.configData.getLockedMessageBody())
            await channel.edit(overwrites=overwriteDict)

            _bot.configData.addMessageIds(str(channel.id) + "-" + str(message.id))
        except discord.NotFound:
            _bot.logger.warning("Found invalid Channel id: " + channelID)
            continue
    _bot.logger.info("locked Channels")


@tasks.loop(time=timeUnlock)
async def unlockChannelTask(_bot: CustomBot):
    await deleteMessageTask(_bot)

    guild = await _bot.fetch_guild(_bot.main_guild_id)
    overwriteDict = {}
    for roleID in roles:
        role = guild.get_role(roleID)
        overwriteDict[role] = discord.PermissionOverwrite(send_messages=None)

    for channelID in _bot.configData.getLockedChannels():
        try:
            channel = await _bot.fetch_channel(channelID)
            await channel.edit(overwrites=overwriteDict)
            message = await channel.send(content=_bot.configData.getUnlockedMessageBody())

            _bot.configData.addMessageIds(str(channel.id) + "-" + str(message.id))
        except discord.NotFound:
            _bot.logger.warning("Found invalid Channel id: " + channelID)
            continue
    _bot.logger.info("Unlocked Channels")


@tasks.loop(time=timeDelete)
async def deleteMessageTask(_bot: CustomBot):
    for combinedID in _bot.configData.getMessageIds():
        channelID, messageID = combinedID.split("-")
        try:
            channel = _bot.get_partial_messageable(channelID)
            message = channel.get_partial_message(messageID)
            await message.delete()
        except discord.NotFound:
            _bot.logger.warning("Found invalid message id: " + messageID)
            continue
    _bot.configData.clearMessageIds()
    _bot.logger.info("Deleted Messages")


class Scheduler(commands.Cog):
    def __init__(self, bot: CustomBot):
        self.bot = bot

        lockChannelTask.start(self.bot)
        unlockChannelTask.start(self.bot)
        deleteMessageTask.start(self.bot)

    def cog_unload(self):
        lockChannelTask.stop()
        unlockChannelTask.stop()
        deleteMessageTask.stop()
