import pytest
import shutil
import os
import tempfile
import settings
from screener.repository.history import History
from screener.repository.securities import Securities

SECURITIES_ONLY='libs/securities_only.sqlite'
EMPTY_HISTORY='libs/empty_history.sqlite'
WITH_HISTORY='libs/with_history.sqlite'


@pytest.fixture
def securities_only():
    with tempfile.NamedTemporaryFile('w', delete=False) as t:
        pass
    shutil.copyfile(SECURITIES_ONLY, t.name)
    settings.DB_PATH = t.name
    yield
    os.remove(t.name)

@pytest.fixture
def empty_history():
    with tempfile.NamedTemporaryFile('w', delete=False) as t:
        pass
    shutil.copyfile(EMPTY_HISTORY, t.name)
    settings.DB_PATH = t.name
    yield
    os.remove(t.name)

@pytest.fixture
def with_history():
    with tempfile.NamedTemporaryFile('w', delete=False) as t:
        pass
    shutil.copyfile(WITH_HISTORY, t.name)
    settings.DB_PATH = t.name
    yield
    os.remove(t.name)