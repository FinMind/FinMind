import numpy as np
import pandas as pd
from ta.momentum import StochasticOscillator

from FinMind.strategies.base import Strategy
from FinMind.indicators import add_kd_indicators


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

    def create_trade_sign(
        self, stock_price: pd.DataFrame, **kwargs
    ) -> pd.DataFrame:
        stock_price = add_kd_indicators(
            stock_price=stock_price, k_days=self.k_days
        )
        stock_price["signal"] = 0
        stock_price.loc[stock_price["K"] <= self.kd_lower, "signal"] = 1
        stock_price.loc[stock_price["K"] >= self.kd_upper, "signal"] = -1
        return stock_price
