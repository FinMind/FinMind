from FinMind.indicators.bias import add_bias_indicators
from FinMind.indicators.continue_holding import add_continue_holding_indicators
from FinMind.indicators.institutional_investors_follower import (
    add_institutional_investors_follower,
)
from FinMind.indicators.institutional_investors_over_buy import (
    add_institutional_investors_over_buy_indicators,
)
from FinMind.indicators.kd import add_kd_indicators
from FinMind.indicators.kd_crossover import (
    add_kd_golden_death_cross_over_indicators,
)
from FinMind.indicators.ma_cross_orver import (
    add_ma_golden_death_cross_orver_indicators,
)
from FinMind.indicators.short_sale_margin_purchase_ratio import (
    add_short_sale_margin_purchase_ratio_indicators,
)

INDICATORS_MAPPING = dict(
    KD=add_kd_indicators,
    BIAS=add_bias_indicators,
    ContinueHolding=add_continue_holding_indicators,
    InstitutionalInvestorsFollower=add_institutional_investors_follower,
    KDGoldenDeathCrossOver=add_kd_golden_death_cross_over_indicators,
    MAGoldenDeathCrossOver=add_ma_golden_death_cross_orver_indicators,
    InstitutionalInvestorsOverBuy=add_institutional_investors_over_buy_indicators,
    ShortSaleMarginPurchaseRatio=add_short_sale_margin_purchase_ratio_indicators,
)
