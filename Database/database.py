import sqlite3

def connect_db():
    return sqlite3.connect("../moderator.db")

def create_guild_table(guild_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(f'CREATE TABLE IF NOT EXISTS guild_{guild_id} (word TEXT UNIQUE)')
    conn.commit()
    conn.close()

def add_ban_word(guild_id, word):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(f'INSERT INTO guild_{guild_id} (word) VALUES (?)', (word,))
    conn.commit()
    conn.close()

def remove_banword(guild_id, word):
    conn = connect_db()
    c = conn.cursor()
    c.execute(f'DELETE FROM guild_{guild_id} WHERE word = ?', (word,))
    conn.commit()
    conn.close()

# Получение всех банвордов для сервера
def get_banwords(guild_id):
    conn = connect_db()
    c = conn.cursor()
    c.execute(f'SELECT word FROM guild_{guild_id}')
    words = [row[0] for row in c.fetchall()]
    conn.close()
    return words
