import pytest
from itertools import islice
import datetime as dt
import sqlite3 as sql
import settings
from screener.server.repository.history import History
from screener.server.repository.securities import Securities, Market

@pytest.fixture(scope='session')
def db():
    settings.DB_PATH = '/tmp/test.sqlite'


def test_update(securities_only):
    securities = Securities()
    h = History()
    h.update(securities.codes(Market.PRIME, False)[:3], dt.date(2024, 2, 19), dt.date(2024, 2, 25))
    conn = sql.connect(settings.DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute(f'SELECT COUNT(*) FROM {History.table()}')
        assert cur.fetchone()[0] == 12
    finally:
        conn.close()

def test_create_table(securities_only):
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

def test_get_history(with_history):
    h = History()
    df = h.get_history()
    assert len(df) == 12 
    df = h.get_history(1301)
    assert len(df) == 4

def test_latest(with_history):
    h = History()
    actual = h.latest()
    assert actual == dt.date(2024, 2, 22)

def test_latest_not_found(empty_history):
    h = History()
    actual = h.latest()
    assert actual is None