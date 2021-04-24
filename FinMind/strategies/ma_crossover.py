import pandas as pd
from ta.trend import SMAIndicator

from FinMind.strategies.base import Strategy


class MaCrossOver(Strategy):
    """
    url:
    "https://www.cmoney.tw/learn/course/technicalanalysisfast/topic/1811"

    summary:
    均線黃金交叉
    以短線操作來說，當 5日均線 向上突破 20日均線
    也就是短期的平均買進成本大於長期平均成本
    代表短期買方的力道較大，市場上大多數人獲利
    市場易走出「多頭」的趨勢，進而帶動長期均線向上，讓股價上漲機率較大
    短期線 突破 長期線(黃金交叉)，進場
    長期線 突破 短期線(死亡交叉)，出場
    """

    ma_fast_days = 10
    ma_slow_days = 30

    def create_trade_sign(self, stock_price: pd.DataFrame) -> pd.DataFrame:
        stock_price = stock_price.sort_values("date")
        stock_price[f"ma{self.ma_fast_days}"] = SMAIndicator(
            stock_price["close"], self.ma_fast_days
        ).sma_indicator()
        stock_price[f"ma{self.ma_slow_days}"] = SMAIndicator(
            stock_price["close"], self.ma_slow_days
        ).sma_indicator()
        stock_price["ma_diff"] = (
            stock_price[f"ma{self.ma_fast_days}"]
            - stock_price[f"ma{self.ma_slow_days}"]
        )
        stock_price["bool_signal"] = stock_price["ma_diff"].map(
            lambda x: 1 if x > 0 else -1
        )
        stock_price["bool_signal_shift1"] = (
            stock_price["bool_signal"].shift(1).fillna(0)
        )
        stock_price["bool_signal_shift1"] = stock_price[
            "bool_signal_shift1"
        ].astype(int)
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
        return stock_price
