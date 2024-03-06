import datetime as dt
import pandas as pd
import yfinance as yf
import logging
import sqlite3 as sql
import traceback
from screener.server.repository.securities import Securities
import settings
yf.pdr_override()

class History:
    __logger = logging.getLogger(__name__)
    @staticmethod
    def table() -> str:
        return __class__.__name__

    def __init__(self) -> None:
        pass

    def update(self, securities: list[str], begin: dt.date, end: dt.date) -> bool:
        self.create_table()
        tickers = list(map(lambda s: str(s) + '.T', securities))
        self.__logger.info(f'down load data: tickers: {len(tickers)}, begin: {begin}, end: {end}')
        begin_ = begin if begin is not None else dt.date(2023, 1, 1)
        end_ = end if end is not None else dt.date.today()
        df: pd.DataFrame = yf.download(tickers, start=begin_, end=end_)
        con = sql.connect(settings.DB_PATH)
        stmt: str = f'REPLACE INTO {self.table()} (date, code, adj_close, close, high, low, open, volume) values(?, ?, ?, ?, ?, ?, ?, ?)'
        try:
            cur = con.cursor()
            for s in securities:
                history : pd.DataFrame = df.loc[:, (slice(None), [s + '.T'], slice(None))]
                history.columns = [col[0] for col in history.columns.values]

                for row in history.itertuples():
                    data = (row.Index.strftime('%Y-%m-%d'), int(s), row[1], row.Close, row.High, row.Low, row.Open, row.Volume)
                    cur.execute(stmt, data)
            con.commit()
        except Exception as e:
            con.rollback()
            self.__logger.error(traceback.format_exc())
            raise
        finally:
            con.close()

    def get_history(self, code: str = None) -> pd.DataFrame:
        query = f'SELECT date, code, close high, low, open, volume FROM {self.table()}' + (f" WHERE code = '{code}'" if code is not None else '')
        self.__logger.debug(f'query = {query}')
        con = sql.connect(settings.DB_PATH)
        try:
            df = pd.read_sql_query(query, con)
        except Exception as e:
            self.__logger.error(traceback.format_exc())
            raise
        finally:
            con.close()
        return df

    def latest(self) -> dt.date:
        con = sql.connect(settings.DB_PATH)
        try:
            cur = con.cursor() 
            cur.execute(f'SELECT MAX(date) FROM {History.table()}')
            found = cur.fetchone()[0]
            retval = None if found is None else dt.datetime.strptime(found, '%Y-%m-%d').date()
            cur.close()
            return retval
        except Exception as e:
            self.__logger.error(traceback.format_exc())
            raise
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
            raise
        finally:
            conn.close()

    def select(self, code: int) -> pd.DataFrame:
        pass

if __name__ == '__main__':
    s = Securities()
    h = History()
    h.update(s.codes(None), h.latest(), dt.date.today())
