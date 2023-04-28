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

        try:
            self.cur.execute(
                "CREATE TABLE DataSignal(name_pair, position, enter_time, exit_time, enter_price)")
            self.con.commit()
        except sqlite3.OperationalError:
            pass

    def input_data(self):
        self.cur.execute(f'INSERT INTO DataSignal VALUES (?, ?, ?, ?, ?)', (self.symbol, self.position, self.enter_time, self.exit_time, self.enter_price))
        self.con.commit()
