import pandas as pd

class security:
    def __init__(self, code: int, name: str, market: str, industory33: int, industory17: int, size: int) -> None:
       self.__code: int = code
       self.__name: str = name
       self.__market: str = market
       self.__industory33: int = industory33
       self.__industory17: int = industory17
       self.__size: int = size

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
    def industory33(self) -> int:
        return self.__industory33
    @property
    def industory17(self) -> int:
        return self.__industory17
    @property
    def size(self) -> int:
        return self.__size


def get_codes(name = 'プライム（内国株式）') -> list :
    basename = path.dirname(__file__)
    symbols = pd.read_csv(path.join(basename, 'TSE.csv'), header=0)
    criteria = symbols['市場・商品区分'] == name
    return [str(i) + '.T' for i in symbols[criteria]['コード'].to_list()]