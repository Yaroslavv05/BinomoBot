import sqlite3
from datetime import datetime


class DataVerify:
    con = sqlite3.connect('InfoToSignal.db')
    cur = con.cursor()

    def __init__(self):
        self.cur.execute('CREATE TABLE IF NOT EXISTS delete_messages(message_id INT, time TEXT)')
        try:
            self.cur.execute(
                "CREATE TABLE DataVerify(date, name_pair, plus_or_minus)")
            self.con.commit()
        except sqlite3.OperationalError:
            pass

    def input_data(self, date, symbol, plus_or_minus):
        self.cur.execute(f'INSERT INTO DataVerify VALUES (?, ?, ?)', (date, symbol, plus_or_minus))
        self.con.commit()

    def input_data2(self, date, message_id):
        self.cur.execute(f'INSERT INTO delete_messages VALUES (?, ?)', (message_id, date))
        self.con.commit()

    def get_all_signals(self):
        now = datetime.now()
        formatted_date = now.strftime("%Y-%m-%d")
        return self.cur.execute(f'SELECT * FROM DataVerify WHERE date = "{formatted_date}"').fetchall()

    def get_all_messages(self):
        now = datetime.now()
        formatted_date = now.strftime("%Y-%m-%d")
        return self.cur.execute(f'SELECT * FROM delete_messages WHERE time = "{formatted_date}"').fetchall()
