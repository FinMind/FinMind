import pandas as pd

from FinMind.strategies.base import Strategy


class ContinueHolding(Strategy):
    """
    summary:
        定期定額買進持有策略，每30天買進一次
    """

    buy_freq_day = 30

    def create_trade_sign(self, stock_price: pd.DataFrame) -> pd.DataFrame:
        '''
        create indicator
        '''
        # stock_price["signal"] = (
        #     stock_price.index % self.buy_freq_day == 0
        # ).astype(int)
        return stock_price

    def next(self):
        signal = 1 if self.stock_price.index[-1] % self.buy_freq_day == 0 else 0

        trade_price = self.stock_price["open"].values[-1]
        trade_lots = signal

        if signal > 0:
            self.buy(trade_price=trade_price, trade_lots=trade_lots)
        elif signal < 0:
            self.sell(trade_price=trade_price, trade_lots=trade_lots)
        else:
            self.no_action(trade_price=trade_price)