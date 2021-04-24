import pandas as pd
from ta.momentum import StochasticOscillator

from FinMind.strategies.base import Strategy


class NaiveKd(Strategy):
    """
    url: "https://school.stockcharts.com/doku.php?id=technical_indicators:stochastic_oscillator_fast_slow_and_full"
    summary:
        kd計算方式相較於網路上 kd 交易策略有些微差距，但概念是相同的
        日KD 80 20
        日K線 <= 20 進場
        日K線 >= 80 出場
    """

    k_days = 9
    d_days = 3
    kd_upper = 80
    kd_lower = 20

    def create_trade_sign(self, stock_price: pd.DataFrame) -> pd.DataFrame:
        stock_price = stock_price.sort_values("date")
        kd = StochasticOscillator(
            high=stock_price["max"],
            low=stock_price["min"],
            close=stock_price["close"],
            n=self.k_days,
            d_n=self.d_days,
        )
        stock_price["K"] = kd.stoch()
        stock_price["D"] = kd.stoch_signal()
        stock_price.index = range(len(stock_price))
        stock_price["signal"] = 0
        stock_price.loc[stock_price["K"] <= self.kd_lower, "signal"] = 1
        stock_price.loc[stock_price["K"] >= self.kd_upper, "signal"] = -1
        return stock_price
