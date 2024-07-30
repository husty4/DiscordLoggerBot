import disnake
from disnake.ext import commands

class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Kick user from server")
    @commands.has_permissions(kick_members=True)
    async def kick(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, reason: str = None):
        await member.kick(reason=reason)
        await inter.send(f'User {member.mention} has been kicked. Reason: {reason}')

def setup(bot):
    bot.add_cog(Kick(bot))