import discord
import requests
import logging
import sqlite3
from discord.ext import commands
from discord import app_commands
from utils import get_uuid
from config import HYPIXEL_API_KEY

class Link(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name='link', description='Link Minecraft and Discord')
    @app_commands.describe(ign='Enter a Minecraft Username')
    async def link(self, interaction: discord.Interaction, ign: str) -> None:
        await interaction.response.defer()

        try:
            uuid = get_uuid(ign)
            data = requests.get(f'https://api.hypixel.net/v2/player?uuid={uuid}&key={HYPIXEL_API_KEY}').json()
            logging.debug(f'[GET] https://api.hypixel.net/v2/player?uuid={uuid}&key={HYPIXEL_API_KEY}')

            discord_name = data['socialMedia']['links']['DISCORD']
            if discord_name != interaction.user.name:
                embed = discord.Embed(
                    colour=discord.Colour.dark_red(),
                    description='Your discord in-game is not linked correctly.')
                await interaction.edit_original_response(embed=embed)
                return

            with sqlite3.connect("database.db") as connection:
                cursor = connection.cursor()
                connection.execute("PRAGMA foreign_keys = ON;")

                cursor.execute('SELECT discord_id FROM users WHERE uuid = ?', (uuid,))
                user_check = cursor.fetchone()[0]

                if user_check is not None:
                    embed = discord.Embed(
                        colour=discord.Colour.teal(),
                        description='**Link Status:** `already linked`')
                    await interaction.edit_original_response(embed=embed)
                    return

                cursor.execute('UPDATE users SET discord_id = ?, discord_name = ? WHERE uuid = ?',
                        (interaction.user.id, discord_name, uuid))
                connection.commit()

            embed = discord.Embed(
                colour=discord.Colour.dark_green(),
                description='**Link Status:** `successful`')
            await interaction.edit_original_response(embed=embed)

        except Exception as e:
            logging.error(e)
            embed = discord.Embed(
                colour=discord.Colour.dark_red(),
                description='**Link Status:** `error looking up ign`')
            await interaction.edit_original_response(embed=embed)