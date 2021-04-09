from FinMind.BackTestSystem.BaseClass import Strategy
import pandas as pd


class ContinueHolding(Strategy):
    buy_freq_day = 30

    def add_indicator(self,
        buy_freq_day: int,
    ):
        self.buy_freq_day = buy_freq_day


    def create_trade_sign(self, stock_price: pd.DataFrame) -> pd.DataFrame:
        stock_price["signal"] = (
            stock_price.index % self.buy_freq_day == 0
        ).astype(int)
        return stock_price
