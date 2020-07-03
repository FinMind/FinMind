import numpy as np
from ta.momentum import StochasticOscillator

from FinMind.BackTestSystem.BaseClass import Strategy


class Kd(Strategy):
    """
    url: "https://www.mirrormedia.mg/story/20180719fin012/"
    summary:
        日KD 80 20
        日K線 <= 20 進場
        日K線 >= 80 出場
    """

    kdays = 9
    kd_upper = 80
    kd_lower = 20

    def init(self, base_data):
        base_data = base_data.sort_values("date")

        kd = StochasticOscillator(
            high=base_data["max"],
            low=base_data["min"],
            close=base_data["close"],
            n=self.kdays,
        )
        rsv_ = kd.stoch().fillna(50)

        _k = np.zeros(base_data.shape[0])
        _d = np.zeros(base_data.shape[0])
        for i, r in enumerate(rsv_):
            if i == 0:
                _k[i] = 50
                _d[i] = 50
            else:
                _k[i] = _k[i - 1] * 2 / 3 + r / 3
                _d[i] = _d[i - 1] * 2 / 3 + _k[i] / 3

        base_data["K"] = _k
        base_data["D"] = _d

        base_data.index = range(len(base_data))

        base_data["signal"] = 0
        base_data.loc[base_data["K"] <= self.kd_lower, "signal"] = 1
        base_data.loc[base_data["K"] >= self.kd_upper, "signal"] = -1
        return base_data
