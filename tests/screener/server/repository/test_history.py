import pytest
from itertools import islice
import datetime as dt
import sqlite3 as sql
import settings
from screener.server.repository.history import History
from screener.server.repository.securities import Securities, Market

def test_update():
    securities = Securities()
    h = History()
    h.update(islice(securities.items(Market.PRIME), 3), dt.date(2024, 2, 19), dt.date(2024, 2, 25))

def test_create_table():
    h = History()
    h.create_table()
    conn = sql.connect(settings.DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT COUNT(*) FROM sqlite_master WHERE TYPE='table' AND name='{History.table()}'")
        assert cur.fetchone()[0] == 1
        cur.close()
    finally:
        conn.close()
