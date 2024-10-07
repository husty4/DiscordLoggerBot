from disnake.ext import commands
from Database.database import add_ban_word, remove_banword, get_banwords


class BanWordsCommand(commands.Cog):  # Определение класса с наследованием от Cog
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Добавить банворд")  # Команда для добавления слова
    @commands.has_permissions(administrator=True)  # Проверка прав администратора
    async def addbanword(self, inter, word: str):  # Убедись, что все параметры правильно указаны
        guild_id = inter.guild.id
        try:
            add_ban_word(guild_id, word)  # Вызов функции для добавления слова в БД
            await inter.response.send_message(f'Слово "{word}" добавлено в бан-лист.')
        except Exception as e:
            await inter.response.send_message(f'Ошибка: {str(e)}')  # Обработка исключений

    @commands.slash_command(description="Удалить банворд")  # Команда для удаления слова
    @commands.has_permissions(administrator=True)
    async def removebanword(self, inter, word: str):
        guild_id = inter.guild.id
        remove_banword(guild_id, word)  # Вызов функции для удаления слова
        await inter.response.send_message(f'Слово "{word}" удалено из бан-листа.')

    @commands.slash_command(description="Показать список банвордов")  # Команда для показа списка
    @commands.has_permissions(administrator=True)
    async def banwordlist(self, inter):
        guild_id = inter.guild.id
        banned_words = get_banwords(guild_id)

        if banned_words:  # Условие проверяет, есть ли запрещённые слова
            await inter.response.send_message("Запрещённые слова: " + ", ".join(banned_words))
        else:
            await inter.response.send_message("В бан-листе пока нет слов.")

def setup(bot):
    bot.add_cog(BanWordsCommand(bot))