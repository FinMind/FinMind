from ta.trend import MACD

from FinMind.BackTestSystem.BaseClass import Strategy


class MacdCrossOver(Strategy):
    """
    url:https://www.cmoney.tw/learn/course/technicals/topic/750

    summary:
    MACD 指標由 DIF 與 MACD 兩條線組成
    DIF（快）短期，判斷股價趨勢的變化
    MACD（慢）長期，判斷股價大趨勢
    短期線 突破 長期線(黃金交叉)，進場
    長期線 突破 短期線(死亡交叉)，出場
    """

    def init(self, base_data):
        base_data = base_data.sort_values("date")

        macd = MACD(close=base_data["close"], n_slow=26, n_fast=12, n_sign=9)

        base_data["macd_diff"] = macd.macd_diff()
        base_data["macd_signal"] = macd.macd_signal()

        base_data["fs_dif"] = base_data["macd_diff"] - base_data["macd_signal"]
        base_data["bool_signal"] = base_data["fs_dif"].map(
            lambda x: 1 if x > 0 else -1
        )
        base_data["bool_signal_shift1"] = base_data["bool_signal"].shift(1)

        base_data["signal"] = 0
        base_data.loc[
            (
                (base_data["bool_signal"] > 0)
                & (base_data["bool_signal_shift1"] < 0)
            ),
            "signal",
        ] = 1
        base_data.loc[
            (
                (base_data["bool_signal"] < 0)
                & (base_data["bool_signal_shift1"] > 0)
            ),
            "signal",
        ] = -1

        base_data.index = range(len(base_data))
        return base_data
