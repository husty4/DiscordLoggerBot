from disnake.ext import commands
from Database.database import get_banwords

class MessageCheckCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        guild_id = message.guild.id
        banned_words = get_banwords(guild_id)

        for word in banned_words:
            if word in message.content:
                await message.delete()

def setup(bot):
    bot.add_cog(MessageCheckCog(bot))
