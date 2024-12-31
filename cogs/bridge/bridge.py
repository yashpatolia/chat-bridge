import asyncio
import discord
import re
import logging
import emoji
from discord.ext import commands
from javascript import On
from config import OPTIONS, BRIDGE_WEBHOOK, OFFICER_WEBHOOK, BRIDGE_CHANNEL_ID, OFFICER_CHANNEL_ID

class Bridge(commands.Cog):
    def __init__(self, client):
        self.client = client

        @On(self.client.bot, 'chat')
        def handle_message(this, chat, message, *args) -> None:
            if chat in ['Guild', 'Officer']:
                bridge_webhook = discord.SyncWebhook.from_url(BRIDGE_WEBHOOK)
                officer_webhook = discord.SyncWebhook.from_url(OFFICER_WEBHOOK)

                if message.split(' ')[-1] in ['joined', 'left'] and OPTIONS['username'].lower() not in message.lower():
                    embed = discord.Embed(description=message)
                    embed.colour = discord.Colour.green() if message.split(' ')[-1] == 'joined.' else discord.Colour.red()
                    bridge_webhook.send(embed=embed)
                    return

                try:
                    match = re.search(r"^(?:\[(?P<rank>.+?)\])?\s?(?P<player>.+?)\s?(?:\[(?P<guild_rank>.+?)\])?: (?P<message>.*)$", message)
                    message = re.sub('@', '', match.group('message'))
                    username = match.group("player")

                    logging.debug(f'[MC] {username}: {message}')
                    if chat == 'Guild':
                        bridge_webhook.send(message, username=username, avatar_url=f'https://mc-heads.net/avatar/{username}')
                    elif chat == 'Officer':
                        officer_webhook.send(message, username=username, avatar_url=f'https://mc-heads.net/avatar/{username}')
                except Exception as e:
                    logging.error(e)
                    return

    @commands.Cog.listener()
    async def on_message(self, message) -> None:
        if message.author.bot or len(message.content) > 250 or len(message.content) <= 0:
            return

        if message.channel.id in [BRIDGE_CHANNEL_ID, OFFICER_CHANNEL_ID]:
            await asyncio.sleep(1)
            logging.debug(f'[D] {message.author.display_name}: {message.content}')

            message.content = emoji.demojize(message.clean_content)
            message.content = re.sub(r'<[^:]*(:[^:]+:)\d+>', r'\1', message.content)

            if message.type == discord.MessageType.reply:
                reply_message = await message.channel.fetch_message(message.reference.message_id)
                message.content = f'{message.author.display_name} replied to {reply_message.author.display_name}: {message.content}'
            else:
                message.content = f'{message.author.display_name}: {message.content}'

            if message.channel.id == BRIDGE_CHANNEL_ID:
                self.client.bot.chat(f'/gc {message.content}')
            elif message.channel.id == OFFICER_CHANNEL_ID:
                self.client.bot.chat(f'/oc {message.content}')

async def setup(client):
    await client.add_cog(Bridge(client))