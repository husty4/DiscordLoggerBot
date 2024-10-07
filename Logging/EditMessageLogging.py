import disnake
from disnake.ext import commands
import datetime

class EditMessageLogging(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        @bot.event
        async def on_message_edit(before: disnake.Message, after: disnake.Message):
            channel_log = bot.get_channel(1277249730728038480)
            if after.author.bot:
                return
            time = (disnake.utils.format_dt(datetime.datetime.now(), style='D'))
            embed = disnake.Embed(title="Message editing", description=f"User: {after.author.mention} \nChanel {after.channel.mention} \nTime: {time}", color=disnake.Color.yellow())
            embed.add_field(name="Past content: ", value=f"> {before.content}", inline=False)
            embed.add_field(name="New content: ", value=f'> {after.content}', inline=False)
            embed.set_thumbnail(url=after.author.display_avatar)
            await channel_log.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(EditMessageLogging(bot))