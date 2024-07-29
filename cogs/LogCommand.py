import discord
from discord.ext import commands
import os
import datetime

class LogCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='logs')
    @commands.has_any_role('Администратор', 'Логер')
    async def logs(self, ctx):
        log_file_path = 'logs/message_log.txt'
        if os.path.exists(log_file_path):
            await ctx.send(file=discord.File(log_file_path))
        else:
            await ctx.send("Log file not found.")

    @commands.command(name='datelog')
    @commands.has_any_role('Администратор', 'Логер')
    async def datelog(self, ctx, date: str):
        try:
            date_obj = datetime.datetime.strptime(date, '%d-%m-%Y')
            log_file_path = f'logs/message_log_{date_obj.strftime("%d-%m-%Y")}.txt'
            if os.path.exists(log_file_path):
                await ctx.send(file=discord.File(log_file_path))
            else:
                await ctx.send("Log file for the specified date not found.")
        except ValueError:
            await ctx.send("Incorrect date format. Please use DD-MM-YYYY.")

async def setup(bot):
    bot.add_cog(LogCommand(bot))
