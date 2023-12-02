import pandas as pd


def add_continue_holding_indicators(
    stock_price: pd.DataFrame, buy_freq_day: int = 30, **kwargs
) -> pd.DataFrame:
    """
    summary:
        定期定額買進持有策略，每 n 天買進一次
    """
    stock_price["DollarCostAveraging"] = (
        stock_price.index % buy_freq_day == 0
    ).astype(int)
    return stock_price
