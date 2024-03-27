import asyncio
import datetime
import discord.utils
from config import DataStorage
from discord.ext import commands, tasks
from main import CustomBot
import os
from dotenv import load_dotenv

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
timeUnlock = timeUnlock.time().replace(tzinfo=MST())

# roles = ["949453820893728838", "949866744158236742", "949433355479421008"]
roles = [944510057784168540, 967661896658460783]


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
            await channel.send(content=_bot.configData.getLockedMessageBody())
            await channel.edit(overwrites=overwriteDict)
        except discord.NotFound:
            _bot.logger.warning("Found invalid Channel id: " + channelID)
            continue
    _bot.logger.info("locked Channels")


@tasks.loop(time=timeUnlock)
async def unlockChannelTask(_bot: CustomBot):
    await asyncio.sleep(10)
    guild = await _bot.fetch_guild(_bot.main_guild_id)
    overwriteDict = {}
    for roleID in roles:
        role = guild.get_role(roleID)
        overwriteDict[role] = discord.PermissionOverwrite(send_messages=None)

    for channelID in _bot.configData.getLockedChannels():
        try:
            channel = await _bot.fetch_channel(channelID)
            await channel.edit(overwrites=overwriteDict)
            await channel.send(content=_bot.configData.getUnlockedMessageBody())
        except discord.NotFound:
            _bot.logger.warning("Found invalid Channel id: " + channelID)
            continue
    _bot.logger.info("Unlocked Channels")



class Scheduler(commands.Cog):
    def __init__(self, bot: CustomBot):
        self.bot = bot

        lockChannelTask.start(self.bot)
        unlockChannelTask.start(self.bot)

    def cog_unload(self):
        lockChannelTask.cancel()
        unlockChannelTask.cancel()
