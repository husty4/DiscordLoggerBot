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

intents = disnake.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix="/", intents=disnake.Intents.all())


#Logging settings for text messages
def setup_message_logger(folder_path):
    log_file_path = os.path.join(folder_path, "message_log.txt")
    message_logger = logging.getLogger('message_logger')
    message_logger.setLevel(logging.INFO)
    message_handler = RotatingFileHandler(log_file_path ,maxBytes=10485760, backupCount=5, encoding='utf-8')
    message_formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%d-%m-%Y, %H:%M:%S')
    message_handler.setFormatter(message_formatter)
    message_logger.addHandler(message_handler)
    message_logger.info("Message logger initialized")
    return message_logger

#Logging setting for delete messages
def setup_delete_logger(folder_path):
    log_file_path = os.path.join(folder_path, 'delete_message_log.txt')
    delete_logger = logging.getLogger('delete_logger')
    delete_logger.setLevel(logging.INFO)
    delete_handler = RotatingFileHandler(folder_path, '/delete_message_log.txt', maxBytes=10485760, backupCount=5, encoding='utf-8')
    delete_formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%d-%m-%Y, %H:%M:%S')
    delete_handler.setFormatter(delete_formatter)
    delete_logger.addHandler(delete_formatter)
    delete_logger.info("delete logger initialized")
    return delete_logger

#Logging settings for voice
def setup_voice_logger(folder_path):
    log_file_path = os.path.join(folder_path, 'delete_message_log.txt')
    voice_logger = logging.getLogger(f'{folder_path}_voice_logger')
    voice_logger.setLevel(logging.INFO)
    voice_handler = RotatingFileHandler(folder_path, 'voice_log.txt', maxBytes=10485760, backupCount=5, encoding='utf-8')
    voice_formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%d-%m-%Y, %H:%M:%S')
    voice_handler.setFormatter(voice_formatter)
    voice_logger.addHandler(voice_handler)
    voice_logger.info("Voice logger initialized")
    return voice_logger

@bot.event
async def on_guild_join(guild):
    folder_path = os.path.join('server_data', str(guild.id))
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    setup_message_logger(folder_path)
    setup_delete_logger(folder_path)
    setup_voice_logger(folder_path)

    print(f"Bot joined the server: {guild.name} (ID: {guild.id}). Loggers set up")

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
    #log_message_delete(message)
    delete_logger = logging.getLogger('delete_logger')
    delete_logger.info(f"Message deleted: {message.content} by {message.author}"
                       )

#Voice logger
@bot.event
async def on_voice_state_update(member, before, after):
    log_voice_state_update(member, before, after)
    voice_logger = logging.getLogger('voice_logger')

bot.load_extensions("cogs")
bot.load_extensions("Modules")


bot.run(TOKEN)