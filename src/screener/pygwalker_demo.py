import pygwalker as pyg
import pandas as pd
import streamlit.components.v1 as components
import streamlit as st

from screener.models.analyzer import Analyzer
from screener.repository.history import History
 
# Streamlitページの幅を調整する
st.set_page_config(
    page_title="StreamlitでPygwalkerを使う",
    layout="wide"
)
 
# タイトルを追加
st.title("StreamlitでPygwalkerを使う")
 
# データをインポートする
h = History()
a = Analyzer(h.get_history(9434))

a.add_sma(5) \
    .add_sma(20) \
    .add_sma(50) \
    .add_rsi(10, 'rsi') \
    .add_macd(5, 20, 5, 'macd') \
    .add_bb(5, 'bb') \
    .add_zigzag(0.02)
 
# Pygwalkerを使用してHTMLを生成する
pyg_html = pyg.to_html(a.df)
 
# HTMLをStreamlitアプリケーションに埋め込む
components.html(pyg_html, height=1000, scrolling=True)