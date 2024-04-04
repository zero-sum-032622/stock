import sys
from screener.repository.history import History
from screener.repository.securities import Securities

if __name__ == "__main__":
    h = History()
    s = Securities()
    h.update(s.codes(None), sys.argv[1], sys.argv[2])