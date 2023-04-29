from tradingview_ta import TA_Handler, Interval, Exchange
import time
from datetime import datetime, timedelta
from db.InfoToSignalDB import DataInfoToSignal
from selenium import webdriver

symbols = ['EURUSD', 'GBPUSD', 'CHFJPY', 'EURJPY', 'EURCAD', 'USDJPY', 'NZDJPY', 'USDCAD', 'AUDUSD', 'AUDCAD', 'AUDNZD',
           'EURMXN', 'GBPJPY', 'AUDJPY', 'USDCHF', 'EURNZD', 'NZDUSD', 'GBPNZD']


def get_data(symbol):
    output = TA_Handler(
        symbol=symbol,
        screener="forex",
        exchange=Exchange.FOREX,
        interval=Interval.INTERVAL_15_MINUTES
    )
    activiti = output.get_analysis().summary
    activiti['SYMBOL'] = symbol
    return activiti


def get_symbols():
    return symbols


s = get_symbols()
longs = []
shorts = []

print('search first data')


def first_data():
    for i in s:
        try:
            data = get_data(i)
            if data['RECOMMENDATION'] == 'STRONG_BUY':
                longs.append(data['SYMBOL'])
            elif data['RECOMMENDATION'] == 'STRONG_SELL':
                shorts.append(data['SYMBOL'])
            time.sleep(0.01)
        except:
            pass

    print(f'longs: {longs}')
    print(f'shorts: {shorts}')


print('Start')
first_data()

while True:
    for i in s:
        try:
            data = get_data(i)
            if data['RECOMMENDATION'] == 'STRONG_BUY' and data['SYMBOL'] not in longs:
                now = datetime.now()
                time_now = now.strftime("%H:%M")
                name_pair = data['SYMBOL']
                position = 'LONG'
                ex = now + timedelta(minutes=5)
                exit_position = ex.strftime("%H:%M")
                handler = TA_Handler(
                    symbol=name_pair,
                    screener="forex",
                    exchange=Exchange.FOREX,
                    interval=Interval.INTERVAL_1_MINUTE
                )
                enter_price = handler.get_analysis().indicators['close']
                print(f'Цена при входе - {enter_price}', time_now, name_pair, f'Buy - выход со сделки в {exit_position}')
                longs.append(data['SYMBOL'])
                browser = webdriver.Chrome()
                browser.get(f'https://ru.tradingview.com/chart/?symbol=OANDA%3A{data["SYMBOL"]}')
                time.sleep(3)
                browser.save_screenshot('screenshot.png')
                browser.quit()
                Data = DataInfoToSignal(name_pair=name_pair, position=position, enter_time=time_now, exit_time=exit_position, enter_price=enter_price)
                Data.input_data()
                time.sleep(600)
            elif data['RECOMMENDATION'] == 'STRONG_SELL' and data['SYMBOL'] not in shorts:
                now = datetime.now()
                time_now = now.strftime("%H:%M")
                name_pair = data['SYMBOL']
                position = 'SHORT'
                ex = now + timedelta(minutes=5)
                exit_position = ex.strftime("%H:%M")
                handler = TA_Handler(
                    symbol=name_pair,
                    screener="forex",
                    exchange=Exchange.FOREX,
                    interval=Interval.INTERVAL_1_MINUTE
                )
                enter_price = handler.get_analysis().indicators['close']
                print(f'Цена при входе - {enter_price}', time_now, name_pair, f'Sell - выход со сделки в {exit_position}')
                shorts.append(data['SYMBOL'])
                browser = webdriver.Chrome()
                browser.get(f'https://ru.tradingview.com/chart/?symbol=OANDA%3A{data["SYMBOL"]}')
                time.sleep(3)
                browser.save_screenshot('screenshot.png')
                browser.quit()
                Data = DataInfoToSignal(name_pair=name_pair, position=position, enter_time=time_now, exit_time=exit_position, enter_price=enter_price)
                Data.input_data()
                time.sleep(600)
            time.sleep(0.01)
        except:
            pass