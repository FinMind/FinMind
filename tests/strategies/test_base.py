import os

import pandas as pd
import pytest

from FinMind.schema.data import Dataset
from FinMind.schema.indicators import AddBuySellRule, Indicators
from FinMind.schema.rule import Rule
from FinMind.strategies.base import BackTest

FINMIND_API_TOKEN = os.environ.get("FINMIND_API_TOKEN", "")
FINMIND_USER = os.environ.get("FINMIND_USER", "")
FINMIND_PASSWORD = os.environ.get("FINMIND_PASSWORD", "")


@pytest.fixture(scope="module")
def backtest():
    backtest = BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        token=FINMIND_API_TOKEN,
    )
    return backtest


def test_add_indicators_formula(backtest):
    indicators_info = {"name": "DollarCostAveraging", "formula_value": 30}
    result = backtest._add_indicators_formula(
        indicator="ContinueHolding", indicators_info=indicators_info
    )
    assert result == {"name": "DollarCostAveraging", "buy_freq_day": 30}


def test_add_indicators_formula_list(backtest):
    indicators_info = {
        "name": "MAGoldenDeathCrossOver",
        "formula_value": [10, 30],
    }
    result = backtest._add_indicators_formula(
        indicator="MAGoldenDeathCrossOver", indicators_info=indicators_info
    )
    assert result == {
        "name": "MAGoldenDeathCrossOver",
        "ma_short_term_days": 10,
        "ma_long_term_days": 30,
    }


def test_add_indicators(backtest):
    # init
    if "DollarCostAveraging" in backtest.stock_price.columns:
        backtest.stock_price = backtest.stock_price.drop(
            "DollarCostAveraging", axis=1
        )
    backtest.add_indicators(
        indicators_info_list=[
            {
                "name": Indicators.ContinueHolding,
                "formula_value": 30,
            }
        ]
    )
    assert "DollarCostAveraging" in backtest.stock_price.columns


test_add_buy_rule_params = [
    [
        AddBuySellRule(
            indicators=Indicators.ContinueHolding,
            more_or_less_than=Rule.Equal,
            threshold=1,
        )
    ],
    [
        dict(
            indicators=Indicators.ContinueHolding,
            more_or_less_than=Rule.Equal,
            threshold=1,
        ),
    ],
    [
        dict(
            indicators="DollarCostAveraging",
            more_or_less_than="equal",
            threshold=1,
        ),
    ],
    [
        dict(
            indicators="DollarCostAveraging",
            more_or_less_than="=",
            threshold=1,
        ),
    ],
]


@pytest.mark.parametrize(
    "buy_rule_list",
    test_add_buy_rule_params,
)
def test_add_buy_rule(backtest, buy_rule_list):
    backtest.buy_rule_list = []
    backtest.add_buy_rule(buy_rule_list=buy_rule_list)
    backtest.buy_rule_list == [
        {
            "indicators": "DollarCostAveraging",
            "more_or_less_than": "=",
            "threshold": 1,
        }
    ]


test_add_sell_rule_params = [
    [
        AddBuySellRule(
            indicators=Indicators.ContinueHolding,
            more_or_less_than=Rule.Equal,
            threshold=1,
        )
    ],
    [
        dict(
            indicators=Indicators.ContinueHolding,
            more_or_less_than=Rule.Equal,
            threshold=1,
        ),
    ],
    [
        dict(
            indicators="DollarCostAveraging",
            more_or_less_than="equal",
            threshold=1,
        ),
    ],
    [
        dict(
            indicators="DollarCostAveraging",
            more_or_less_than="=",
            threshold=1,
        ),
    ],
]


@pytest.mark.parametrize(
    "sell_rule_list",
    test_add_sell_rule_params,
)
def test_add_sell_rule(backtest, sell_rule_list):
    backtest.sell_rule_list = []
    backtest.add_sell_rule(sell_rule_list=sell_rule_list)
    backtest.sell_rule_list == [
        {
            "indicators": "DollarCostAveraging",
            "more_or_less_than": "=",
            "threshold": 1,
        }
    ]


def test_create_sign(backtest):
    # create buy sign
    backtest.add_buy_rule(
        buy_rule_list=[
            {
                "indicators": "DollarCostAveraging",
                "more_or_less_than": "=",
                "threshold": 1,
            }
        ]
    )
    backtest._create_sign(
        sign_name=f"buy_signal_0",
        sign_value=1,
        indicators="DollarCostAveraging",
        more_or_less_than="=",
        threshold=1,
    )
    date_list = [
        "2018-01-02",
        "2018-02-21",
        "2018-04-09",
        "2018-05-22",
        "2018-07-04",
        "2018-08-15",
        "2018-09-27",
        "2018-11-09",
        "2018-12-21",
    ]
    # buy date
    assert list(
        backtest.stock_price.loc[
            backtest.stock_price.date.isin(date_list), "buy_signal_0"
        ].values
    ) == [1 for i in range(len(date_list))]
    # other day no buy
    assert (
        backtest.stock_price.loc[
            backtest.stock_price.date.isin(date_list) == False, "buy_signal_0"
        ].sum()
        == 0
    )


def test_create_buy_sign(backtest):
    backtest.add_buy_rule(
        buy_rule_list=[
            {
                "indicators": "DollarCostAveraging",
                "more_or_less_than": "=",
                "threshold": 1,
            }
        ]
    )
    backtest._create_buy_sign(
        sign_name=f"buy_signal_0",
        sign_value=1,
        indicators="DollarCostAveraging",
        more_or_less_than="=",
        threshold=1,
    )
    date_list = [
        "2018-01-02",
        "2018-02-21",
        "2018-04-09",
        "2018-05-22",
        "2018-07-04",
        "2018-08-15",
        "2018-09-27",
        "2018-11-09",
        "2018-12-21",
    ]
    # buy date
    assert list(
        backtest.stock_price.loc[
            backtest.stock_price.date.isin(date_list), "buy_signal_0"
        ].values
    ) == [1 for i in range(len(date_list))]
    # other day no buy
    assert (
        backtest.stock_price.loc[
            backtest.stock_price.date.isin(date_list) == False, "buy_signal_0"
        ].sum()
        == 0
    )


def test_create_buy_sign(backtest):
    backtest.add_indicators(
        indicators_info_list=[
            dict(name=Indicators.BIAS, formula_value=24),
        ]
    )
    backtest.add_buy_rule(
        buy_rule_list=[
            {
                "indicators": "BIAS",
                "more_or_less_than": "<",
                "threshold": -7,
            }
        ]
    )
    backtest.add_sell_rule(
        sell_rule_list=[
            {
                "indicators": "BIAS",
                "more_or_less_than": ">",
                "threshold": 8,
            }
        ]
    )
    backtest._create_trade_sign()
    date_list = [
        "2018-10-11",
        "2018-10-23",
        "2018-10-24",
        "2018-10-25",
        "2018-10-26",
        "2018-10-29",
        "2018-10-30",
    ]
    # buy date
    assert list(
        backtest.stock_price.loc[
            backtest.stock_price.date.isin(date_list), "signal"
        ].values
    ) == [1 for i in range(len(date_list))]
    # other day no buy
    assert (
        backtest.stock_price.loc[
            backtest.stock_price.date.isin(date_list) == False, "signal"
        ].sum()
        == 0
    )


def test_additional_dataset():
    backtest = BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        additional_dataset_list=[
            Dataset.TaiwanStockInstitutionalInvestorsBuySell
        ],
        token=FINMIND_API_TOKEN,
    )
    assert isinstance(
        backtest.TaiwanStockInstitutionalInvestorsBuySell, pd.DataFrame
    )
