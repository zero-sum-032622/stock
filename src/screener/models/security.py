import pandas as pd
from enum import Enum, IntFlag, auto

# class Market(Flag):
#     PRIME = 'プライム（内国株式）'
#     STANDARD = 'スタンダード（内国株式）'
#     GROWTH = 'グロース（内国株式）'

#     PRIME_F = 'プライム（外国株式）'
#     STANDARD_F = 'スタンダード（外国株式）'
#     GROWTH_F = 'グロース（外国株式）'

#     ETF = 'ETF・ETN'
#     REIT = 'REIT・ベンチャーファンド・カントリーファンド・インフラファンド'
#     INVESTMENT = '出資証券'

class Market(IntFlag):
    PRIME = auto()
    STANDARD = auto()
    GROWTH = auto()

    PRIME_F = auto()
    STANDARD_F = auto()
    GROWTH_F = auto()

    ETF = auto()
    REIT = auto()
    INVESTMENT = auto()
    @staticmethod
    def label2flag(label: str):
        for m in Market:
            if MarketNames[m] == label:
                return m
            
        return 0


MarketNames = {
    Market.PRIME: 'プライム（内国株式）',
    Market.STANDARD: 'スタンダード（内国株式）',
    Market.GROWTH: 'グロース（内国株式）',
    Market.PRIME_F: 'プライム（外国株式）',
    Market.STANDARD_F: 'スタンダード（外国株式）',
    Market.GROWTH_F: 'グロース（外国株式）',
    Market.ETF: 'ETF・ETN',
    Market.REIT: 'REIT・ベンチャーファンド・カントリーファンド・インフラファンド',
    Market.INVESTMENT: '出資証券'
}




class Security:
    def __init__(self, code: int, name: str, market: str, industory33: str, industory17: str, size: str) -> None:
       self.__code: int = code
       self.__name: str = name
       self.__market: str = market
       self.__industory33: str = industory33
       self.__industory17: str = industory17
       self.__size: str = size

    @property
    def code(self) -> int:
        return self.__code
    @property
    def name(self) -> str:
        return self.__name
    @property
    def market(self) -> str:
        return self.__market
    @property
    def industory33(self) -> str:
        return self.__industory33
    @property
    def industory17(self) -> str:
        return self.__industory17
    @property
    def size(self) -> str:
        return self.__size


# def get_codes(name = 'プライム（内国株式）') -> list :
#     basename = path.dirname(__file__)
#     symbols = pd.read_csv(path.join(basename, 'TSE.csv'), header=0)
#     criteria = symbols['市場・商品区分'] == name
#     return [str(i) + '.T' for i in symbols[criteria]['コード'].to_list()]