import sys
sys.path.append('..')
import pandas as pd
import yfinance as yf
import libs.utils as util
yf.pdr_override()


stock_name = util.get_codes()
df = yf.download(stock_name[:5], start='2023-01-01', end='2023-01-14', interval='1d')

for i in stock_name[:5] :
    history : pd.DataFrame = df.loc[:, (slice(None), [i], slice(None))]
    history.columns = [col[0] for col in history.columns.values]

