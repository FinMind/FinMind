from FinMind.indicators.kd import add_kd_indicators
from FinMind.indicators.bias import add_bias_indicators
from FinMind.indicators.continue_holding import add_continue_holding_indicators
from FinMind.indicators.institutional_investors_follower import (
    add_institutional_investors_follower,
)

INDICATORS_MAPPING = dict(
    KD=add_kd_indicators,
    BIAS=add_bias_indicators,
    ContinueHolding=add_continue_holding_indicators,
    InstitutionalInvestorsFollower=add_institutional_investors_follower,
)
