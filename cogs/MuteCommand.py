from disnake.ext import commands
from asyncio import sleep
import disnake

class Mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Mute user")
    @commands.has_permissions(manage_roles=True)
    async def mute(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, duration: int, reason: str = None):
        if member == inter.author:
            await inter.send("You cannot mute yourself.")
            return

        mute_role = disnake.utils.get(inter.guild.roles, name="Muted")
        if not mute_role:
            await inter.send("Role Muted was not found.")
            return

        await member.add_roles(mute_role, reason=reason)
        await inter.send(f"{member.mention} was muted for {duration} minute(s). Reason: {reason}")

        await sleep(duration * 60)

        await member.remove_roles(mute_role, reason="Mute duration expired")
        await inter.send(f"{member.mention} is no longer muted.")

    @commands.slash_command(description="Unmute user")
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member):
        mute_role = disnake.utils.get(inter.guild.roles, name="Muted")
        if not mute_role:
            await inter.send("Role Muted was not found.")
            return

        if mute_role not in member.roles:
            await inter.send(f"{member.mention} is not muted.")
            return

        await member.remove_roles(mute_role, reason="Unmuted by command")
        await inter.send(f"{member.mention} is no longer muted.")

    @mute.error
    async def mute_error(self, inter, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await inter.send("Please, specify a user and duration.")
        elif isinstance(error, commands.MissingPermissions):
            await inter.send("You don't have permission to use this command.")

def setup(bot):
    bot.add_cog(Mute(bot))
