import numpy as np
import pandas as pd
from ta.trend import SMAIndicator


def add_bias_indicators(
    stock_price: pd.DataFrame, ma_days: int = 24, **kwargs
) -> pd.DataFrame:
    stock_price = stock_price.sort_values("date")
    stock_price[f"ma{ma_days}"] = SMAIndicator(
        stock_price["close"], ma_days
    ).sma_indicator()
    stock_price["BIAS"] = (
        (stock_price["close"] - stock_price[f"ma{ma_days}"])
        / stock_price[f"ma{ma_days}"]
    ) * 100
    stock_price = stock_price.drop(f"ma{ma_days}", axis=1)
    return stock_price
