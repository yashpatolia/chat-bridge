import discord
from discord.ext import commands
from discord import app_commands
from config import ADMIN_ROLE

class Exec(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name='exec', description='executes a command')
    @app_commands.describe(command='command to run in game')
    @app_commands.checks.has_role(ADMIN_ROLE)
    async def exec(self, interaction: discord.Interaction, command: str) -> None:
        self.client.bot.chat(f'/{command}')
        embed = discord.Embed(colour=discord.Color.green(), description=f'**Executed:** `/{command}`')
        await interaction.response.send_message(embed=embed)

async def setup(client):
    client.add_cog(Exec(client))