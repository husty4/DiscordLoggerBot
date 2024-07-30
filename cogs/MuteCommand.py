from disnake.ext import commands
from asyncio import sleep  # Импортируем sleep из asyncio
import disnake

class Mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: disnake.Member, duration: int, *, reason: str = None):
        if member == ctx.author:
            await ctx.send("You cannot mute yourself")
            return

        # Предполагается, что у вас уже есть роль для мута
        mute_role = disnake.utils.get(ctx.guild.roles, name="Muted")
        if not mute_role:
            await ctx.send("Role Muted was not found")
            return

        await member.add_roles(mute_role, reason=reason)
        await ctx.send(f"{member.mention} was muted for {duration} minute(s). Reason: {reason}")

        await sleep(duration * 60)  # Задержка в секундах

        await member.remove_roles(mute_role, reason="Mute duration expired")
        await ctx.send(f"{member.mention} no longer muted.")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: disnake.Member):
        mute_role = disnake.utils.get(ctx.guild.roles, name="Muted")
        if not mute_role:
            await ctx.send("Role Muted was not found")
            return

        if mute_role not in member.roles:
            await ctx.send(f"{member.mention} is not muted.")
            return

        await member.remove_roles(mute_role, reason="Unmuted by command")
        await ctx.send(f"{member.mention} no longer muted.")

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please, enter user name and duration.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You have no permission to use this command.")

def setup(bot):
    bot.add_cog(Mute(bot))
