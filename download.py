import pandas as pd
import yfinance as yf
import utils
yf.pdr_override()


stock_name = utils.get_codes()
df = yf.download(stock_name, start='2023-01-01', end='2024-01-13', interval='1d')
df.to_csv('00000000.csv')