import asyncio
from config import DataStorage
import dotenv
import os

from typing import Optional

import discord
from discord.ext import commands
from aiohttp import ClientSession

dotenv.load_dotenv()


class CustomBot(commands.Bot):
    def __init__(
        self,
        *args,
        db_pool: None,
        web_client: ClientSession,
        testing_guild_id: Optional[int] = None,
        main_guild_id: Optional[int] = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.db_pool = db_pool
        self.web_client = web_client
        self.testing_guild_id = testing_guild_id
        self.main_guild_id = main_guild_id
        self.configData: DataStorage = DataStorage(filename=os.environ["CONFIG_FILE"])
        self.help_command = None
        self.owner_ids=[]

    async def setup_hook(self) -> None:
        for extension in os.listdir(os.environ["COGS_PATH"]):
            if not extension.endswith('.py'):
                continue
            await self.load_extension(f'{os.environ["COGS_PATH"]}.{extension[:-3]}')
            print(f"loaded {extension}")

        if self.testing_guild_id:
            guild = discord.Object(self.testing_guild_id)
            # We'll copy in the global commands to test with:
            self.tree.copy_global_to(guild=guild)
            # followed by syncing to the testing guild.
            await self.tree.sync(guild=guild)
        else:
            await self.tree.sync()

        # This would also be a good place to connect to our database and
        # load anything that should be in memory prior to handling events.


async def main():
    async with ClientSession() as our_client:
        intents = discord.Intents.default()
        intents.message_content = True
        async with CustomBot(
            commands.when_mentioned,
            db_pool=None,
            web_client=our_client,
            intents=intents,
            testing_guild_id=None,
            main_guild_id=949137157778468914
        ) as bot:
            await bot.start(os.environ["BOT_TOKEN"])

if __name__ == "__main__":
    asyncio.run(main())
