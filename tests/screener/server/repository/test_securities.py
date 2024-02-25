import pytest
from screener.server.repository.securities import Securities

def test_constructor() -> None:
    sec = Securities()

def test_codes_default() -> None:
    sec = Securities()
    codes = list(sec.codes())
    assert codes[1] == '1332.T'

def test_codes_without_suffix() -> None:
    sec = Securities()
    codes = list(sec.codes(None, False))
    assert codes[1] == '1305'