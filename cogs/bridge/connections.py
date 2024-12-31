import discord
import asyncio
import logging
from discord.ext import commands
from javascript import Once, On
from config import OPTIONS, BRIDGE_WEBHOOK

class Connections(commands.Cog):
    def __init__(self, client):
        self.client = client

        @Once(self.client.bot, 'spawn')
        def spawn(this) -> None:
            logging.debug(f"[Bot] Logged in as {OPTIONS['username']}")
            bridge_webhook = discord.SyncWebhook.from_url(BRIDGE_WEBHOOK)
            embed = discord.Embed(
                description=f"**Connected to:** `{OPTIONS['host']}`",
                colour=discord.Colour.dark_green())
            bridge_webhook.send(embed=embed)

        @On(self.client.bot, 'end')
        def end(this, event) -> None:
            if self.client.reason == 'relog':
                return

            logging.debug(f"[Bot] Disconnected from {OPTIONS['host']}")
            bridge_webhook = discord.SyncWebhook.from_url(BRIDGE_WEBHOOK)
            embed = discord.Embed(
                description=f"**Disconnected from:** `{OPTIONS['host']}`\nRestarting `{OPTIONS['username']}` in 5 seconds!",
                colour=discord.Colour.orange())
            bridge_webhook.send(embed=embed)

            async def reconnect():
                await asyncio.sleep(5)
                await self.client.start_mineflayer(restart=True)
            asyncio.run(reconnect())

async def setup(client):
    client.add_cog(Connections(client))