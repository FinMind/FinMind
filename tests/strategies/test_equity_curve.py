"""BackTest 權益曲線 EverytimeTotalProfit 的純 unit test（不需 token / 不連網）"""

import numpy as np
import pandas as pd
import pytest

from FinMind.schema.data import Dataset
from FinMind.strategies.base import BackTest, Strategy

TRADER_FUND = 500000.0
DATES = ["2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05", "2024-01-08"]
OPEN_PRICE = [25.0, 25.0, 26.0, 24.0, 25.5]


class StubDataLoader:
    """只提供 BackTest 需要的最少資料"""

    def taiwan_stock_info(self):
        return pd.DataFrame(
            {"stock_id": ["0056"], "industry_category": ["ETF"]}
        )

    def get_data(self, dataset, data_id, start_date, end_date):
        if dataset == Dataset.TaiwanStockDividend:
            return pd.DataFrame()
        return pd.DataFrame(
            {
                "date": DATES,
                "stock_id": data_id,
                "open": OPEN_PRICE,
                "close": OPEN_PRICE,
            }
        )


def run_backtest(signal):
    class FixedSignal(Strategy):
        def create_trade_sign(self, stock_price, **kwargs):
            stock_price["signal"] = signal
            return stock_price

    backtest = BackTest(
        stock_id="0056",
        start_date=DATES[0],
        end_date=DATES[-1],
        trader_fund=TRADER_FUND,
        strategy=FixedSignal,
        data_loader=StubDataLoader(),
    )
    backtest.simulate()
    return backtest


def test_no_trade_keeps_equity():
    backtest = run_backtest([0, 0, 0, 0, 0])

    assert (backtest.trade_detail["EverytimeTotalProfit"] == TRADER_FUND).all()
    assert (backtest.compare_market_detail["CumDailyReturn"] == 0).all()


def test_buy_only_costs_trading_fees():
    # 第 0 天的訊號在第 1 天開盤以 25 元買進 1 張
    backtest = run_backtest([1, 0, 0, 0, 0])
    row = backtest.trade_detail.iloc[1]

    assert row["hold_volume"] == 1000
    # 權益 = 現金 + 持股以當下價格清算的淨值（扣賣出手續費與交易稅）
    liquidation_value = 25.0 * 1000 - 35.625 - 25.0
    assert row["EverytimeTotalProfit"] == pytest.approx(
        row["trader_fund"] + liquidation_value
    )
    # 只少了買進手續費 35.625、預估賣出手續費 35.625 與交易稅 25
    assert row["EverytimeTotalProfit"] == pytest.approx(499903.75)


def test_final_equity_matches_final_profit():
    # 第 1 天買進、第 3 天賣出，之後空手
    backtest = run_backtest([1, 0, -1, 0, 0])
    final_equity = backtest.trade_detail["EverytimeTotalProfit"].iloc[-1]
    final_profit = backtest.final_stats["FinalProfit"]

    assert final_equity - TRADER_FUND == pytest.approx(final_profit)
    cum_return = backtest.compare_market_detail["CumDailyReturn"].iloc[-1]
    assert cum_return == pytest.approx(
        np.log(final_equity / TRADER_FUND), abs=1e-5
    )
