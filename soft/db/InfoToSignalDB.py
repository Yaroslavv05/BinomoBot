import sqlite3


class DataInfoToSignal:
    con = sqlite3.connect('InfoToSignal.db')
    cur = con.cursor()

    def __init__(self, name_pair, position, enter_time, exit_time, enter_price):
        self.symbol = name_pair
        self.position = position
        self.enter_time = enter_time
        self.exit_time = exit_time
        self.enter_price = enter_price

        self.cur.execute("CREATE TABLE IF NOT EXISTS DataSignal(name_pair, position, enter_time, exit_time, "
                         "enter_price)")
        self.con.commit()

    def input_data(self):
        self.cur.execute(f'INSERT INTO DataSignal VALUES (?, ?, ?, ?, ?)', (self.symbol, self.position, self.enter_time, self.exit_time, self.enter_price))
        self.con.commit()
