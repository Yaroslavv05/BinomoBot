import sqlite3


class DataVerify:
    con = sqlite3.connect('InfoToSignal.db')
    cur = con.cursor()

    def __init__(self, date, name_pair, plus_or_minus):
        self.date = date
        self.symbol = name_pair
        self.plus_or_minus = plus_or_minus
        try:
            self.cur.execute(
                "CREATE TABLE DataVerify(date, name_pair, plus_or_minus)")
            self.con.commit()
        except sqlite3.OperationalError:
            pass

    def input_data(self):
        self.cur.execute(f'INSERT INTO DataVerify VALUES (?, ?, ?)', (self.date, self.symbol, self.plus_or_minus))
        self.con.commit()
