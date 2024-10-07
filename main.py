import disnake
from disnake.ext import commands
from dotenv import load_dotenv
import os

from Database.database import create_guild_table
from Logging.EditMessageLogging import EditMessageLogging
from Logging.DeleteMessageLogging import DeleteMessageLogging

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

intents = disnake.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix="/", intents=disnake.Intents.all(), activity=disnake.Activity(type=disnake.ActivityType.watching, name="Breaking bad"))

@bot.event
async def on_guild_join(guild):
    guild_id = guild.id
    create_guild_table(guild_id)
    print(f"Создана таблица для сервера {guild.name} (ID: {guild_id})")


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