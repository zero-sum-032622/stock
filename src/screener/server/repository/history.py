import datetime as dt
import pandas as pd
import yfinance as yf
import logging
import sqlite3 as sql
import traceback
from collections.abc import Iterable
from screener.server.models.security import Security
import settings
yf.pdr_override()

class History:
    __logger = logging.getLogger(__name__)
    @staticmethod
    def table() -> str:
        return __class__.__name__

    def __init__(self) -> None:
        pass

    def update(self, securities: Iterable[Security], begin: dt.date, end: dt.date) -> bool:
        self.create_table()
        sec = list(securities)
        tickers = list(map(lambda s: str(s.code) + '.T', sec))
        self.__logger.info(f'down load data: tickers: {len(tickers)}, begin: {begin}, end: {end}')
        df: pd.DataFrame = yf.download(tickers, start=begin, end=end)
        con = sql.connect(settings.DB_PATH)
        stmt: str = f'REPLACE INTO {self.table()} (date, code, adj_close, close, high, low, open, volume) values(?, ?, ?, ?, ?, ?, ?, ?)'
        try:
            cur = con.cursor()
            for s in sec:
                history : pd.DataFrame = df.loc[:, (slice(None), [str(s.code) + '.T'], slice(None))]
                history.columns = [col[0] for col in history.columns.values]

                for row in history.itertuples():
                    data = (row.Index.strftime('%Y-%m-%d'), s.code, row[1], row.Close, row.High, row.Low, row.Open, row.Volume)
                    cur.execute(stmt, data)
            con.commit()
        except Exception as e:
            con.rollback()
            self.__logger.error(traceback.format_exc())
        finally:
            con.close()

    
    def create_table(self) -> None:
        query: str = f'''CREATE TABLE IF NOT EXISTS {self.table()} (
            date TEXT NOT NULL,
            code INTEGER NOT NULL,
            adj_close NUMBER,
            close NUMBER,
            high NUMBER,
            low NUMBER,
            open NUMBER,
            volume NUMBER,
            PRIMARY KEY(date, code)
        );'''
        self.__logger.debug(query)
        conn = sql.connect(settings.DB_PATH)
        try:
            cur = conn.cursor()
            cur.execute(query)
            cur.close()
            conn.commit()
            self.__logger.info(f'create table {self.table()}')
        except Exception as e:
            conn.rollback()
            self.__logger.error(traceback.format_exc())
        finally:
            conn.close()

        


    def select(self, code: int) -> pd.DataFrame:
        pass

# ifname: str = sys.argv[1]
# ofname: str = sys.argv[2]


# stock_name = utils.get_codes()
# base = pd.read_csv(ifname, header=[0, 1, 2], index_col=0, parse_dates=True)
# if base.index[-1].date() < dt.date.today():
#     df: pd.DataFrame = yf.download(stock_name, start=base.index[-1] + dt.timedelta(1), end=dt.date.today(), interval='1d')
#     for idx in df.index:
#         base.loc[idx] = df.loc[idx]
#     base.to_csv(ofname)
# else:
    # print(f'{ifname} is up to date.')