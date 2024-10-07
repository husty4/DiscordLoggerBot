import disnake
from disnake.ext import commands
import datetime

class DeleteMessageLogging(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        @bot.event
        async def on_message_delete(message: disnake.Message):
            channel_log = bot.get_channel(1277253541949472819)
            ctx = await bot.get_context(message)
            if message.author.bot:
                return
            time = (disnake.utils.format_dt(datetime.datetime.now(), style="D"))
            embed = disnake.Embed(title=f"Message delete", description=f"Author: {message.author.mention} \nChanel {message.channel.mention} \nTime {time}", color=disnake.Colour.red())
            embed.add_field(name="Context: ", value=f"> {message.content}", inline=False)
            embed.set_thumbnail(url=message.author.display_avatar)
            await channel_log.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(DeleteMessageLogging(bot))