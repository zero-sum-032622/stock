import sys
from screener.server.repository.history import History
from screener.server.repository.securities import Securities

if __name__ == "__main__":
    pass
    h = History()
    s = Securities()
    h.update(s.codes(None), sys.argv[1], sys.argv[1])