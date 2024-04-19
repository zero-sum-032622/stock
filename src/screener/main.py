#! /opt/conda/bin/python
import sys
import os
import logging
import json
import logging.config
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
        .diff('sma05', 'sma20') \
        .diff('sma20', 'sma50')
        # .add_bb(5, 'bb') \
    a.df['code'] = s[0]
    a.df['name'] = s[1]
    a.df['market'] = s[2]
    # a.df['seg33'] = s[3]
    # a.df['seg17'] = s[4]
    # a.df['scale'] = s[5]

    a.df[50:].to_csv(os.path.join(sys.argv[1], f'{s[0]}.csv'), float_format='%.6g')

if __name__ == '__main__':
    securities = Securities()
    h = History()
    joblib.Parallel(n_jobs=-1)(joblib.delayed(analyze)(h, s) for s in securities.items().itertuples())
    # for s in securities.items(None).itertuples():
    #     joblib.Parallel(n_jobs=-1)
    #     a = Analyzer(h.get_history(s[0]))
    #     a.add_sma(5) \
    #         .add_sma(20) \
    #         .add_sma(50) \
    #         .add_rsi(10, 'rsi') \
    #         .add_macd(5, 20, 5, 'macd') \
    #         .add_bb(5, 'bb') \
    #         .add_zigzag(0.01) \
    #         .pct_change(['sma05', 'sma20', 'sma50', 'Open', 'Close', 'High', 'Low']) \
    #         .diff('sma05', 'sma20') \
    #         .diff('sma20', 'sma50')
    #     a.df['code'] = s[0]
    #     a.df['name'] = s[1]
    #     a.df['market'] = s[2]
    #     a.df['seg33'] = s[3]
    #     a.df['seg17'] = s[4]
    #     a.df['scale'] = s[5]

    #     a.df[50:].to_csv(os.path.join(sys.argv[1], 'test.csv'))
    