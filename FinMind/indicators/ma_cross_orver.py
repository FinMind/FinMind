import pandas as pd
from ta.trend import SMAIndicator


def add_ma_golden_death_cross_orver_indicators(
    stock_price: pd.DataFrame,
    ma_short_term_days: int = 10,
    ma_long_term_days: int = 30,
    **kwargs,
) -> pd.DataFrame:
    """
    url:
    "https://www.cmoney.tw/learn/course/technicalanalysisfast/topic/1811"

    summary:
    均線黃金交叉
    以短線操作來說，當 5日均線 向上突破 20日均線
    也就是短期的平均買進成本大於長期平均成本
    代表短期買方的力道較大，市場上大多數人獲利
    市場易走出「多頭」的趨勢，進而帶動長期均線向上，讓股價上漲機率較大
    短期線 突破 長期線(黃金交叉)，進場
    長期線 突破 短期線(死亡交叉)，出場
    """
    stock_price = stock_price.sort_values("date")
    stock_price[f"ma{ma_short_term_days}"] = SMAIndicator(
        stock_price["close"], ma_short_term_days
    ).sma_indicator()
    stock_price[f"ma{ma_long_term_days}"] = SMAIndicator(
        stock_price["close"], ma_long_term_days
    ).sma_indicator()
    stock_price["ma_diff"] = (
        stock_price[f"ma{ma_short_term_days}"]
        - stock_price[f"ma{ma_long_term_days}"]
    )
    stock_price["bool_signal"] = stock_price["ma_diff"].map(
        lambda x: 1 if x > 0 else -1
    )
    stock_price["bool_signal_shift1"] = (
        stock_price["bool_signal"].shift(1).fillna(0)
    )
    stock_price["bool_signal_shift1"] = stock_price[
        "bool_signal_shift1"
    ].astype(int)
    stock_price["MAGoldenDeathCrossOver"] = 0
    stock_price.loc[
        (
            (stock_price["bool_signal"] > 0)
            & (stock_price["bool_signal_shift1"] < 0)
        ),
        "MAGoldenDeathCrossOver",
    ] = 1
    stock_price.loc[
        (
            (stock_price["bool_signal"] < 0)
            & (stock_price["bool_signal_shift1"] > 0)
        ),
        "MAGoldenDeathCrossOver",
    ] = -1
    stock_price = stock_price.drop(
        [
            "ma_diff",
            "bool_signal",
            "bool_signal_shift1",
            f"ma{ma_short_term_days}",
            f"ma{ma_long_term_days}",
        ],
        axis=1,
    )
    return stock_price
