import typing
from enum import Enum

from pydantic import BaseModel

from FinMind.schema.data import Dataset
from FinMind.schema.rule import Rule


class Indicators(str, Enum):
    KD = "K"
    """ the formula of KD is k_days, defalt 9"""
    BIAS = "BIAS"
    """the formula of BIAS is ma_days, defalt 24"""
    ContinueHolding = "DollarCostAveraging"
    """
        the formula of ContinueHolding is buy_freq_day,
        Regular fixed-amount buy-and-hold strategy, buy once every n days,
        defalt 30
    """
    InstitutionalInvestorsFollower = "InstitutionalInvestorsFollower"
    """
        the formula of InstitutionalInvestorsFollower is n_days,
        if InstitutionalInvestors over buy n days,
        but the stock has not risen,
        so we will follow up and buy,
        defalt 10
    """
    KDGoldenDeathCrossOver = "KDGoldenDeathCrossOver"
    """
        the formula of KD is k_days, defalt 9,

        Indicators
            1 means Golden Cross Over,
            -1 means Death Cross Over
    """
    MAGoldenDeathCrossOver = "MAGoldenDeathCrossOver"
    """
        the formula of MA is [ma_short_term_days, ma_long_term_days]
        
        defalt [10, 30],

        Indicators
            1 means Golden Cross Over,
            -1 means Death Cross Over
    """
    InstitutionalInvestorsOverBuy = "InstitutionalInvestorsOverBuy"
    """
        the formula is None, it just calculates ( Buy - Sell )

        Indicators
            > 0 means OverBuy,
            < 0 means OverSell
    """
    ShortSaleMarginPurchaseRatio = "ShortSaleMarginPurchaseRatio"
    """
        the formula is None, it just calculates ( ShortSaleTodayBalance / MarginPurchaseTodayBalance )
    """


class IndicatorsParams(str, Enum):
    KD = "k_days"
    BIAS = "ma_days"
    ContinueHolding = "buy_freq_day"
    InstitutionalInvestorsFollower = "n_days"
    KDGoldenDeathCrossOver = "k_days"
    MAGoldenDeathCrossOver = ["ma_short_term_days", "ma_long_term_days"]
    InstitutionalInvestorsOverBuy = None
    ShortSaleMarginPurchaseRatio = None


class IndicatorsInfo(BaseModel):
    name: Indicators
    formula_value: typing.Union[
        typing.List[typing.Union[int, float, str]], int, float, str
    ] = None


class AddBuySellRule(BaseModel):
    indicators: Indicators
    more_or_less_than: Rule
    threshold: typing.Union[float, int, str]


class AdditionalDataset(str, Enum):
    InstitutionalInvestorsFollower = (
        Dataset.TaiwanStockInstitutionalInvestorsBuySell.value
    )
    InstitutionalInvestorsOverBuy = (
        Dataset.TaiwanStockInstitutionalInvestorsBuySell.value
    )
    ShortSaleMarginPurchaseRatio = (
        Dataset.TaiwanStockMarginPurchaseShortSale.value
    )
