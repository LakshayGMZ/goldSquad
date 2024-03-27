import concurrent.futures
import logging

import discord
from discord import app_commands
import dotenv
import discord_webhook
from discord.ext import commands
import os
import json
from discord_webhook import DiscordWebhook

dotenv.load_dotenv()


async def setup(bot):
    await bot.add_cog(Log(bot))


log_level = {
    'critical': logging.CRITICAL,
    'error': logging.ERROR,
    'info': logging.INFO,
    'debug': logging.DEBUG,
    'fatal': logging.FATAL,
    'warn': logging.WARN
}


class HttpLoggingHandler(logging.Handler):
    def __init__(self):
        self.url = os.environ['BOT_LOG_WEBHOOK']
        self.headers = {"Content-type": "application/json"}
        self.setLevel(log_level[os.environ['LOG_LEVEL']])
        self.setFormatter = logging.Formatter(json.dumps({
            'time': '%(asctime)s',
            'pathname': '%(pathname)s',
            'line': '%(lineno)d',
            'logLevel': '%(levelname)s',
            'message': '%(message)s'
        }, indent=4))
        super().__init__()

    def emit(self, record):
        data = self.format(record)
        embed = discord_webhook.DiscordEmbed(title=record.levelname, colour=0xec1313, description=f"```json\n{data}```")
        embed.set_timestamp()
        webhook = DiscordWebhook(url=self.url, rate_limit_retry=True)
        webhook.add_embed(embed)
        webhook.execute()


def start():
    start.logger = logging.getLogger('discord')
    start.logger.setLevel(log_level[os.environ['LOG_LEVEL']])
    httpHandler = HttpLoggingHandler()
    start.logger.addHandler(httpHandler)


class Log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            executor.submit(start)
            self.bot.logger = start.logger
            pass

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        start.logger.error(error)

    @commands.Cog.listener()
    async def on_application_command_error(self, interaction: discord.Interaction, error):
        start.logger.error(error)

    @commands.Cog.listener()
    async def on_app_command_completion(self, interaction: discord.Interaction, command):
        start.logger.info(
            f"{interaction.user.name} ({interaction.user.id}) used /{command.qualified_name}"
            # + "".join(f" {i['name']}: {i['value']}" for i in interaction.data["options"])
        )
