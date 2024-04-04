import os
import json
import datetime as dt
import streamlit as st
import logging
import logging.config
import streamlit_lightweight_charts as charts

from screener.repository.securities import Securities, Market, MarketNames
from screener.repository.history import History
import screener.charts.ohlc as ohlc

with open(os.path.join(os.path.dirname(__file__), 'logging.json'), 'r', encoding='utf-8') as f:
    j = json.load(f)
    logging.config.dictConfig(j)

logger: logging.Logger = logging.getLogger(__name__)



def setup_logger() -> logging.Logger:
    with open(os.path.join(os.path.dirname(__file__), 'logging.json'), 'r', encoding='utf-8') as f:
        j = json.load(f)
        logging.config.dictConfig(j)
    return logging.getLogger(__name__)

def securites(s: Securities):
    selected = st.multiselect("市場・商品区分", [MarketNames[m] for m in Market], MarketNames[Market.PRIME])
    flags = 0
    for sel in selected:
        flags |= Market.label2flag(sel)
    
    if flags != 0:
        st.write(s.items(flags))

def update(s: Securities, h: History):
    if st.button('DB更新'):
        h.update(s.codes(None), h.latest(), dt.date.today())


def main() -> None:
    logger.debug("start.")

    st.set_page_config(layout="wide")

    securities = Securities()
    history = History()

    with st.sidebar:
        update(securities, history)
        securites(securities)

    tab_chart, tab_table = st.tabs(["Chart", "Table"]) 
    d = history.get_history(5831)
    d.dropna()
    with tab_chart:
        subheder, data = ohlc.ohlc_chart(d)
        st.subheader(subheder)
        charts.renderLightweightCharts(data, "multipane")
    with tab_table:
        st.write(d)
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