import sqlite3

conn = sqlite3.connect('users.db')
cur = conn.cursor()


class UsersDatabase:
    def __init__(self):
        cur.execute('CREATE TABLE IF NOT EXISTS users(users_id INTEGER NOT NULL, tg_id INT)')
        conn.commit()
