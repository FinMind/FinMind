from FinMind.BackTestSystem.BaseClass import Strategy


class ContinueHolding(Strategy):
    buy_freq_day = 30

    def init(self, base_data):
        base_data["signal"] = (base_data.index % self.buy_freq_day == 0).astype(
            int
        )
        return base_data
