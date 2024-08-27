import disnake
from disnake.ext import commands


class Applications(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.min_age = 15

    @commands.slash_command(name="заявка")
    async def application(self, inter: disnake.ApplicationCommandInteraction,
                          name: str = commands.Param(name="имя", description="Полное имя"),
                          age: int = commands.Param(name="возраст", description="Количество полных лет"),
                          online: str = commands.Param(name="онлайн", description="Средний онлайн")):
        allowed_channel_id = 1277941325819416636
        if inter.channel.id != allowed_channel_id:
            await inter.response.send_message("Эту команду здесь нельзя использовать", ephemeral=True)
            return

        try:
            if int(age) < self.min_age:
                return await inter.response.send_message(f"Набор на должность строго с {self.min_age} лет",
                                                         ephemeral=True)
        except ValueError:
            return await inter.response.send_message("Введите возраст правильно!", ephemeral=True)

        await inter.response.send_message("Заявка отправлена", ephemeral=True)
        statement_channel = self.bot.get_channel(1277935602309922973)
        embed = disnake.Embed(title="Заявка", description=f"Автор: {inter.author.mention}",
                              color=disnake.Colour.yellow())
        embed.add_field(name="Имя", value=f"> {name}", inline=False)
        embed.add_field(name="Возраст", value=f"> {age}", inline=False)
        embed.add_field(name="Онлайн", value=f"> {online} ч./день", inline=False)
        await statement_channel.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Applications(bot))
