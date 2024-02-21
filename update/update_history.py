import sys
import datetime as dt
import pandas as pd
import yfinance as yf
import utils
yf.pdr_override()

ifname: str = sys.argv[1]
ofname: str = sys.argv[2]


stock_name = utils.get_codes()
base = pd.read_csv(ifname, header=[0, 1, 2], index_col=0, parse_dates=True)
if base.index[-1].date() < dt.date.today():
    df: pd.DataFrame = yf.download(stock_name, start=base.index[-1] + dt.timedelta(1), end=dt.date.today(), interval='1d')
    for idx in df.index:
        base.loc[idx] = df.loc[idx]
    base.to_csv(ofname)
else:
    print(f'{ifname} is up to date.')

