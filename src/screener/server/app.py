import os
import json
import datetime as dt
import streamlit as st
import logging
import logging.config

from screener.server.repository.securities import Securities, Market, MarketNames
from screener.server.repository.history import History
from screener.server.models.security import Security

def setup_logger() -> logging.Logger:
    with open(os.path.join(os.path.dirname(__file__), 'logging.json'), 'r', encoding='utf-8') as f:
        j = json.load(f)
        logging.config.dictConfig(j)
    return logging.getLogger(__name__)

def securites():
    checked: Market = None
    target = [Market.PRIME, Market.STANDARD, Market.GROWTH]
    all = Market.PRIME | Market.STANDARD | Market.GROWTH

    for m in target:
        if st.checkbox(MarketNames[m]):
            checked = m if checked is None else checked | m

    rep_security = Securities()
    if checked is not None:
        st.write(rep_security.items(checked))

def update():
    if st.button('DB更新'):
        s = Securities()
        h = History()
        h.update(s.codes(None), h.latest(), dt.date.today())


def main() -> None:
    logger: logging.Logger = setup_logger()
    update()
    securites()
# if st.button()

#スライダー（デフォルトでは0~100）
# st.title("スライダー")
# weight = st.slider("今日の体重は")
# st.write("今の体重は" + str(weight) +"kgです")

#ボタン
# st.title("今日の天気は")
# st.button("リセット", type="primary")
# if st.button("晴れ？"):
#     st.write("今日も元気に！")
# else:
#     st.write("傘を忘れずに")

# #テキスト入力
# st.title("やること")
# st.text_input("今やること", key="do")
# st.session_state.do #keyでアクセス

# #チェックボックス
# st.title("ごみ捨てチェック")
# is_agree = st.checkbox("ごみ捨てた？")
# if is_agree:
#     st.write("お疲れ様！")
# else:
#     st.write("忘れずに！")


if __name__ == "__main__":
    main()