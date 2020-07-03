from ta.trend import SMAIndicator

from FinMind.BackTestSystem.BaseClass import Strategy


class MaxMinPeriodBias(Strategy):
    """
    url: http://www.bituzi.com/2013/03/bias.html

    summary:
    乖離率加上最近 k 天最大最小值進出法
    單存乖離率來判斷進出相對而言比較不穩定，因此多一個限制是跟最近 k 天最大最小值股價做比較來段進出
    負乖離表示股價 低 於過去一段時間平均價且股價大於過去k天最大值，意味著股價相對過去 低 且即將走高 ，則選擇進場
    正乖離表示股價 高 於過去一段時間平均價且股價大於過去k天最小值，意味著股價相對過去 高 且即將走低，則選擇出場
    相對於單存乖離率而言來的保守
    """

    ma_days = 24
    last_k_days = 5
    bais_lower = -7
    bais_upper = 8

    def init(self, base_data):
        base_data = base_data.sort_values("date")

        base_data[f"ma{self.ma_days}"] = SMAIndicator(
            base_data["close"], self.ma_days
        ).sma_indicator()

        base_data["bias"] = (
            (base_data["close"] - base_data[f"ma{self.ma_days}"])
            / base_data[f"ma{self.ma_days}"]
        ) * 100

        base_data[f"max_last_k_days{self.last_k_days}"] = (
            base_data["close"].shift(1).rolling(window=self.last_k_days).max()
        )

        base_data[f"min_last_k_days{self.last_k_days}"] = (
            base_data["close"].shift(1).rolling(window=self.last_k_days).min()
        )

        base_data["signal"] = 0
        base_data.loc[
            (
                (base_data["bias"] < self.bais_lower)
                & (
                    base_data["close"]
                    > base_data[f"max_last_k_days{self.last_k_days}"]
                )
            ),
            "signal",
        ] = 1
        base_data.loc[
            (
                (base_data["bias"] > self.bais_upper)
                & (
                    base_data["close"]
                    < base_data[f"min_last_k_days{self.last_k_days}"]
                )
            ),
            "signal",
        ] = -1

        return base_data
