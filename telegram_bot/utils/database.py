import sqlite3
from aiogram import types

conn = sqlite3.connect('users.db')
cur = conn.cursor()


class UsersDatabase:
    def __init__(self):
        cur.execute('CREATE TABLE IF NOT EXISTS users(users_id INTEGER PRIMARY KEY, tg_id INT)')
        conn.commit()

    def create_new_user(self, telegram_id: int):
        cur.execute('INSERT INTO users(tg_id) VALUES(?)', (telegram_id,))
        conn.commit()

    def get_user(self, telegram_id: int):
        data = cur.execute('SELECT * FROM users WHERE tg_id = ?', (telegram_id,))
        user = data.fetchone()
        return user

    def if_user_exists(self, telegram_id: int):
        user = self.get_user(telegram_id)
        return True if user else False