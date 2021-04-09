from ta.momentum import StochasticOscillator
import pandas as pd
from FinMind.BackTestSystem.BaseClass import Strategy


class NaiveKd(Strategy):
    """
    url: "https://www.mirrormedia.mg/story/20180719fin012/"
    summary:
        日KD 80 20
        日K線 <= 20 進場
        日K線 >= 80 出場
    """

    kdays = 9
    ddays = 3
    kd_upper = 80
    kd_lower = 20

    def add_indicator(self,
        kdays: int,
        ddays: int,
        kd_upper: int, 
        kd_lower: int
    ):
        self.kdays = kdays
        self.ddays = ddays
        self.kd_upper = kd_upper
        self.kd_lower = kd_lower

    def create_trade_sign(self, stock_price: pd.DataFrame) -> pd.DataFrame:
        stock_price = stock_price.sort_values("date")
        kd = StochasticOscillator(
            high=stock_price["max"],
            low=stock_price["min"],
            close=stock_price["close"],
            n=self.kdays,
            d_n=self.ddays,
        )
        stock_price["K"] = kd.stoch()
        stock_price["D"] = kd.stoch_signal()
        stock_price.index = range(len(stock_price))
        stock_price["signal"] = 0
        stock_price.loc[stock_price["K"] <= self.kd_lower, "signal"] = 1
        stock_price.loc[stock_price["K"] >= self.kd_upper, "signal"] = -1
        return stock_price
