import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def clear(self, ctx, amount: int):
        messages = await ctx.channel.purge(limit=amount + 1)
        await ctx.reply(f'{len(messages)} было ощищено')



def setup(bot):
    bot.add_cog(Moderation(bot = bot))