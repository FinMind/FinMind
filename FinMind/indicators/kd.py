import numpy as np
import pandas as pd
from ta.momentum import StochasticOscillator


def add_kd_indicators(
    stock_price: pd.DataFrame, k_days: int = 9, **kwargs
) -> pd.DataFrame:
    stock_price = stock_price.sort_values("date")
    kd = StochasticOscillator(
        high=stock_price["max"],
        low=stock_price["min"],
        close=stock_price["close"],
        n=k_days,
    )
    rsv_ = kd.stoch().fillna(50)
    _k = np.zeros(stock_price.shape[0])
    # _d = np.zeros(stock_price.shape[0])
    for i, r in enumerate(rsv_):
        if i == 0:
            _k[i] = 50
        else:
            _k[i] = _k[i - 1] * 2 / 3 + r / 3

    stock_price["K"] = _k
    return stock_price
