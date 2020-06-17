from ta.momentum import StochasticOscillator

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

    def init(self, base_data):
        base_data = base_data.sort_values("date")

        kd = StochasticOscillator(
            high=base_data["max"],
            low=base_data["min"],
            close=base_data["close"],
            n=self.kdays,
            d_n=self.ddays,
        )
        base_data["K"] = kd.stoch()
        base_data["D"] = kd.stoch_signal()

        base_data.index = range(len(base_data))

        base_data["signal"] = 0
        base_data.loc[base_data["K"] <= self.kd_lower, "signal"] = 1
        base_data.loc[base_data["K"] >= self.kd_upper, "signal"] = -1
        return base_data
