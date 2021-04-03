import numpy as np
import pandas as pd
from ta.momentum import StochasticOscillator

from FinMind.strategies.base import Strategy


class Kd(Strategy):
    """
    url: "https://www.mirrormedia.mg/story/20180719fin012/"
    summary:
        網路上常見的 kd 交易策略
        日KD 80 20
        日K線 <= 20 進場
        日K線 >= 80 出場
    """

    k_days = 9
    kd_upper = 80
    kd_lower = 20

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
        stock_price["signal"] = 0
        stock_price.loc[stock_price["K"] <= self.kd_lower, "signal"] = 1
        stock_price.loc[stock_price["K"] >= self.kd_upper, "signal"] = -1
        return stock_price
