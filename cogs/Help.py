from discord import Embed
from discord import Interaction
from discord import app_commands
from discord.ext import commands

from main import CustomBot


async def setup(bot):
    await bot.add_cog(Help(bot))


def mention_slash(name: str, _id):
    return f"<:point:1017790082729644112> </{name}:{str(_id)}>"


class Help(commands.Cog):
    def __init__(self, bot: CustomBot):
        self.bot = bot

    @app_commands.command(name="help", description="Detailed help command for bot")
    async def help(self, interaction: Interaction):
        allCommands = await self.bot.tree.fetch_commands(guild=interaction.guild)
        channelID = "1223127275206086778"
        helpID = "1223127274673541225"

        embed = Embed(title="Help Menu", description="commands list of the bot.", color=0x2f3136)
        embed.add_field(name=mention_slash("channel add", channelID),
                        value=f'> ```Add a channel to the auto-lock list```', inline=False)
        embed.add_field(name=mention_slash("channel remove", channelID),
                        value=f'> ```Remove a channel from the auto-lock list```', inline=False)
        embed.add_field(name=mention_slash("channel add-lock-time", channelID),
                        value=f'> ```Set a time to auto-lock the channels in MST.```', inline=False)
        embed.add_field(name=mention_slash("channel add-unlock-time", channelID),
                        value=f'> ```Set a time to auto-unlock the channels in MST.```', inline=False)
        embed.add_field(name=mention_slash("channel lock-message", channelID),
                        value=f'> ```Set the message that will be sent before locking the channels.```', inline=False)
        embed.add_field(name=mention_slash("channel unlock-message", channelID),
                        value=f'> ```Set the message that will be sent after unlocking the channels.```', inline=False)
        embed.add_field(name=mention_slash("help", helpID),
                        value=f'> ```Set the message that will be sent before locking the channels.```', inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)
