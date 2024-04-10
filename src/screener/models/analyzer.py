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

    def add_zigzag(self, cp: float) -> Analyzer:
        self.__calculate_zigzag(cp)
        self.__calculate_profit()
        return self

    def __calculate_profit(self) -> None:
        expected = []
        period = []
        for row in self.df.itertuples():
            profit = self.df.at[row.switch, 'Close'] - row.Close
            expected.append(profit / row.Close)
            period.append(self.df.index.get_loc(row.switch) - self.df.index.get_loc(row.Index))
        self.df['expected'] = expected
        self.df['period'] = period


    def __calculate_zigzag(self, cp: float) -> None:
        prev_trend = 1
        prev_provisional = self.df.Close.iloc[0]

        trend = []
        provisional = []

        for c in self.df.Close:
            change = (c - prev_provisional) / prev_provisional
            cur_trend = 1 if change > cp \
                else -1 if change < -cp \
                else prev_trend
            cur_provisional = abs(max(cur_trend * c, cur_trend * prev_provisional))
            trend.append(cur_trend)
            provisional.append(cur_provisional)
            prev_trend = cur_trend
            prev_provisional = cur_provisional

        self.df['trend'] = trend
        self.df['provisional'] = provisional

        fixed = []
        switch = []
        zigzag = []
        cur_fixed = 0
        prev_fixed = provisional[-1]
        prev_switch = self.df.index[-1]
        for r in self.df.iloc[::-1].itertuples():
            cur_fixed = abs(max(r.trend * r.provisional, r.trend * prev_fixed))
            fixed.append(cur_fixed)
            prev_fixed = cur_fixed
            switch.append(prev_switch)
            if r.Close == cur_fixed:
                prev_switch = r.Index
                zigzag.append(cur_fixed)
            else:
                zigzag.append(None)

        switch.reverse()
        zigzag.reverse()
        self.df.drop(columns=['trend', 'provisional'])
        self.df['zigzag'] = zigzag
        self.df['zigzag'].interpolate(inplace=True)
        self.df['switch'] = switch