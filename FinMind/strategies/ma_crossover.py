import pandas as pd

from FinMind.indicators import add_ma_golden_death_cross_orver_indicators
from FinMind.strategies.base import Strategy


class MaCrossOver(Strategy):
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

    ma_fast_days = 10
    ma_slow_days = 30

    def create_trade_sign(
        self, stock_price: pd.DataFrame, **kwargs
    ) -> pd.DataFrame:
        stock_price = add_ma_golden_death_cross_orver_indicators(
            stock_price=stock_price,
            ma_short_term_days=self.ma_fast_days,
            ma_long_term_days=self.ma_slow_days,
        )
        stock_price["signal"] = stock_price["MAGoldenDeathCrossOver"]
        stock_price = stock_price.drop(["MAGoldenDeathCrossOver"], axis=1)
        return stock_price
