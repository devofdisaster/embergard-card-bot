from dotenv import load_dotenv
from discord import Intents, Client
import os
import logging

load_dotenv()

log_handler = logging.FileHandler(filename='card-bot.log', encoding='utf-8', mode='a', )

intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('((') and message.content.endswith('))'):
        content = message.content.lstrip('( ').rstrip(' )')
        await message.channel.send(f'Thou hath written {content}')

client.run(os.getenv('CLIENT_TOKEN'), log_handler=log_handler, log_level=logging.DEBUG)