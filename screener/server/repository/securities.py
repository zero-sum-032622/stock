import sys
import pandas as pd
import sqlite3 as sql
from globals import globals as gl

class securities:
    @staticmethod
    def table() -> str:
        return __class__.__name__
    



if __name__ == '__main__':
    symbols = pd.read_csv(sys.argv[1], header=0)
    symbols.set_index('コード', inplace=True)
    conn = sql.connect(gl.db_path())
    symbols.to_sql(securities.table(), conn, if_exists='replace')
    conn.close()