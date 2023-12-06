import numpy as np
import pandas as pd
from ta.momentum import StochasticOscillator


def add_kd_golden_death_cross_over_indicators(
    stock_price: pd.DataFrame, k_days: int = 9, **kwargs
) -> pd.DataFrame:
    """
    url: "http://smart.businessweekly.com.tw/Reading/WebArticle.aspx?id=68129&p=2"
    summary: 日KD黃金交叉和死亡交叉
            日K線 < 日D線，翻轉成，日K線 > 日D線 稱為黃金交叉
            日K線 > 日D線，翻轉成，日K線 < 日D線 稱為死亡交叉
            黃金交叉進場，死亡交叉出場
    """
    stock_price = stock_price.sort_values("date")
    kd = StochasticOscillator(
        high=stock_price["max"],
        low=stock_price["min"],
        close=stock_price["close"],
        n=k_days,
    )
    rsv_ = kd.stoch().fillna(50)
    _k = np.zeros(stock_price.shape[0])
    _d = np.zeros(stock_price.shape[0])
    for i, r in enumerate(rsv_):
        if i == 0:
            _k[i] = 50
            _d[i] = 50
        else:
            _k[i] = _k[i - 1] * 2 / 3 + r / 3
            _d[i] = _d[i - 1] * 2 / 3 + _k[i] / 3
    stock_price["K"] = _k
    stock_price["D"] = _d
    stock_price.index = range(len(stock_price))
    stock_price["diff"] = stock_price["K"] - stock_price["D"]
    stock_price.loc[(stock_price.index < k_days), "diff"] = np.nan
    stock_price["diff_sign"] = stock_price["diff"].map(
        lambda x: 1 if x >= 0 else (-1 if x < 0 else 0)
    )
    stock_price["diff_sign_yesterday"] = (
        stock_price["diff_sign"].shift(1).fillna(0).astype(int)
    )
    stock_price["KDGoldenDeathCrossOver"] = 0
    stock_price.loc[
        (
            (stock_price["diff_sign"] > 0)
            & (stock_price["diff_sign_yesterday"] < 0)
        ),
        "KDGoldenDeathCrossOver",
    ] = 1
    stock_price.loc[
        (
            (stock_price["diff_sign"] < 0)
            & (stock_price["diff_sign_yesterday"] > 0)
        ),
        "KDGoldenDeathCrossOver",
    ] = -1
    stock_price = stock_price.drop(
        ["diff", "diff_sign", "diff_sign_yesterday"], axis=1
    )
    return stock_price
