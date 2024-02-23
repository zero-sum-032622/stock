import pandas as pd

def get_codes(name = 'プライム（内国株式）') -> list :
    symbols = pd.read_csv('TSE.csv', header=0)
    criteria = symbols['市場・商品区分'] == name
    return [str(i) + '.T' for i in symbols[criteria]['コード'].to_list()]