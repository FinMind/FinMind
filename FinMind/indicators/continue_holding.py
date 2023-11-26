import pandas as pd


def add_continue_holding_indicators(
    stock_price: pd.DataFrame, buy_freq_day: int = 30, **kwargs
) -> pd.DataFrame:
    stock_price["DollarCostAveraging"] = (
        stock_price.index % buy_freq_day == 0
    ).astype(int)
    return stock_price
