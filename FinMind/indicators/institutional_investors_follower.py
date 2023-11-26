import typing

import numpy as np
import pandas as pd

from FinMind.schema.data import Dataset


def add_institutional_investors_follower(
    stock_price: pd.DataFrame, additional_dataset_obj, **kwargs
) -> pd.DataFrame:
    stock_price = stock_price.sort_values("date")
    institutional_investors_buy_sell = getattr(
        additional_dataset_obj, Dataset.TaiwanStockInstitutionalInvestorsBuySell
    )
    institutional_investors_buy_sell = institutional_investors_buy_sell.groupby(
        ["date", "stock_id"], as_index=False
    ).agg({"buy": np.sum, "sell": np.sum})
    institutional_investors_buy_sell["diff"] = (
        institutional_investors_buy_sell["buy"]
        - institutional_investors_buy_sell["sell"]
    )
    stock_price = pd.merge(
        stock_price,
        institutional_investors_buy_sell[["stock_id", "date", "diff"]],
        on=["stock_id", "date"],
        how="left",
    ).fillna(0)
    stock_price["InstitutionalInvestorsOverBuy"] = __detect_Abnormal_Peak(
        y=stock_price["diff"].values,
        lag=10,
        threshold=3,
        influence=0.35,
    )
    stock_price = stock_price.drop(["diff"], axis=1)
    return stock_price


def __detect_Abnormal_Peak(
    y: np.array, lag: int, threshold: float, influence: float
) -> typing.List[float]:
    signals = np.zeros(len(y))
    filtered_y = np.array(y)
    avg_filter = [0] * len(y)
    std_filter = [0] * len(y)
    avg_filter[lag - 1] = np.mean(y[0:lag])
    std_filter[lag - 1] = np.std(y[0:lag])
    for i in range(lag, len(y)):
        if abs(y[i] - avg_filter[i - 1]) > threshold * std_filter[i - 1]:
            if y[i] > avg_filter[i - 1]:
                signals[i] = 1
            else:
                signals[i] = -1

            filtered_y[i] = (
                influence * y[i] + (1 - influence) * filtered_y[i - 1]
            )
            avg_filter[i] = np.mean(filtered_y[(i - lag + 1) : i + 1])
            std_filter[i] = np.std(filtered_y[(i - lag + 1) : i + 1])
        else:
            signals[i] = 0
            filtered_y[i] = y[i]
            avg_filter[i] = np.mean(filtered_y[(i - lag + 1) : i + 1])
            std_filter[i] = np.std(filtered_y[(i - lag + 1) : i + 1])
    return list(signals)
