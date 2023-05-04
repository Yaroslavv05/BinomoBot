import sqlite3


class DataInfoToSignal:
    con = sqlite3.connect('InfoToSignal.db', check_same_thread=False)
    cur = con.cursor()

    def __init__(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS DataSignal(name_pair, position, enter_time, exit_time, "
                         "enter_price)")
        self.con.commit()

    def input_data(self, name_pair, position, enter_time, exit_time, enter_price):
        self.cur.execute(f'INSERT INTO DataSignal VALUES (?, ?, ?, ?, ?)', (name_pair, position, enter_time, exit_time, enter_price))
        self.con.commit()

    def get_last_forcast(self):
        return self.cur.execute('SELECT * FROM DataSignal').fetchall()[-1]
