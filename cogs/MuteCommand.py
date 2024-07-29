from disnake.ext import commands
from asyncio import sleep  # Импортируем sleep из asyncio
import disnake

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: disnake.Member, duration: int, *, reason: str = None):
        if member == ctx.author:
            await ctx.send("Вы не можете замютить себя.")
            return

        # Предполагается, что у вас уже есть роль для мута
        mute_role = disnake.utils.get(ctx.guild.roles, name="Muted")
        if not mute_role:
            await ctx.send("Роль 'Muted' не найдена. Создайте её и добавьте к боту.")
            return

        await member.add_roles(mute_role, reason=reason)
        await ctx.send(f"{member.mention} был замьючен на {duration} минут(ы) по причине: {reason}")

        await sleep(duration * 60)  # Задержка в секундах

        await member.remove_roles(mute_role, reason="Mute duration expired")
        await ctx.send(f"{member.mention} больше не замьючен.")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: disnake.Member):
        # Предполагается, что у вас уже есть роль для мута
        mute_role = disnake.utils.get(ctx.guild.roles, name="Muted")
        if not mute_role:
            await ctx.send("Роль 'Muted' не найдена. Создайте её и добавьте к боту.")
            return

        if mute_role not in member.roles:
            await ctx.send(f"{member.mention} не замьючен.")
            return

        await member.remove_roles(mute_role, reason="Unmuted by command")
        await ctx.send(f"{member.mention} больше не замьючен.")

def setup(bot):
    bot.add_cog(Moderation(bot))
