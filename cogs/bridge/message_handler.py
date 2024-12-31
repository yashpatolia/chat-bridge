import logging
import discord
from discord.ext import commands
from javascript import On
from config import OPTIONS, BRIDGE_WEBHOOK, LOGS_WEBHOOK

class MessageHandler(commands.Cog):
    def __init__(self, client):
        self.client = client

        @On(self.client.bot, 'messagestr')
        def messagestr(this, message, *args) -> None:
            logging.debug(f'[MC] {message}')
            bridge_webhook = discord.SyncWebhook.from_url(BRIDGE_WEBHOOK)
            logs_webhook = discord.SyncWebhook.from_url(LOGS_WEBHOOK)

            if OPTIONS['username'].lower() in message.lower():
                return

            if message.lower().startswith('you cannot say the same message twice!'):
                embed = discord.Embed(colour=discord.Colour.dark_red(), description='Duplicate Message!')
                bridge_webhook.send(embed=embed)
            elif message.lower().endswith('not found.'):
                embed = discord.Embed(colour=discord.Colour.red(), description=message)
                bridge_webhook.send(embed=embed)
            elif 'was promoted from' in message.lower() or 'was demoted from' in message.lower():
                embed = discord.Embed(colour=discord.Colour.dark_teal(), description=message)
                bridge_webhook.send(embed=embed)
                logs_webhook.send(embed=embed)
            elif 'is already in another guild!' in message.lower():
                embed = discord.Embed(colour=discord.Colour.red(), description=message)
                logs_webhook.send(embed=embed)
            elif 'was invited to the' in message.lower():
                embed = discord.Embed(colour=discord.Colour.orange(), description=message)
                logs_webhook.send(embed=embed)
            elif 'you invited' in message.lower() and 'to your guild' in message.lower():
                embed = discord.Embed(colour=discord.Colour.orange(), description=message)
                logs_webhook.send(embed=embed)
            elif 'joined the guild!' in message.lower():
                embed = discord.Embed(colour=discord.Colour.dark_green(), description=message)
                bridge_webhook.send(embed=embed)
                logs_webhook.send(embed=embed)
            elif 'left the guild!' in message.lower():
                embed = discord.Embed(colour=discord.Colour.red(), description=message)
                bridge_webhook.send(embed=embed)
                logs_webhook.send(embed=embed)
            elif 'has muted' in message.lower() and 'for' in message.lower():
                embed = discord.Embed(colour=discord.Colour.dark_purple(), description=message)
                bridge_webhook.send(embed=embed)
                logs_webhook.send(embed=embed)
            elif 'has unmuted' in message.lower():
                embed = discord.Embed(colour=discord.Colour.dark_magenta(), description=message)
                bridge_webhook.send(embed=embed)
                logs_webhook.send(embed=embed)
            elif 'was kicked from the guild' in message.lower():
                embed = discord.Embed(colour=discord.Colour.dark_red(), description=message)
                bridge_webhook.send(embed=embed)
                logs_webhook.send(embed=embed)

async def setup(client):
    client.add_cog(MessageHandler(client))