import pandas as pd

from FinMind.strategies.base import Strategy
from FinMind.indicators import add_continue_holding_indicators


class ContinueHolding(Strategy):
    """
    summary:
        定期定額買進持有策略，每30天買進一次
    """

    buy_freq_day = 30

    def create_trade_sign(
        self, stock_price: pd.DataFrame, **kwargs
    ) -> pd.DataFrame:
        stock_price = add_continue_holding_indicators(
            stock_price=stock_price, buy_freq_day=self.buy_freq_day
        )
        stock_price["signal"] = stock_price["DollarCostAveraging"]
        return stock_price
