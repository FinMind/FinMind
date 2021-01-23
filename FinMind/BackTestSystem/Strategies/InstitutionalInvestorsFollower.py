import typing

import numpy as np
import pandas as pd
from FinMind.BackTestSystem.BaseClass import Strategy
from FinMind.Data import Load


class InstitutionalInvestorsFollower(Strategy):
    """
    url: "https://www.finlab.tw/%E8%85%A6%E5%8A%9B%E6%BF%80%E7%9B%AA%E7%9A%84%E5%A4%96%E8%B3%87%E7%AD%96%E7%95%A5%EF%BC%81/"
    summary:
        策略概念: 法人大量買超會導致股價上漲, 賣超反之
        策略規則: 三大法人大量買超隔天就賣，大量賣超就買
    """

    def create_trade_sign(self, stock_price: pd.DataFrame) -> pd.DataFrame:
        stock_price = stock_price.sort_values("date")
        stock_price.index = range(len(stock_price))
        InstitutionalInvestorsBuySell = Load.FinData(
            dataset="InstitutionalInvestorsBuySell",
            select=self.stock_id,
            date=self.start_date,
            end_date=self.end_date,
        )
        InstitutionalInvestorsBuySell = InstitutionalInvestorsBuySell.groupby(
            ["date", "stock_id"], as_index=False
        ).agg({"buy": np.sum, "sell": np.sum})
        InstitutionalInvestorsBuySell["diff"] = (
            InstitutionalInvestorsBuySell["buy"]
            - InstitutionalInvestorsBuySell["sell"]
        )
        stock_price = pd.merge(
            stock_price,
            InstitutionalInvestorsBuySell[["stock_id", "date", "diff"]],
            on=["stock_id", "date"],
            how="left",
        ).fillna(0)
        stock_price["signal_info"] = self.detect_Abnormal_Peak(
            y=stock_price["diff"].values,
            lag=10,
            threshold=3,
            influence=0.35,
        )
        stock_price["signal"] = 0
        stock_price.loc[stock_price["signal_info"] == -1, "signal"] = 1
        stock_price.loc[stock_price["signal_info"] == 1, "signal"] = -1
        return stock_price

    def detect_Abnormal_Peak(
        self, y: np.array, lag: int, threshold: float, influence: float
    ) -> typing.List[float]:
        signals = np.zeros(len(y))
        filteredY = np.array(y)
        avgFilter = [0] * len(y)
        stdFilter = [0] * len(y)
        avgFilter[lag - 1] = np.mean(y[0:lag])
        stdFilter[lag - 1] = np.std(y[0:lag])
        for i in range(lag, len(y)):
            if abs(y[i] - avgFilter[i - 1]) > threshold * stdFilter[i - 1]:
                if y[i] > avgFilter[i - 1]:
                    signals[i] = 1
                else:
                    signals[i] = -1

                filteredY[i] = (
                    influence * y[i] + (1 - influence) * filteredY[i - 1]
                )
                avgFilter[i] = np.mean(filteredY[(i - lag + 1) : i + 1])
                stdFilter[i] = np.std(filteredY[(i - lag + 1) : i + 1])
            else:
                signals[i] = 0
                filteredY[i] = y[i]
                avgFilter[i] = np.mean(filteredY[(i - lag + 1) : i + 1])
                stdFilter[i] = np.std(filteredY[(i - lag + 1) : i + 1])
        return list(signals)
