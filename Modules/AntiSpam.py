from disnake.ext import commands
from disnake import Message
import disnake
import time

class AntiSpam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_messages = {}

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author.bot:
            return

        user_id = message.author.id
        content = message.content
        current_time = time.time()

        if user_id in self.user_messages:
            last_message, last_time = self.user_messages[user_id]

            if content == last_message and current_time - last_time < 10:
                await message.delete()
                return
        self.user_messages[user_id] = (content, current_time)

    async def on_message_edit(self, before: Message, after: Message):
        await self.on_message(after)

def setup(bot):
    bot.add_cog(AntiSpam(bot))