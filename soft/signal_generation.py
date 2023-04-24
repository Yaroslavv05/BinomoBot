from tradingview_ta import TA_Handler, Interval, Exchange
coins = ['EURUSD', 'GBPUSD', 'CHFJPY', 'EURJPY', 'EURCAD', 'USDJPY', 'NZDJPY', 'USDCAD', 'AUDUSD', 'AUDCAD', 'AUDNZD', 'EURMXN', 'GBPJPY', 'AUDJPY', 'USDCHF', 'EURNZD', 'NZDUSD', 'GBPNZD']
eurusd = TA_Handler(
    symbol="EURUSD",
    screener="forex",
    exchange=Exchange.FOREX,
    interval=Interval.INTERVAL_5_MINUTES
)
print(eurusd.get_analysis().summary)



