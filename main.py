import discord
import asyncio
import os
import logging
from javascript import require
from discord.ext import commands
from config import OPTIONS, TOKEN

mineflayer = require("mineflayer")
logging.basicConfig(level=logging.INFO)

class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="+", intents=discord.Intents.all())
        self.bot = None

    async def start_mineflayer(self):
        self.bot = mineflayer.createBot(OPTIONS)

    async def setup_hook(self):
        await self.start_mineflayer()

        for folder in os.listdir("cogs"):
            for file in os.listdir(f"cogs/{folder}"):
                if file.endswith(".py"):
                    await self.load_extension(f"cogs.{folder}.{file[:-3]}")

    async def on_ready(self):
        logging.info(f"Logged in as {self.user.name} (ID: {self.user.id})")
        synced = await self.tree.sync()
        logging.info(f"Synced {len(synced)} slash commands!")


async def run_bot():
    async with Client() as client:
        await client.start(TOKEN)


asyncio.run(run_bot())