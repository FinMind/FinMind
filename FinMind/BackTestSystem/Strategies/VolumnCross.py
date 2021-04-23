import numpy as np
import pandas as pd
from FinMind.BackTestSystem.BaseClass import Strategy

class VolumnCross(Strategy):
    """
    summary:
        5日均量與10日均量黃金交叉且上漲 買入
        5日均量與10日均量死亡交叉且下跌 賣出
    """
    kdays1 = 5
    kdays2 = 10

    def add_indicator(self,
        kdays1: int,
        kdays2: int
    ):
        self.kdays1 = kdays1
        self.kdays2 = kdays2
    
    def create_trade_sign(self, stock_price: pd.DataFrame) -> pd.DataFrame:
        stock_price = stock_price.sort_values("date")
        stock_price["ma5"] = np.round(stock_price["Trading_Volume"].rolling(window = 5, center = False).mean(), 2)
        stock_price["ma10"] = np.round(stock_price["Trading_Volume"].rolling(window = 10, center = False).mean(), 2)
        stock_price['ma5-10'] = stock_price['ma5'] - stock_price['ma10']
        stock_price['diff'] = np.sign(stock_price['ma5-10'])
        stock_price.loc[(stock_price.index < self.kdays2), "diff"] = np.nan
        stock_price['signal'] = 0
        stock_price.loc[
            (
                np.sign(stock_price['diff'] - stock_price['diff'].shift(1)) > 0
                & (stock_price['spread'] > 0)
            ),
            "signal",
        ] = 1
        stock_price.loc[
            (
                np.sign(stock_price['diff'] - stock_price['diff'].shift(1)) < 0
                & (stock_price['spread'] < 0)
            ),
            "signal",
        ] = -1
        return stock_price
