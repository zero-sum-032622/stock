#! /opt/conda/bin/python
import os
import logging
import json
import logging.config
import pandas as pd
import joblib

from screener.models.analyzer import Analyzer
from screener.repository.history import History
from screener.repository.securities import Securities

with open(os.path.join(os.path.dirname(__file__), 'logging.json'), 'r', encoding='utf-8') as f:
    j = json.load(f)
    logging.config.dictConfig(j)

logger = logging.getLogger(__name__)

def analyze(h: History, s: tuple):
    logger.info(f'analyze {s[0]}: {s[1]}')
    a = Analyzer(h.get_history(s[0]))
    if a.df.isnull().values.sum() != 0:
        logger.warning(f'{s[0]} has NaN. skipped.')
        return
    a.add_sma(5) \
        .add_sma(20) \
        .add_sma(50) \
        .add_rsi(10, 'rsi') \
        .add_macd(5, 20, 5, 'macd') \
        .add_zigzag(0.01) \
        .pct_change(['sma05', 'sma20', 'sma50', 'Open', 'Close', 'High', 'Low']) \
        .diff('sma05', 'sma20', 'Close') \
        .diff('sma20', 'sma50', 'Close') \
        .normalize('Open', 'Close') \
        .normalize('High', 'Close') \
        .normalize('Low', 'Close')

    a.df['code'] = s[0]
    a.df['name'] = s[1]
    a.df['market'] = s[2]
    a.df.reset_index(inplace=True)
    return a.df[50:]

if __name__ == '__main__':
    securities = Securities()
    h = History()
    tables = joblib.Parallel(n_jobs=-1)(joblib.delayed(analyze)(h, s) for s in securities.items().itertuples())
    df = pd.concat(tables, axis=0, ignore_index=True)
    df.to_csv('all.csv')
