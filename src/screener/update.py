import sys
from screener.repository.history import History
from screener.repository.securities import Securities
import datetime

if __name__ == "__main__":
    h = History()
    s = Securities()
    if len(sys.argv) == 3:
        begin: datetime.date = datetime.datetime.strptime(sys.argv[1], '%Y-%m-%d').date()
        end: datetime.date = datetime.datetime.strptime(sys.argv[2], '%Y-%m-%d').date()
    elif len(sys.argv) == 2:
        begin = datetime.date = datetime.datetime.strptime(sys.argv[1], '%Y-%m-%d').date()
        end = datetime.date.today()
    else:
        begin = h.latest()
        end = datetime.date.today()

    print(f'get data : {begin} - {end}')
    h.update(s.codes(None), begin, end)