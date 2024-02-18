import os
import sys
import pandas as pd
import utils
import mplfinance as mpl
import datetime as dt

# ifname: str = sys.argv[1]
ifname: str = 'result/history.csv'

os.makedirs('result/csv', exist_ok=True)
os.makedirs('result/png', exist_ok=True)
df = pd.read_csv(ifname, header=[0, 1, 2], index_col=0, parse_dates=True)
header = None
today = None
codes = utils.get_codes()
key = df.index[-1]
for i in codes:
    history : pd.DataFrame = df.loc[:, (slice(None), [i], slice(None))]
    history.columns = [col[0] for col in history.columns.values]
    history.loc[:, 'SMA05'] = history.loc[:, 'Close'].rolling(5).mean()
    history.loc[:, 'SMA20'] = history.loc[:, 'Close'].rolling(20).mean()
    history.loc[:, 'SMA50'] = history.loc[:, 'Close'].rolling(50).mean()

    history.loc[:, 'DIV05'] = history.loc[:, 'SMA05'].diff()
    history.loc[:, 'DIV20'] = history.loc[:, 'SMA20'].diff()
    history.loc[:, 'DIV50'] = history.loc[:, 'SMA50'].diff()
    history.loc[:, 'DIV05%'] = history.loc[:, 'SMA05'].pct_change()
    history.loc[:, 'DIV20%'] = history.loc[:, 'SMA20'].pct_change()
    history.loc[:, 'DIV50%'] = history.loc[:, 'SMA50'].pct_change()
    
    history.loc[:, 'is-long'] = [ True if e > 0 else False for e in history.loc[:, 'DIV05'].values]
    history.to_csv(f'result/csv/{i}.csv')
    history.to_csv(f'result/csv/{i}.csv')

    # try:
    #     mpl.plot(history.tail(100), type='candle', mav=(5, 20, 50), volume=True, savefig=f'result/png/{i}.png')
    # except Exception as e:
    #     print(f'----- i -----')   
    #     print(e)

    if today is None:
        today = pd.DataFrame(columns=history.columns)
    today.loc[i] = history.loc[key]

today.to_csv(key.strftime('result/today.%Y-%m-%d.csv'))

    