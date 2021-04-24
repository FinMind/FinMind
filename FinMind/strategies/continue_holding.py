import pandas as pd

from FinMind.strategies.base import Strategy


class ContinueHolding(Strategy):
    """
    summary:
        定期定額買進持有策略，每30天買進一次
    """

    buy_freq_day = 30

    def create_trade_sign(self, stock_price: pd.DataFrame) -> pd.DataFrame:
        stock_price["signal"] = (
            stock_price.index % self.buy_freq_day == 0
        ).astype(int)
        return stock_price
