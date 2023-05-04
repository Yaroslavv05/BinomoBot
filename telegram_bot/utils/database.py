import sqlite3

conn = sqlite3.connect('users.db')
cur = conn.cursor()


class UsersDatabase:
    def __init__(self):
        cur.execute('CREATE TABLE IF NOT EXISTS users(users_id INTEGER PRIMARY KEY, tg_id INT)')
        cur.execute('CREATE TABLE IF NOT EXISTS work_time(num INT, is_work BOOLEAN)')
        conn.commit()

    @staticmethod
    def create_new_user(telegram_id: int):
        cur.execute('INSERT INTO users(tg_id) VALUES(?)', (telegram_id,))
        conn.commit()

    @staticmethod
    def get_user(telegram_id: int) -> tuple:
        data = cur.execute('SELECT * FROM users WHERE tg_id = ?', (telegram_id,))
        user = data.fetchone()
        return user

    def if_user_exists(self, telegram_id: int) -> bool:
        user = self.get_user(telegram_id)
        return True if user else False

    @staticmethod
    def get_all_users() -> list[tuple[int]]:
        data = cur.execute('SELECT tg_id FROM users')
        users_id = data.fetchall()
        return users_id

    @staticmethod
    def is_work_time(is_work=False):
        data = cur.execute('SELECT * FROM work_time').fetchone()
        if not data:
            cur.execute('INSERT INTO work_time(num, is_work) VALUES(?,?)', (1, is_work,))
        conn.commit()

    def change_work_time(self, work_time):
        self.is_work_time(work_time)
        cur.execute(f'UPDATE work_time SET is_work = {work_time} WHERE num = 1')
        conn.commit()
