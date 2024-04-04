from __future__ import annotations
import pandas as pd
import talib as ta

class Analyzer:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
    
    def add_sma(self, timeperiod: int, name: str = None) -> Analyzer:
        col = name if name is not None else f'sma{timeperiod:02}'
        self.df[col] = ta.SMA(self.df.Close, timeperiod = timeperiod)
        return self
    
    def add_macd(self, fast: int, slow: int, signal: int, name: str = None) -> Analyzer:
        col = name if name is not None else f'macd{slow:02}_{fast:02}_{signal:02}'
        self.df[col], self.df[col + 'sig'], self.df[col + 'his'] = ta.MACD(self.df.Close, fastperiod=fast, slowperiod=slow, signalperiod=signal)
        return self
    
    def add_rsi(self, period:int, name: str = None) -> Analyzer:
        col = name if name is not None else f'rsi{period:02}'
        self.df[col] = ta.RSI(self.df.Close, timeperiod=period)
        return self 
    
    def add_bb(self, period:int, prefix: str = None) -> Analyzer:
        col = prefix if prefix is not None else f'bb{period:02}_'
        self.df[col + 'u1'], self.df[col + 'mid'], self.df[col + 'd1'] = ta.BBANDS(self.df.Close, period, 1, 1, 0)
        self.df[col + 'u2'], self.df[col + 'mid'], self.df[col + 'd2'] = ta.BBANDS(self.df.Close, period, 2, 2, 0)
        self.df[col + 'u3'], self.df[col + 'mid'], self.df[col + 'd3'] = ta.BBANDS(self.df.Close, period, 3, 3, 0)
        return self
    
    