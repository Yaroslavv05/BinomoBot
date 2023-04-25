from tradingview_ta import TA_Handler, Interval, Exchange
import time

symbols = ['EURUSD', 'GBPUSD', 'CHFJPY', 'EURJPY', 'EURCAD', 'USDJPY', 'NZDJPY', 'USDCAD', 'AUDUSD', 'AUDCAD', 'AUDNZD',
           'EURMXN', 'GBPJPY', 'AUDJPY', 'USDCHF', 'EURNZD', 'NZDUSD', 'GBPNZD']


def get_data(symbol):
    output = TA_Handler(
        symbol=symbol,
        screener="forex",
        exchange=Exchange.FOREX,
        interval=Interval.INTERVAL_1_HOUR
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
    print('search first data')
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
    print('------------------NEW ROUND--------------------')
    for i in s:
        try:
            data = get_data(i)
            if data['RECOMMENDATION'] == 'STRONG_BUY' and data['SYMBOL'] not in longs:
                print(data['SYMBOL'], 'Buy')
                longs.append(data['SYMBOL'])
            elif data['RECOMMENDATION'] == 'STRONG_SELL' and data['SYMBOL'] not in shorts:
                print(data['SYMBOL'], 'Sell')
                shorts.append(data['SYMBOL'])
            time.sleep(0.01)
        except:
            pass