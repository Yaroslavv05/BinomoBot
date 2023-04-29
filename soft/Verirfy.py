import sqlite3
from tradingview_ta import TA_Handler, Interval, Exchange

conn = sqlite3.connect('InfoToSignal.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM DataSignal')
rows = cursor.fetchall()


def get_exit_time():
    info = []
    for row in rows:
        info.append(row)
    exit_time = info[len(info) - 1][3]
    return exit_time


def get_now_price():
    info = []
    for row in rows:
        info.append(row)
    name_pair = info[len(info) - 1][0]
    handler = TA_Handler(
        symbol=name_pair,
        screener="forex",
        exchange=Exchange.FOREX,
        interval=Interval.INTERVAL_1_MINUTE
    )
    price_now = handler.get_analysis().indicators['close']
    return price_now


cursor.close()
conn.close()