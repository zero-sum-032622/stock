import sys
import pandas as pd
import sqlite3 as sql
import logging
from collections.abc import Iterator
import settings
from screener.server.models.security import Security, Market

class Securities:
    __logger: logging.Logger = logging.getLogger(__name__)
    @staticmethod
    def table() -> str:
        return __class__.__name__

    def __init__(self) -> None:
        self.__logger.info(f'Open Database "{settings.DB_PATH}"')
        conn = sql.connect(settings.DB_PATH)
        self.__itmes = []
        cur = conn.cursor()
        cur.execute(f'SELECT "コード", "銘柄名", "市場・商品区分", "33業種区分", "17業種区分", "規模区分" FROM {Securities.table()}')
        self.__itmes = [Security(c[0], c[1], c[2], c[3], c[4], c[5]) for c in cur.fetchall()]
        conn.close()
        self.__logger.debug(f'get {len(self.__itmes)} items.')

    def items(self, market: Market = Market.PRIME) -> Iterator[Security]:
        if market is None:
            return self.__itmes
        else:
            return filter(lambda s: s.market == market.value, self.__itmes)

    def codes(self, market: Market = Market.PRIME, add_t: bool = True) -> Iterator[str]:
        suffix = '.T' if add_t else ''
        if market is None:
            return map(lambda s: str(s.code) + suffix, self.__itmes)
        else:
            return map(lambda s: str(s.code) + suffix, filter(lambda s: s.market == market.value, self.__itmes))


if __name__ == '__main__':
    symbols = pd.read_csv(sys.argv[1], header=0)
    symbols.set_index('コード', inplace=True)
    conn = sql.connect(settings.DB_PATH)
    symbols.to_sql(Securities.table(), conn, if_exists='replace')
    conn.close()