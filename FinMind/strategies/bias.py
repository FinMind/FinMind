import pandas as pd
from ta.trend import SMAIndicator

from FinMind.strategies.base import Strategy
from FinMind.indicators import add_bias_indicators


class Bias(Strategy):
    """
    url:
    "https://bc8800.pixnet.net/blog/post/ \
        328645973-%E7%A8%8B%E5%BC%8F%E4%BA%A4 \
        %E6%98%93%E4%B9%8B%E7%A0%94%E7%A9%B6% \
        E7%AD%86%E8%A8%98---%E4%B9%96%E9%9B%A2%E7%8E%87"

    summary:
    乖離率策略是觀察股價偏離移動平均線(MA線)的程度來決定是否進場
        負乖離表示股價 低 於過去一段時間平均價，意味著股價相對過去 低 ，所以選擇進場
        正乖離表示股價 高 於過去一段時間平均價，意味著股價相對過去 高 ，所以選擇出場
    """

    ma_days = 24
    bias_lower = -7
    bias_upper = 8

    def create_trade_sign(
        self, stock_price: pd.DataFrame, **kwargs
    ) -> pd.DataFrame:
        stock_price = add_bias_indicators(
            stock_price=stock_price, ma_days=self.ma_days
        )
        stock_price["signal"] = stock_price["BIAS"].map(
            lambda x: (
                1 if x < self.bias_lower else (-1 if x > self.bias_upper else 0)
            )
        )

        stock_price["signal"] = stock_price["signal"].fillna(0)
        return stock_price
