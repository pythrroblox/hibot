import sqlite3
from discord.ext import commands
channel_ids = [1079796101005185120, 1281146099654066230]

class levellingsystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect('levelsystem.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT,
            level INTEGER DEFAULT 1,
            xp INTEGER DEFAULT 0
        )
        ''')
        self.conn.commit()
        print("Table created or already exists.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.channel.id not in channel_ids:
            return

        user_id = str(message.author.id)
        username = message.author.name

        self.cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = self.cursor.fetchone()

        if row is None:
            self.cursor.execute('INSERT INTO users (id, username, xp) VALUES (?, ?, ?)', (user_id, username, 10))
        else:
            new_xp = row[3] + 10
            self.cursor.execute('UPDATE users SET xp = ? WHERE id = ?', (new_xp, user_id))

        self.conn.commit()
        print("Database commit successful.")

        new_level = self.update_level(user_id)
        if new_level:
            await message.channel.send(f'Congratulations {username}, you have leveled up to level {new_level}!')

    def update_level(self, user_id):
        self.cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = self.cursor.fetchone()

        if row:
            xp = row[3]
            level = int(0.1 * (xp ** 0.5))

            if level > row[2]:
                self.cursor.execute('UPDATE users SET level = ? WHERE id = ?', (level, user_id))
                self.conn.commit()
                return level
        return None

def setup(bot):
    bot.add_cog(levellingsystem(bot))
