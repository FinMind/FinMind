"""BackTest.__compute_div_income 的純 unit test（不需 token / 不連網）"""

import pytest

from FinMind.strategies.base import BackTest, Trader

# private static method, 需透過 name mangling 取用
compute_div_income = BackTest._BackTest__compute_div_income


def make_trader(
    hold_volume: float = 1000,
    hold_cost: float = 50.0,
    trader_fund: float = 0.0,
    trade_price: float = None,
):
    trader = Trader(
        stock_id="2330",
        trader_fund=trader_fund,
        hold_volume=hold_volume,
        hold_cost=hold_cost,
        fee=0.0,
        tax=0.0,
    )
    trader.trade_price = trade_price
    return trader


def test_stock_dividend_keeps_total_cost():
    """配股不是交易，總持有成本不變，只稀釋每股成本"""
    trader = make_trader(hold_volume=1000, hold_cost=50.0)
    # stock_div=1 元 --> 每 1000 股配 100 股
    compute_div_income(trader, cash_div=0.0, stock_div=1.0)

    assert trader.hold_volume == 1100
    assert trader.hold_cost == pytest.approx(50000 / 1100)
    assert trader.hold_volume * trader.hold_cost == pytest.approx(50000)


def test_stock_dividend_keeps_unrealized_profit_continuous():
    """除權當天股價被稀釋，未實現損益不應該跟著跳動"""
    trader = make_trader(hold_volume=1000, hold_cost=50.0, trade_price=55.0)
    unrealized_profit_before = (55.0 - trader.hold_cost) * trader.hold_volume

    # 除權參考價 55 / 1.1 = 50
    trader.trade_price = 50.0
    compute_div_income(trader, cash_div=0.0, stock_div=1.0)

    assert trader.UnrealizedProfit == pytest.approx(unrealized_profit_before)


def test_cash_dividend_does_not_change_holding():
    """現金股利不動持股與持有成本，全數進已實現損益與資金池"""
    trader = make_trader(hold_volume=1000, hold_cost=50.0, trader_fund=10000)
    compute_div_income(trader, cash_div=2.5, stock_div=0.0)

    assert trader.hold_volume == 1000
    assert trader.hold_cost == pytest.approx(50.0)
    assert trader.RealizedProfit == pytest.approx(2500)
    assert trader.trader_fund == pytest.approx(12500)


def test_stock_dividend_fraction_paid_by_cash():
    """畸零股按面額 10 元折現，不計入股數"""
    trader = make_trader(hold_volume=1005, hold_cost=50.0, trader_fund=0)
    # 1005 * 1 / 10 = 100.5 股 --> 100 股 + 0.5 股折現 5 元
    compute_div_income(trader, cash_div=0.0, stock_div=1.0)

    assert trader.hold_volume == 1105
    assert trader.RealizedProfit == pytest.approx(5.0)
    assert trader.trader_fund == pytest.approx(5.0)
    assert trader.hold_volume * trader.hold_cost == pytest.approx(1005 * 50.0)


def test_cash_and_stock_dividend_together():
    """同時配息配股：現金股利以除權前股數計算"""
    trader = make_trader(hold_volume=1000, hold_cost=50.0, trader_fund=0)
    compute_div_income(trader, cash_div=2.0, stock_div=1.0)

    assert trader.hold_volume == 1100
    assert trader.hold_volume * trader.hold_cost == pytest.approx(50000)
    assert trader.RealizedProfit == pytest.approx(2000)


def test_no_holding_does_not_raise():
    """空手時不應該除以零"""
    trader = make_trader(hold_volume=0, hold_cost=0.0)
    compute_div_income(trader, cash_div=2.0, stock_div=1.0)

    assert trader.hold_volume == 0
    assert trader.hold_cost == 0
    assert trader.RealizedProfit == 0
