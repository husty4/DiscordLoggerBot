import disnake
from disnake.ext import commands

class BanCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Ban user on server")
    @commands.has_permissions(ban_members=True)
    async def ban(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, reason: str = None):
        await member.ban(reason=reason)
        await inter.send(f"User {member.mention} has been banned. Reason: {reason}")

def setup(bot):
    bot.add_cog(BanCommand(bot))