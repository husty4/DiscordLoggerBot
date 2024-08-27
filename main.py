import logging
import disnake
from disnake.ext import commands
from dotenv import load_dotenv
import os

from logging.handlers import RotatingFileHandler
from Logging.EditMessageLogging import EditMessageLogging
from Logging.DeleteMessageLogging import DeleteMessageLogging

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

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


bot.add_cog(EditMessageLogging(bot))
bot.add_cog(DeleteMessageLogging(bot))

bot.load_extensions("cogs")
bot.load_extensions("Modules")
bot.load_extensions("Modals")


bot.run(TOKEN)