import sys
import pandas as pd
import sqlite3 as sql
import logging
import traceback
from collections.abc import Iterator
import settings
from screener.models.security import Security, Market, MarketNames

class Securities:
    __logger: logging.Logger = logging.getLogger(__name__)
    @staticmethod
    def table() -> str:
        return __class__.__name__

    def __init__(self) -> None:
        self.__logger.info(f'Open Database "{settings.DB_PATH}"')
        conn = sql.connect(settings.DB_PATH)
        try:
            self.__items = pd.read_sql(f'SELECT "code", "name", "market", "segment33", "segment17", "scale" FROM {Securities.table()}', conn)
            self.__items.set_index('code', inplace=True)
            self.__logger.debug(f'get {len(self.__items)} items.')
        except Exception as ex:
            self.__logger.error(traceback.format_exc())
            raise
        finally:
            conn.close()

    def items(self, market: Market = Market.PRIME) -> pd.DataFrame:
        if market is None:
            return self.__items
        else:
            query: str = ' or '.join(map(lambda m: f"market == '{MarketNames[m]}'", [tgt for tgt in Market if market & tgt]))
            # return self.__items.query(f"market == '{market.value}'")
            return self.__items.query(query)

    def codes(self, market: Market = Market.PRIME, add_t: bool = False) -> list[str]:
        suffix = '.T' if add_t else ''
        # return map(lambda s: str(s) + suffix, self.items(market).code)
        return [str(c) + suffix for c in self.items(market).index]
    
    @classmethod
    def create_table(cls, csv: str = None) -> None:
        target: str = settings.TSE_PATH if csv is not None else csv
        symbols = pd.read_csv(target, header=0)
        symbols.columns = ['date', 'code', 'name', 'market', 'segment33', 'segment33_name', 'segment17', 'segment17_name', 'scale', 'scale_name']
        symbols.set_index('code', inplace=True)
        conn = sql.connect(settings.DB_PATH)
        try:
            symbols.to_sql(Securities.table(), conn, if_exists='replace', index=True)
        except Exception as e:
            cls.__logger.error(traceback.format_exc())
            raise
        finally:
            conn.close()

if __name__ == '__main__':
    Securities.create_table(sys.argv[1] if len(sys.argv) == 2 else None) 