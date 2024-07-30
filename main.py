import logging
import disnake
from disnake.ext import commands
from dotenv import load_dotenv
import os

from Logging.MessageLogging import log_message, log_message_delete
from Logging.VoiceStateLogging import log_voice_state_update
from logging.handlers import RotatingFileHandler

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

#Logging settings for text messages
message_logger = logging.getLogger('message_logger')
message_logger.setLevel(logging.INFO)
message_handler = RotatingFileHandler('logs/message_log.txt', maxBytes=10485760, backupCount=5, encoding='utf-8')
message_formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%d-%m-%Y, %H:%M:%S')
message_handler.setFormatter(message_formatter)
message_logger.addHandler(message_handler)

#Logging setting for delete messages
delete_logger = logging.getLogger('delete_logger')
delete_logger.setLevel(logging.INFO)
delete_handler = RotatingFileHandler('logs/delete_message_log.txt', maxBytes=10485760, backupCount=5, encoding='utf-8')
delete_formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%d-%m-%Y, %H:%M:%S')
delete_handler.setFormatter(message_formatter)
delete_logger.addHandler(message_handler)

#Logging settings for voice
voice_logger = logging.getLogger('voice_logger')
voice_logger.setLevel(logging.INFO)
voice_handler = RotatingFileHandler('logs/voice_log.txt', maxBytes=10485760, backupCount=5, encoding='utf-8')
voice_formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%d-%m-%Y, %H:%M:%S')
voice_handler.setFormatter(voice_formatter)
voice_logger.addHandler(voice_handler)

intents = disnake.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix="/", intents=disnake.Intents.all())

#Status checker
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
#Message logger
@bot.event
async def on_message(message):
    log_message(message)
    await bot.process_commands(message)
    global last_channel
    last_channel = message.channel

#Message delete logger
@bot.event
async def on_message_delete(message):
    log_message_delete(message)

#Voice logger
@bot.event
async def on_voice_state_update(member, before, after):
    log_voice_state_update(member, before, after)

bot.load_extensions("cogs")

bot.run(TOKEN)