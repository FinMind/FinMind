from enum import Enum


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
