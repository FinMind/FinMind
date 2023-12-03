import typing
from enum import Enum

from pydantic import BaseModel

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
    InstitutionalInvestorsFollower = "InstitutionalInvestorsOverBuy"
    """
        the formula of InstitutionalInvestorsFollower is n_days,
        if InstitutionalInvestors over buy n days,
        but the stock has not risen,
        so we will follow up and buy,
        defalt 10
    """
    KDGoldenDeathCrossOver = "kd_golden_death_cross_over"
    """
        the formula of KD is k_days, defalt 9,

        Indicators
            1 means Golden Cross Over,
            -1 means Death Cross Over
    """


class IndicatorsParams(str, Enum):
    KD = "k_days"
    BIAS = "ma_days"
    ContinueHolding = "buy_freq_day"
    InstitutionalInvestorsFollower = "n_days"
    KDGoldenDeathCrossOver = "k_days"


class IndicatorsInfo(BaseModel):
    name: Indicators
    formula_value: typing.Union[int, float, str] = None


class AddBuySellRule(BaseModel):
    indicators: Indicators
    more_or_less_than: Rule
    threshold: typing.Union[int, float, str]
