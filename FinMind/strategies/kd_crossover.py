import numpy as np
import pandas as pd
from ta.momentum import StochasticOscillator

from FinMind.strategies.base import Strategy


class KdCrossOver(Strategy):
    """
    url: "http://smart.businessweekly.com.tw/Reading/WebArticle.aspx?id=68129&p=2"
    summary: 日KD黃金交叉和死亡交叉
            日K線 小於 日D線，翻轉成，日K線 大於 日D線 稱為黃金交叉
            日K線 大於 日D線，翻轉成，日K線 小於 日D線 稱為死亡交叉
            黃金交叉進場，死亡交叉出場
    """

    k_days = 9

    def create_trade_sign(self, stock_price: pd.DataFrame) -> pd.DataFrame:
        stock_price = stock_price.sort_values("date")
        kd = StochasticOscillator(
            high=stock_price["max"],
            low=stock_price["min"],
            close=stock_price["close"],
            n=self.k_days,
        )
        rsv_ = kd.stoch().fillna(50)
        _k = np.zeros(stock_price.shape[0])
        _d = np.zeros(stock_price.shape[0])
        for i, r in enumerate(rsv_):
            if i == 0:
                _k[i] = 50
                _d[i] = 50
            else:
                _k[i] = _k[i - 1] * 2 / 3 + r / 3
                _d[i] = _d[i - 1] * 2 / 3 + _k[i] / 3
        stock_price["K"] = _k
        stock_price["D"] = _d
        stock_price.index = range(len(stock_price))
        stock_price["diff"] = stock_price["K"] - stock_price["D"]
        stock_price.loc[(stock_price.index < self.k_days), "diff"] = np.nan
        stock_price["diff_sign"] = stock_price["diff"].map(
            lambda x: 1 if x >= 0 else (-1 if x < 0 else 0)
        )
        stock_price["diff_sign_yesterday"] = (
            stock_price["diff_sign"].shift(1).fillna(0).astype(int)
        )
        stock_price["signal"] = 0
        stock_price.loc[
            (
                (stock_price["diff_sign"] > 0)
                & (stock_price["diff_sign_yesterday"] < 0)
            ),
            "signal",
        ] = 1
        stock_price.loc[
            (
                (stock_price["diff_sign"] < 0)
                & (stock_price["diff_sign_yesterday"] > 0)
            ),
            "signal",
        ] = -1
        return stock_price
