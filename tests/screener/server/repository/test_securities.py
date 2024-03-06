import pytest
from screener.server.repository.securities import Securities, Market

def test_constructor(securities_only) -> None:
    sec = Securities()

def test_codes_default(securities_only) -> None:
    sec = Securities()
    codes = list(sec.codes())
    assert codes[1] == '1332'

def test_codes_multi(securities_only) -> None:
    sec = Securities()
    codes = list(sec.codes(Market.PRIME | Market.STANDARD | Market.GROWTH))
    assert codes[1] == '1332'
    assert len(codes) == 3838

def test_codes_with_suffix(securities_only) -> None:
    sec = Securities()
    codes = list(sec.codes(None, True))
    assert codes[1] == '1305.T'