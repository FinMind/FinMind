import pandas as pd
from ta.trend import MACD

from FinMind.strategies.base import Strategy


class MacdCrossOver(Strategy):
    """
    url:https://www.cmoney.tw/learn/course/technicals/topic/750

    summary:
    MACD 指標由 DIF 與 MACD 兩條線組成
    差離值(DIF值)，短期，判斷股價趨勢的變化
    訊號線(DEM值，又稱MACD值)，長期，判斷股價大趨勢
    短期線 突破 長期線(黃金交叉)，進場
    長期線 突破 短期線(死亡交叉)，出場
    """

    @staticmethod
    def create_trade_sign(stock_price: pd.DataFrame) -> pd.DataFrame:
        stock_price = stock_price.sort_values("date")
        macd = MACD(close=stock_price["close"], n_slow=26, n_fast=12, n_sign=9)
        stock_price["DIF"] = macd.macd_diff()
        stock_price["MACD"] = macd.macd_signal()
        stock_price["OSC"] = stock_price["DIF"] - stock_price["MACD"]
        stock_price["OSC_signal"] = stock_price["OSC"].map(
            lambda x: 1 if x > 0 else -1
        )
        stock_price["OSC_signal_yesterday"] = stock_price["OSC_signal"].shift(1)
        stock_price["signal"] = 0
        stock_price.loc[
            (
                (stock_price["OSC_signal"] > 0)
                & (stock_price["OSC_signal_yesterday"] < 0)
            ),
            "signal",
        ] = 1  # 下而上穿過
        stock_price.loc[
            (
                (stock_price["OSC_signal"] < 0)
                & (stock_price["OSC_signal_yesterday"] > 0)
            ),
            "signal",
        ] = -1  # 上而下穿過
        stock_price.index = range(len(stock_price))
        return stock_price
