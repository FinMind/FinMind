import pandas as pd
from ta.trend import SMAIndicator

from FinMind.strategies.base import Strategy


class MaxMinPeriodBias(Strategy):
    """
    url: http://www.bituzi.com/2013/03/bias.html

    summary:
    乖離率加上最近 k 天最大最小值進出法
    單純乖離率來判斷進出相對而言比較不穩定，因此多一個限制是跟最近 k 天最大最小值股價做比較來段進出
    負乖離表示股價 低 於過去一段時間平均價且股價大於過去k天最大值，意味著股價相對過去 低 且即將走高，則選擇進場
    正乖離表示股價 高 於過去一段時間平均價且股價大於過去k天最小值，意味著股價相對過去 高 且即將走低，則選擇出場
    相對於單純乖離率而言來的保守
    """

    ma_days = 24
    last_k_days = 5
    bias_lower = -7
    bias_upper = 8

    def create_trade_sign(self, stock_price: pd.DataFrame) -> pd.DataFrame:
        stock_price = stock_price.sort_values("date")
        stock_price[f"ma{self.ma_days}"] = SMAIndicator(
            stock_price["close"], self.ma_days
        ).sma_indicator()
        stock_price["bias"] = (
            (stock_price["close"] - stock_price[f"ma{self.ma_days}"])
            / stock_price[f"ma{self.ma_days}"]
        ) * 100
        stock_price[f"max_last_k_days{self.last_k_days}"] = (
            stock_price["close"].shift(1).rolling(window=self.last_k_days).max()
        )
        stock_price[f"min_last_k_days{self.last_k_days}"] = (
            stock_price["close"].shift(1).rolling(window=self.last_k_days).min()
        )
        stock_price["signal"] = 0
        stock_price.loc[
            (
                (stock_price["bias"] < self.bias_lower)
                & (
                    stock_price["close"]
                    > stock_price[f"max_last_k_days{self.last_k_days}"]
                )
            ),
            "signal",
        ] = 1
        stock_price.loc[
            (
                (stock_price["bias"] > self.bias_upper)
                & (
                    stock_price["close"]
                    < stock_price[f"min_last_k_days{self.last_k_days}"]
                )
            ),
            "signal",
        ] = -1
        return stock_price
