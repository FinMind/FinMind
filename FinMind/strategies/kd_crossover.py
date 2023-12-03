import pandas as pd

from FinMind.indicators import add_kd_golden_death_cross_over_indicators
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

    def create_trade_sign(
        self, stock_price: pd.DataFrame, **kwargs
    ) -> pd.DataFrame:
        stock_price = add_kd_golden_death_cross_over_indicators(
            stock_price=stock_price, k_days=self.k_days
        )
        stock_price["signal"] = stock_price["KDGoldenDeathCrossOver"]
        stock_price = stock_price.drop(["KDGoldenDeathCrossOver"], axis=1)
        return stock_price
