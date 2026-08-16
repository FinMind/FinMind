import pytest

from FinMind.strategies.base import Trader


@pytest.mark.parametrize(
    "trader_fund, fee, expected_volume, expected_fund",
    [
        (10000, 0.001425, 0, 10000),
        (10020, 0.001425, 100, 0),
        (10099, 0.01, 0, 10099),
        (10100, 0.01, 100, 0),
    ],
)
def test_buy_requires_enough_fund_for_price_and_fee(
    trader_fund, fee, expected_volume, expected_fund
):
    trader = Trader(
        stock_id="2330",
        trader_fund=trader_fund,
        hold_volume=0,
        hold_cost=0,
        fee=fee,
        tax=0.003,
    )

    trader.buy(trade_price=100, trade_lots=0.1)

    assert trader.hold_volume == expected_volume
    assert trader.trader_fund == expected_fund
