import disnake
import json
import os
from disnake.ext import commands

class ProfanityFilter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.banned_words_file = "ban_words.json"
        self.load_banned_words()

    def load_banned_words(self):
        if os.path.exists(self.banned_words_file):
            try:
                with open(self.banned_words_file, "r", encoding="utf-8") as file:
                    self.banned_words = json.load(file)
            except json.JSONDecodeError:
                self.banned_words = []
        else:
            self.banned_words = []

    def save_banned_words(self):
        with open(self.banned_words_file, "w", encoding="utf-8") as file:
            json.dump(self.banned_words, file, ensure_ascii=False, indent=4)

    @commands.slash_command(description="Add a word to ban-word list")
    @commands.has_any_role("Administrator", "Moderator")
    async def addbanword(self, inter: disnake.ApplicationCommandInteraction, word: str):
        if word.lower() not in self.banned_words:
            self.banned_words.append(word.lower())
            self.save_banned_words()
            await inter.send(f"Word '{word}' added to ban-word list")
        else:
            await inter.send(f"Word '{word}' is already in the ban-word list")

    @commands.slash_command(description="Remove a word from ban-word list")
    @commands.has_any_role("Administrator", "Moderator")
    async def removebanword(self, inter: disnake.ApplicationCommandInteraction, word: str):
        if word.lower() in self.banned_words:
            self.banned_words.remove(word.lower())
            self.save_banned_words()
            await inter.send(f"Word '{word} removed from ban-word list'")
        else:
            await inter.send(f"Word '{word}' in not in the banned words list.")

    @commands.slash_command(description="List all banned words")
    @commands.has_any_role("Administrator", "Moderator")
    async def banwordlist(self, inter: disnake.ApplicationCommandInteraction):
        if self.banned_words:
            banned_words_formatter = ", ".join(self.banned_words)
            await inter.send(f"Banned words: {banned_words_formatter}", delete_after=60)
        else:
            await inter.send(f"Ban-words list is empty", delete_after=60)
    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.author.bot:
            return
        if any(word in message.content.lower() for word in self.banned_words):
            await message.delete()
            await message.channel.send(f"{message.author.mention} dont use ban-words")


    @commands.Cog.listener()
    async def on_message_edit(self, before: disnake.Message, after: disnake.Message):
        await self.on_message(after)


def setup(bot):
    bot.add_cog(ProfanityFilter(bot))







