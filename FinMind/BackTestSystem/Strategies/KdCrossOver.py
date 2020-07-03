import numpy as np
from ta.momentum import StochasticOscillator

from FinMind.BackTestSystem.BaseClass import Strategy


class KdCrossOver(Strategy):
    """
    url: "http://smart.businessweekly.com.tw/Reading/WebArticle.aspx?id=68129&p=2"
    summary: 日KD黃金交叉和死亡交叉
            日K線 小於 日D線 翻轉成 日K線 大於 日D線 稱為黃金交叉
            日K線 大於 日D線 翻轉成 日K線 小於 日D線 稱為死亡交叉
            黃金交叉進場，死亡交叉出場
    """

    kdays = 9

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

        base_data["diff"] = base_data["K"] - base_data["D"]
        base_data.loc[(base_data.index < self.kdays), "diff"] = np.nan

        base_data["bool_diff"] = base_data["diff"].map(
            lambda x: 1 if x >= 0 else (-1 if x < 0 else 0)
        )
        base_data["bool_diff_shift1"] = (
            base_data["bool_diff"].shift(1).fillna(0).astype(int)
        )

        base_data["signal"] = 0
        base_data.loc[
            (
                (base_data["bool_diff"] > 0)
                & (base_data["bool_diff_shift1"] < 0)
            ),
            "signal",
        ] = 1
        base_data.loc[
            (
                (base_data["bool_diff"] < 0)
                & (base_data["bool_diff_shift1"] > 0)
            ),
            "signal",
        ] = -1
        return base_data
