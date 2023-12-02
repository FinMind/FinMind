from enum import Enum

from pydantic import BaseModel

from FinMind.schema.rule import Rule
import typing


class Indicators(str, Enum):
    KD = "K"
    BIAS = "BIAS"
    ContinueHolding = "DollarCostAveraging"
    InstitutionalInvestorsFollower = "InstitutionalInvestorsOverBuy"


class IndicatorsParams(str, Enum):
    KD = "k_days"
    BIAS = "ma_days"
    ContinueHolding = "buy_freq_day"
    InstitutionalInvestorsFollower = None


class AddBuySellRule(BaseModel):
    indicators: Indicators
    more_or_less_than: Rule
    threshold: typing.Union[int, float, str]
