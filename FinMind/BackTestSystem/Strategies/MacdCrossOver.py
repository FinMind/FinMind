from ta.trend import MACD
import pandas as pd
from FinMind.BackTestSystem.BaseClass import Strategy


class MacdCrossOver(Strategy):
    """
    url:https://www.cmoney.tw/learn/course/technicals/topic/750

    summary:
    MACD 指標由 DIF 與 MACD 兩條線組成
    DIF（快）短期，判斷股價趨勢的變化
    MACD（慢）長期，判斷股價大趨勢
    短期線 突破 長期線(黃金交叉)，進場
    長期線 突破 短期線(死亡交叉)，出場
    """

    def create_trade_sign(self, stock_price: pd.DataFrame) -> pd.DataFrame:
        stock_price = stock_price.sort_values("date")
        macd = MACD(close=stock_price["close"], n_slow=26, n_fast=12, n_sign=9)
        stock_price["macd_diff"] = macd.macd_diff()
        stock_price["macd_signal"] = macd.macd_signal()
        stock_price["fs_dif"] = (
            stock_price["macd_diff"] - stock_price["macd_signal"]
        )
        stock_price["bool_signal"] = stock_price["fs_dif"].map(
            lambda x: 1 if x > 0 else -1
        )
        stock_price["bool_signal_shift1"] = stock_price["bool_signal"].shift(1)
        stock_price["signal"] = 0
        stock_price.loc[
            (
                (stock_price["bool_signal"] > 0)
                & (stock_price["bool_signal_shift1"] < 0)
            ),
            "signal",
        ] = 1
        stock_price.loc[
            (
                (stock_price["bool_signal"] < 0)
                & (stock_price["bool_signal_shift1"] > 0)
            ),
            "signal",
        ] = -1
        stock_price.index = range(len(stock_price))
        return stock_price
