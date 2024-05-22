import os

import pandas as pd
import pytest

from FinMind import strategies
from FinMind.data import DataLoader
from FinMind.schema.data import Dataset
from FinMind.schema.indicators import AddBuySellRule, Indicators, IndicatorsInfo
from FinMind.schema.rule import Rule

FINMIND_API_TOKEN = os.environ.get("FINMIND_API_TOKEN", "")
FINMIND_USER = os.environ.get("FINMIND_USER", "")
FINMIND_PASSWORD = os.environ.get("FINMIND_PASSWORD", "")


@pytest.fixture(scope="module")
def data_loader():
    data_loader = DataLoader()
    data_loader.login(FINMIND_USER, FINMIND_PASSWORD)
    return data_loader


def test_get_stock_price(data_loader):
    obj = strategies.BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        data_loader=data_loader,
        # strategy=ContinueHolding,
    )
    assert isinstance(obj.stock_price, pd.DataFrame)


def test_continue_holding(data_loader):
    trader_fund = 500000.0
    obj = strategies.BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=trader_fund,
        fee=0.001425,
        strategy=strategies.ContinueHolding,
        data_loader=data_loader,
    )
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 755
    assert int(obj.final_stats.MaxLoss) == -10127
    assert int(obj.final_stats.FinalProfit) == -6742

    assert obj.final_stats["MeanProfitPer"] == 0.15
    assert obj.final_stats["FinalProfitPer"] == -1.35
    assert obj.final_stats["MaxLossPer"] == -2.03

    assert obj.trade_detail.to_dict("r")[1] == {
        "stock_id": "0056",
        "date": "2018-01-03",
        "EverytimeProfit": -96.82749999999899,
        "RealizedProfit": 0.0,
        "UnrealizedProfit": -96.82749999999899,
        "board_lot": 1000,
        "hold_cost": 25.18583875,
        "hold_volume": 1000,
        "signal": 1,
        "trade_price": 25.15,
        "trader_fund": 474814.16125,
        "EverytimeTotalProfit": 474717.33375,
        "CashEarningsDistribution": 0.0,
        "StockEarningsDistribution": 0.0,
    }

    assert obj.compare_market_detail.to_dict("r")[-1] == {
        "date": "2018-12-28",
        "CumDailyReturn": -0.61003,
        "CumTaiExDailyReturn": -0.0963,
    }
    assert obj.compare_market_stats["AnnualTaiexReturnPer"] == -9.6
    assert obj.compare_market_stats["AnnualReturnPer"] == -1.35
    # 驗證 RealizedProfit 數據
    # 最終的資金，減掉已實現獲利，應該跟初始資金相同
    last_status = obj.trade_detail[-1:].to_dict("r")[0]
    assert (
        round(
            last_status["trader_fund"]
            + last_status["hold_volume"]
            * last_status["trade_price"]
            * (1 - 0.001 - 0.001425)
            - last_status["RealizedProfit"]
            - last_status["UnrealizedProfit"]
        )
        == trader_fund
    )


test_continue_holding_add_indicators_params = [
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
    test_continue_holding_add_indicators_params,
)
def test_continue_holding_add_indicators(buy_rule_list):
    trader_fund = 500000.0
    backtest = strategies.BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=trader_fund,
        fee=0.001425,
        token=FINMIND_API_TOKEN,
    )
    backtest.add_indicators(
        indicators_info_list=[
            IndicatorsInfo(name=Indicators.ContinueHolding, formula_value=30)
        ]
    )
    backtest.add_buy_rule(buy_rule_list=buy_rule_list)
    backtest.simulate()

    assert int(backtest.final_stats.MeanProfit) == 755
    assert int(backtest.final_stats.MaxLoss) == -10127
    assert int(backtest.final_stats.FinalProfit) == -6742

    assert backtest.final_stats["MeanProfitPer"] == 0.15
    assert backtest.final_stats["FinalProfitPer"] == -1.35
    assert backtest.final_stats["MaxLossPer"] == -2.03

    assert backtest.trade_detail.to_dict("r")[1] == {
        "stock_id": "0056",
        "date": "2018-01-03",
        "EverytimeProfit": -96.82749999999899,
        "RealizedProfit": 0.0,
        "UnrealizedProfit": -96.82749999999899,
        "board_lot": 1000,
        "hold_cost": 25.18583875,
        "hold_volume": 1000,
        "signal": 1,
        "trade_price": 25.15,
        "trader_fund": 474814.16125,
        "EverytimeTotalProfit": 474717.33375,
        "CashEarningsDistribution": 0.0,
        "StockEarningsDistribution": 0.0,
    }

    assert backtest.compare_market_detail.to_dict("r")[-1] == {
        "date": "2018-12-28",
        "CumDailyReturn": -0.61003,
        "CumTaiExDailyReturn": -0.0963,
    }
    assert backtest.compare_market_stats["AnnualTaiexReturnPer"] == -9.6
    assert backtest.compare_market_stats["AnnualReturnPer"] == -1.35
    # 驗證 RealizedProfit 數據
    # 最終的資金，減掉已實現獲利，應該跟初始資金相同
    last_status = backtest.trade_detail[-1:].to_dict("r")[0]
    assert (
        round(
            last_status["trader_fund"]
            + last_status["hold_volume"]
            * last_status["trade_price"]
            * (1 - 0.001 - 0.001425)
            - last_status["RealizedProfit"]
            - last_status["UnrealizedProfit"]
        )
        == trader_fund
    )


def test_continue_holding_add_strategy(data_loader):
    trader_fund = 500000.0
    obj = strategies.BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=trader_fund,
        fee=0.001425,
        data_loader=data_loader,
    )
    obj.add_strategy(strategies.ContinueHolding)
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 755
    assert int(obj.final_stats.MaxLoss) == -10127
    assert int(obj.final_stats.FinalProfit) == -6742

    assert obj.final_stats["MeanProfitPer"] == 0.15
    assert obj.final_stats["FinalProfitPer"] == -1.35
    assert obj.final_stats["MaxLossPer"] == -2.03

    assert obj.trade_detail.to_dict("r")[1] == {
        "stock_id": "0056",
        "date": "2018-01-03",
        "EverytimeProfit": -96.82749999999899,
        "RealizedProfit": 0.0,
        "UnrealizedProfit": -96.82749999999899,
        "board_lot": 1000,
        "hold_cost": 25.18583875,
        "hold_volume": 1000,
        "signal": 1,
        "trade_price": 25.15,
        "trader_fund": 474814.16125,
        "EverytimeTotalProfit": 474717.33375,
        "CashEarningsDistribution": 0.0,
        "StockEarningsDistribution": 0.0,
    }
    # 驗證 RealizedProfit 數據
    # 最終的資金，減掉已實現獲利，應該跟初始資金相同
    last_status = obj.trade_detail[-1:].to_dict("r")[0]
    assert (
        round(
            last_status["trader_fund"]
            + last_status["hold_volume"]
            * last_status["trade_price"]
            * (1 - 0.001 - 0.001425)
            - last_status["RealizedProfit"]
            - last_status["UnrealizedProfit"]
        )
        == trader_fund
    )


test_backtest_add_indicators_bias_params = [
    (
        [
            AddBuySellRule(
                indicators=Indicators.BIAS,
                more_or_less_than=Rule.LessThan,
                threshold=-7,
            )
        ],
        [
            AddBuySellRule(
                indicators=Indicators.BIAS,
                more_or_less_than=Rule.MoreThan,
                threshold=8,
            )
        ],
    ),
    (
        [
            dict(
                indicators=Indicators.BIAS,
                more_or_less_than=Rule.LessThan,
                threshold=-7,
            ),
        ],
        [
            dict(
                indicators=Indicators.BIAS,
                more_or_less_than=Rule.MoreThan,
                threshold=8,
            ),
        ],
    ),
    (
        [
            dict(
                indicators="BIAS",
                more_or_less_than="less_than",
                threshold=-7,
            ),
        ],
        [
            dict(
                indicators="BIAS",
                more_or_less_than="more_than",
                threshold=8,
            ),
        ],
    ),
    (
        [
            dict(
                indicators="BIAS",
                more_or_less_than="<",
                threshold=-7,
            ),
        ],
        [
            dict(
                indicators="BIAS",
                more_or_less_than=">",
                threshold=8,
            ),
        ],
    ),
]


@pytest.mark.parametrize(
    "buy_rule_list, sell_rule_list",
    test_backtest_add_indicators_bias_params,
)
def test_backtest_add_indicators_bias(buy_rule_list, sell_rule_list):
    trader_fund = 500000.0
    backtest = strategies.BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=trader_fund,
        fee=0.001425,
        token=FINMIND_API_TOKEN,
    )
    backtest.add_indicators(
        indicators_info_list=[
            IndicatorsInfo(name=Indicators.BIAS, formula_value=24)
        ]
    )
    backtest.add_buy_rule(buy_rule_list=buy_rule_list)
    backtest.add_sell_rule(sell_rule_list=sell_rule_list)
    backtest.simulate()

    assert int(backtest.final_stats.MeanProfit) == 599
    assert int(backtest.final_stats.MaxLoss) == -2313
    assert int(backtest.final_stats.FinalProfit) == 1395

    assert backtest.final_stats["MeanProfitPer"] == 0.12
    assert backtest.final_stats["FinalProfitPer"] == 0.28
    assert backtest.final_stats["MaxLossPer"] == -0.46

    assert backtest.trade_detail.to_dict("r")[1] == {
        "stock_id": "0056",
        "date": "2018-01-03",
        "EverytimeProfit": 0.0,
        "RealizedProfit": 0.0,
        "UnrealizedProfit": 0.0,
        "board_lot": 1000,
        "hold_cost": 0.0,
        "hold_volume": 0,
        "signal": 0,
        "trade_price": 25.15,
        "trader_fund": 500000.0,
        "EverytimeTotalProfit": 500000.0,
        "CashEarningsDistribution": 0.0,
        "StockEarningsDistribution": 0.0,
    }

    assert backtest.compare_market_detail.to_dict("r")[-1] == {
        "date": "2018-12-28",
        "CumDailyReturn": -0.39843,
        "CumTaiExDailyReturn": -0.0963,
    }

    assert backtest.compare_market_stats["AnnualTaiexReturnPer"] == -9.6
    assert backtest.compare_market_stats["AnnualReturnPer"] == 0.28
    # 驗證 RealizedProfit 數據
    # 最終的資金，減掉已實現獲利，應該跟初始資金相同
    last_status = backtest.trade_detail[-1:].to_dict("r")[0]
    assert (
        round(
            last_status["trader_fund"]
            + last_status["hold_volume"]
            * last_status["trade_price"]
            * (1 - 0.001 - 0.001425)
            - last_status["RealizedProfit"]
            - last_status["UnrealizedProfit"]
        )
        == trader_fund
    )


def test_bias_add_strategy(data_loader):
    trader_fund = 500000.0
    obj = strategies.BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=trader_fund,
        fee=0.001425,
        data_loader=data_loader,
    )
    obj.add_strategy(strategies.Bias)
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 599
    assert int(obj.final_stats.MaxLoss) == -2313
    assert int(obj.final_stats.FinalProfit) == 1395

    assert obj.final_stats["MeanProfitPer"] == 0.12
    assert obj.final_stats["FinalProfitPer"] == 0.28
    assert obj.final_stats["MaxLossPer"] == -0.46

    assert obj.trade_detail.to_dict("r")[1] == {
        "stock_id": "0056",
        "date": "2018-01-03",
        "EverytimeProfit": 0.0,
        "RealizedProfit": 0.0,
        "UnrealizedProfit": 0.0,
        "board_lot": 1000,
        "hold_cost": 0.0,
        "hold_volume": 0,
        "signal": 0,
        "trade_price": 25.15,
        "trader_fund": 500000.0,
        "EverytimeTotalProfit": 500000.0,
        "CashEarningsDistribution": 0.0,
        "StockEarningsDistribution": 0.0,
    }
    # 驗證 RealizedProfit 數據
    # 最終的資金，減掉已實現獲利，應該跟初始資金相同
    last_status = obj.trade_detail[-1:].to_dict("r")[0]
    assert (
        round(
            last_status["trader_fund"]
            + last_status["hold_volume"]
            * last_status["trade_price"]
            * (1 - 0.001 - 0.001425)
            - last_status["RealizedProfit"]
            - last_status["UnrealizedProfit"]
        )
        == trader_fund
    )


def test_naive_kd(data_loader):
    trader_fund = 500000.0
    obj = strategies.BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=trader_fund,
        fee=0.001425,
        strategy=strategies.NaiveKd,
        data_loader=data_loader,
    )
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 3657
    assert int(obj.final_stats.MaxLoss) == -3319
    assert int(obj.final_stats.FinalProfit) == 6333

    assert obj.final_stats["MeanProfitPer"] == 0.73
    assert obj.final_stats["FinalProfitPer"] == 1.27
    assert obj.final_stats["MaxLossPer"] == -0.66

    # 驗證 RealizedProfit 數據
    # 最終的資金，減掉已實現獲利，應該跟初始資金相同
    last_status = obj.trade_detail[-1:].to_dict("r")[0]
    assert (
        round(
            last_status["trader_fund"]
            + last_status["hold_volume"]
            * last_status["trade_price"]
            * (1 - 0.001 - 0.001425)
            - last_status["RealizedProfit"]
            - last_status["UnrealizedProfit"]
        )
        == trader_fund
    )


def test_naive_kd_add_strategy(data_loader):
    trader_fund = 500000.0
    obj = strategies.BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=trader_fund,
        fee=0.001425,
        # strategy=strategies.NaiveKd,
        data_loader=data_loader,
    )
    obj.add_strategy(strategies.NaiveKd)
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 3657
    assert int(obj.final_stats.MaxLoss) == -3319
    assert int(obj.final_stats.FinalProfit) == 6333

    assert obj.final_stats["MeanProfitPer"] == 0.73
    assert obj.final_stats["FinalProfitPer"] == 1.27
    assert obj.final_stats["MaxLossPer"] == -0.66
    # 驗證 RealizedProfit 數據
    # 最終的資金，減掉已實現獲利，應該跟初始資金相同
    last_status = obj.trade_detail[-1:].to_dict("r")[0]
    assert (
        round(
            last_status["trader_fund"]
            + last_status["hold_volume"]
            * last_status["trade_price"]
            * (1 - 0.001 - 0.001425)
            - last_status["RealizedProfit"]
            - last_status["UnrealizedProfit"]
        )
        == trader_fund
    )


test_kd_add_strategy_params = [
    (
        [
            AddBuySellRule(
                indicators=Indicators.KD,
                more_or_less_than=Rule.LessThan,
                threshold=20,
            )
        ],
        [
            AddBuySellRule(
                indicators=Indicators.KD,
                more_or_less_than=Rule.MoreThan,
                threshold=80,
            )
        ],
        [IndicatorsInfo(name=Indicators.KD, formula_value=9)],
    ),
    (
        [
            AddBuySellRule(
                indicators=Indicators.KD,
                more_or_less_than="<",
                threshold=20,
            )
        ],
        [
            AddBuySellRule(
                indicators=Indicators.KD,
                more_or_less_than=">",
                threshold=80,
            )
        ],
        [IndicatorsInfo(name=Indicators.KD, formula_value=9)],
    ),
    (
        [
            dict(
                indicators=Indicators.KD,
                more_or_less_than=Rule.LessThan,
                threshold=20,
            )
        ],
        [
            dict(
                indicators=Indicators.KD,
                more_or_less_than=Rule.MoreThan,
                threshold=80,
            ),
        ],
        [{"name": "KD", "formula_value": 9}],
    ),
    (
        [dict(indicators="K", more_or_less_than="less_than", threshold=20)],
        [
            dict(indicators="K", more_or_less_than="more_than", threshold=80),
        ],
        [{"name": "KD", "formula_value": 9}],
    ),
    (
        [dict(indicators="K", more_or_less_than="<", threshold=20)],
        [
            dict(indicators="K", more_or_less_than=">", threshold=80),
        ],
        [{"name": "KD", "formula_value": 9}],
    ),
]


@pytest.mark.parametrize(
    "buy_rule_list, sell_rule_list, indicators_info_list",
    test_kd_add_strategy_params,
)
def test_kd_add_strategy(buy_rule_list, sell_rule_list, indicators_info_list):
    backtest = strategies.BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        token=FINMIND_API_TOKEN,
    )
    backtest.add_indicators(indicators_info_list=indicators_info_list)
    backtest.add_buy_rule(buy_rule_list=buy_rule_list)
    backtest.add_sell_rule(sell_rule_list=sell_rule_list)
    backtest.simulate()

    assert int(backtest.final_stats.MeanProfit) == 2356
    assert int(backtest.final_stats.MaxLoss) == -1425
    assert int(backtest.final_stats.FinalProfit) == 6196

    assert backtest.final_stats["MeanProfitPer"] == 0.47
    assert backtest.final_stats["FinalProfitPer"] == 1.24
    assert backtest.final_stats["MaxLossPer"] == -0.29


def test_kd_crossover(data_loader):
    trader_fund = 500000.0
    obj = strategies.BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=trader_fund,
        fee=0.001425,
        strategy=strategies.KdCrossOver,
        data_loader=data_loader,
    )
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 55
    assert int(obj.final_stats.MaxLoss) == -1223
    assert int(obj.final_stats.FinalProfit) == -516

    assert obj.final_stats["MeanProfitPer"] == 0.01
    assert obj.final_stats["FinalProfitPer"] == -0.1
    assert obj.final_stats["MaxLossPer"] == -0.24
    # 驗證 RealizedProfit 數據
    # 最終的資金，減掉已實現獲利，應該跟初始資金相同
    last_status = obj.trade_detail[-1:].to_dict("r")[0]
    assert (
        round(
            last_status["trader_fund"]
            + last_status["hold_volume"]
            * last_status["trade_price"]
            * (1 - 0.001 - 0.001425)
            - last_status["RealizedProfit"]
            - last_status["UnrealizedProfit"]
        )
        == trader_fund
    )


def test_kd_crossover_add_strategy(data_loader):
    trader_fund = 500000.0
    obj = strategies.BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=trader_fund,
        fee=0.001425,
        # strategy=strategies.KdCrossOver,
        data_loader=data_loader,
    )
    obj.add_strategy(strategies.KdCrossOver)
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 55
    assert int(obj.final_stats.MaxLoss) == -1223
    assert int(obj.final_stats.FinalProfit) == -516

    assert obj.final_stats["MeanProfitPer"] == 0.01
    assert obj.final_stats["FinalProfitPer"] == -0.1
    assert obj.final_stats["MaxLossPer"] == -0.24
    # 驗證 RealizedProfit 數據
    # 最終的資金，減掉已實現獲利，應該跟初始資金相同
    last_status = obj.trade_detail[-1:].to_dict("r")[0]
    assert (
        round(
            last_status["trader_fund"]
            + last_status["hold_volume"]
            * last_status["trade_price"]
            * (1 - 0.001 - 0.001425)
            - last_status["RealizedProfit"]
            - last_status["UnrealizedProfit"]
        )
        == trader_fund
    )


def test_kd_crossover_add_indicators():
    trader_fund = 500000.0
    backtest = strategies.BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=trader_fund,
        fee=0.001425,
        token=FINMIND_API_TOKEN,
    )
    backtest.add_indicators(
        indicators_info_list=[
            IndicatorsInfo(
                name=Indicators.KDGoldenDeathCrossOver, formula_value=9
            )
        ]
    )
    backtest.add_buy_rule(
        buy_rule_list=[
            AddBuySellRule(
                indicators=Indicators.KDGoldenDeathCrossOver,
                more_or_less_than="=",
                threshold=1,
            )
        ]
    )
    backtest.add_sell_rule(
        sell_rule_list=[
            AddBuySellRule(
                indicators=Indicators.KDGoldenDeathCrossOver,
                more_or_less_than="=",
                threshold=-1,
            )
        ]
    )
    backtest.simulate()

    assert int(backtest.final_stats.MeanProfit) == 55
    assert int(backtest.final_stats.MaxLoss) == -1223
    assert int(backtest.final_stats.FinalProfit) == -516

    assert backtest.final_stats["MeanProfitPer"] == 0.01
    assert backtest.final_stats["FinalProfitPer"] == -0.1
    assert backtest.final_stats["MaxLossPer"] == -0.24
    # 驗證 RealizedProfit 數據
    # 最終的資金，減掉已實現獲利，應該跟初始資金相同
    last_status = backtest.trade_detail[-1:].to_dict("r")[0]
    assert (
        round(
            last_status["trader_fund"]
            + last_status["hold_volume"]
            * last_status["trade_price"]
            * (1 - 0.001 - 0.001425)
            - last_status["RealizedProfit"]
            - last_status["UnrealizedProfit"]
        )
        == trader_fund
    )


def test_institutional_investors_follower(data_loader):
    trader_fund = 500000.0
    obj = strategies.BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=trader_fund,
        fee=0.001425,
        strategy=strategies.InstitutionalInvestorsFollower,
        token=FINMIND_API_TOKEN,
    )
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 1911
    assert int(obj.final_stats.MaxLoss) == -16338
    assert int(obj.final_stats.FinalProfit) == -9600

    assert obj.final_stats["MeanProfitPer"] == 0.38
    assert obj.final_stats["FinalProfitPer"] == -1.92
    assert obj.final_stats["MaxLossPer"] == -3.27
    # 驗證 RealizedProfit 數據
    # 最終的資金，減掉已實現獲利，應該跟初始資金相同
    last_status = obj.trade_detail[-1:].to_dict("r")[0]
    assert (
        round(
            last_status["trader_fund"]
            + last_status["hold_volume"]
            * last_status["trade_price"]
            * (1 - 0.001 - 0.001425)
            - last_status["RealizedProfit"]
            - last_status["UnrealizedProfit"]
        )
        == trader_fund
    )


test_institutional_investors_follower_add_indicators_params = [
    (
        [
            AddBuySellRule(
                indicators=Indicators.InstitutionalInvestorsFollower,
                more_or_less_than=Rule.Equal,
                threshold=-1,
            )
        ],
        [
            AddBuySellRule(
                indicators=Indicators.InstitutionalInvestorsFollower,
                more_or_less_than=Rule.Equal,
                threshold=1,
            )
        ],
    ),
    (
        [
            dict(
                indicators=Indicators.InstitutionalInvestorsFollower,
                more_or_less_than=Rule.Equal,
                threshold=-1,
            ),
        ],
        [
            dict(
                indicators=Indicators.InstitutionalInvestorsFollower,
                more_or_less_than=Rule.Equal,
                threshold=1,
            ),
        ],
    ),
    (
        [
            dict(
                indicators="InstitutionalInvestorsFollower",
                more_or_less_than="equal",
                threshold=-1,
            ),
        ],
        [
            dict(
                indicators="InstitutionalInvestorsFollower",
                more_or_less_than="equal",
                threshold=1,
            ),
        ],
    ),
    (
        [
            dict(
                indicators="InstitutionalInvestorsFollower",
                more_or_less_than="=",
                threshold=-1,
            ),
        ],
        [
            dict(
                indicators="InstitutionalInvestorsFollower",
                more_or_less_than="=",
                threshold=1,
            ),
        ],
    ),
]


@pytest.mark.parametrize(
    "buy_rule_list, sell_rule_list",
    test_institutional_investors_follower_add_indicators_params,
)
def test_institutional_investors_follower_add_indicators(
    buy_rule_list, sell_rule_list
):
    trader_fund = 500000.0
    backtest = strategies.BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=trader_fund,
        fee=0.001425,
        token=FINMIND_API_TOKEN,
    )
    backtest.add_indicators(
        indicators_info_list=[
            IndicatorsInfo(name=Indicators.InstitutionalInvestorsFollower)
        ]
    )
    backtest.add_buy_rule(buy_rule_list=buy_rule_list)
    backtest.add_sell_rule(sell_rule_list=sell_rule_list)
    backtest.simulate()

    assert int(backtest.final_stats.MeanProfit) == 1911
    assert int(backtest.final_stats.MaxLoss) == -16338
    assert int(backtest.final_stats.FinalProfit) == -9600

    assert backtest.final_stats["MeanProfitPer"] == 0.38
    assert backtest.final_stats["FinalProfitPer"] == -1.92
    assert backtest.final_stats["MaxLossPer"] == -3.27
    # 驗證 RealizedProfit 數據
    # 最終的資金，減掉已實現獲利，應該跟初始資金相同
    last_status = backtest.trade_detail[-1:].to_dict("r")[0]
    assert (
        round(
            last_status["trader_fund"]
            + last_status["hold_volume"]
            * last_status["trade_price"]
            * (1 - 0.001 - 0.001425)
            - last_status["RealizedProfit"]
            - last_status["UnrealizedProfit"]
        )
        == trader_fund
    )


def test_institutional_investors_follower_add_strategy(data_loader):
    trader_fund = 500000.0
    obj = strategies.BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=trader_fund,
        fee=0.001425,
        data_loader=data_loader,
    )
    obj.add_strategy(strategies.InstitutionalInvestorsFollower)
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 1911
    assert int(obj.final_stats.MaxLoss) == -16338
    assert int(obj.final_stats.FinalProfit) == -9600

    assert obj.final_stats["MeanProfitPer"] == 0.38
    assert obj.final_stats["FinalProfitPer"] == -1.92
    assert obj.final_stats["MaxLossPer"] == -3.27
    # 驗證 RealizedProfit 數據
    # 最終的資金，減掉已實現獲利，應該跟初始資金相同
    last_status = obj.trade_detail[-1:].to_dict("r")[0]
    assert (
        round(
            last_status["trader_fund"]
            + last_status["hold_volume"]
            * last_status["trade_price"]
            * (1 - 0.001 - 0.001425)
            - last_status["RealizedProfit"]
            - last_status["UnrealizedProfit"]
        )
        == trader_fund
    )


def test_short_sale_margin_purchase_ratio(data_loader):
    trader_fund = 500000.0
    obj = strategies.BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=trader_fund,
        fee=0.001425,
        strategy=strategies.ShortSaleMarginPurchaseRatio,
        data_loader=data_loader,
    )
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 7207
    assert int(obj.final_stats.MaxLoss) == -17589
    assert int(obj.final_stats.FinalProfit) == -6017

    assert obj.final_stats["MeanProfitPer"] == 1.44
    assert obj.final_stats["FinalProfitPer"] == -1.2
    assert obj.final_stats["MaxLossPer"] == -3.52
    # 驗證 RealizedProfit 數據
    # 最終的資金，減掉已實現獲利，應該跟初始資金相同
    last_status = obj.trade_detail[-1:].to_dict("r")[0]
    assert (
        round(
            last_status["trader_fund"]
            + last_status["hold_volume"]
            * last_status["trade_price"]
            * (1 - 0.001 - 0.001425)
            - last_status["RealizedProfit"]
            - last_status["UnrealizedProfit"]
        )
        == trader_fund
    )


def test_short_sale_margin_purchase_ratio_add_strategy(data_loader):
    trader_fund = 500000.0
    obj = strategies.BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=trader_fund,
        fee=0.001425,
        # strategy=strategies.ShortSaleMarginPurchaseRatio,
        data_loader=data_loader,
    )
    obj.add_strategy(strategies.ShortSaleMarginPurchaseRatio)
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 7207
    assert int(obj.final_stats.MaxLoss) == -17589
    assert int(obj.final_stats.FinalProfit) == -6017

    assert obj.final_stats["MeanProfitPer"] == 1.44
    assert obj.final_stats["FinalProfitPer"] == -1.2
    assert obj.final_stats["MaxLossPer"] == -3.52
    # 驗證 RealizedProfit 數據
    # 最終的資金，減掉已實現獲利，應該跟初始資金相同
    last_status = obj.trade_detail[-1:].to_dict("r")[0]
    assert (
        round(
            last_status["trader_fund"]
            + last_status["hold_volume"]
            * last_status["trade_price"]
            * (1 - 0.001 - 0.001425)
            - last_status["RealizedProfit"]
            - last_status["UnrealizedProfit"]
        )
        == trader_fund
    )


def test_short_sale_margin_purchase_ratio_add_indicator(data_loader):
    trader_fund = 500000.0
    backtest = strategies.BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=trader_fund,
        fee=0.001425,
        token=FINMIND_API_TOKEN,
    )
    backtest.add_indicators(
        indicators_info_list=[
            IndicatorsInfo(name=Indicators.InstitutionalInvestorsOverBuy),
            IndicatorsInfo(name=Indicators.ShortSaleMarginPurchaseRatio),
        ]
    )
    backtest.add_buy_rule(
        buy_rule_list=[
            AddBuySellRule(
                # 賣超
                indicators=Indicators.InstitutionalInvestorsOverBuy,
                more_or_less_than="<",
                threshold=0,
            ),
            AddBuySellRule(
                # 券資比<0.3
                indicators=Indicators.ShortSaleMarginPurchaseRatio,
                more_or_less_than="<",
                threshold=0.3,
            ),
        ]
    )
    backtest.add_sell_rule(
        sell_rule_list=[
            AddBuySellRule(
                indicators=Indicators.InstitutionalInvestorsOverBuy,
                more_or_less_than=">",
                threshold=0,
            ),
            AddBuySellRule(
                # 券資比>0.3
                indicators=Indicators.ShortSaleMarginPurchaseRatio,
                more_or_less_than=">",
                threshold=0.3,
            ),
        ]
    )
    backtest.simulate()
    assert int(backtest.final_stats.MeanProfit) == 7207
    assert int(backtest.final_stats.MaxLoss) == -17589
    assert int(backtest.final_stats.FinalProfit) == -6017

    assert backtest.final_stats["MeanProfitPer"] == 1.44
    assert backtest.final_stats["FinalProfitPer"] == -1.2
    assert backtest.final_stats["MaxLossPer"] == -3.52
    # 驗證 RealizedProfit 數據
    # 最終的資金，減掉已實現獲利，應該跟初始資金相同
    last_status = backtest.trade_detail[-1:].to_dict("r")[0]
    assert (
        round(
            last_status["trader_fund"]
            + last_status["hold_volume"]
            * last_status["trade_price"]
            * (1 - 0.001 - 0.001425)
            - last_status["RealizedProfit"]
            - last_status["UnrealizedProfit"]
        )
        == trader_fund
    )


def test_macd_crossover(data_loader):
    trader_fund = 500000.0
    obj = strategies.BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=trader_fund,
        fee=0.001425,
        strategy=strategies.MacdCrossOver,
        data_loader=data_loader,
    )
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 1054
    assert int(obj.final_stats.MaxLoss) == -397
    assert int(obj.final_stats.FinalProfit) == 1782

    assert obj.final_stats["MeanProfitPer"] == 0.21
    assert obj.final_stats["FinalProfitPer"] == 0.36
    assert obj.final_stats["MaxLossPer"] == -0.08
    # 驗證 RealizedProfit 數據
    # 最終的資金，減掉已實現獲利，應該跟初始資金相同
    last_status = obj.trade_detail[-1:].to_dict("r")[0]
    assert (
        round(
            last_status["trader_fund"]
            + last_status["hold_volume"]
            * last_status["trade_price"]
            * (1 - 0.001 - 0.001425)
            - last_status["RealizedProfit"]
            - last_status["UnrealizedProfit"]
        )
        == trader_fund
    )


def test_macd_crossover_add_strategy(data_loader):
    trader_fund = 500000.0
    obj = strategies.BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=trader_fund,
        fee=0.001425,
        # strategy=strategies.MacdCrossOver,
        data_loader=data_loader,
    )
    obj.add_strategy(strategies.MacdCrossOver)
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 1054
    assert int(obj.final_stats.MaxLoss) == -397
    assert int(obj.final_stats.FinalProfit) == 1782

    assert obj.final_stats["MeanProfitPer"] == 0.21
    assert obj.final_stats["FinalProfitPer"] == 0.36
    assert obj.final_stats["MaxLossPer"] == -0.08
    # 驗證 RealizedProfit 數據
    # 最終的資金，減掉已實現獲利，應該跟初始資金相同
    last_status = obj.trade_detail[-1:].to_dict("r")[0]
    assert (
        round(
            last_status["trader_fund"]
            + last_status["hold_volume"]
            * last_status["trade_price"]
            * (1 - 0.001 - 0.001425)
            - last_status["RealizedProfit"]
            - last_status["UnrealizedProfit"]
        )
        == trader_fund
    )


def test_ma_crossover(data_loader):
    obj = strategies.BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        strategy=strategies.MaCrossOver,
        data_loader=data_loader,
    )
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == -381
    assert int(obj.final_stats.MaxLoss) == -1230
    assert int(obj.final_stats.FinalProfit) == -1230

    assert obj.final_stats["MeanProfitPer"] == -0.08
    assert obj.final_stats["FinalProfitPer"] == -0.25
    assert obj.final_stats["MaxLossPer"] == -0.25


def test_ma_crossover_add_strategy(data_loader):
    obj = strategies.BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        # strategy=strategies.MaCrossOver,
        data_loader=data_loader,
    )
    obj.add_strategy(strategies.MaCrossOver)
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == -381
    assert int(obj.final_stats.MaxLoss) == -1230
    assert int(obj.final_stats.FinalProfit) == -1230

    assert obj.final_stats["MeanProfitPer"] == -0.08
    assert obj.final_stats["FinalProfitPer"] == -0.25
    assert obj.final_stats["MaxLossPer"] == -0.25


def test_ma_crossover_add_indicators(data_loader):
    backtest = strategies.BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        token=FINMIND_API_TOKEN,
    )
    backtest.add_indicators(
        indicators_info_list=[
            IndicatorsInfo(
                name=Indicators.MAGoldenDeathCrossOver, formula_value=[10, 30]
            )
        ]
    )
    backtest.add_buy_rule(
        buy_rule_list=[
            AddBuySellRule(
                indicators=Indicators.MAGoldenDeathCrossOver,
                more_or_less_than="=",
                threshold=1,
            )
        ]
    )
    backtest.add_sell_rule(
        sell_rule_list=[
            AddBuySellRule(
                indicators=Indicators.MAGoldenDeathCrossOver,
                more_or_less_than="=",
                threshold=-1,
            )
        ]
    )
    backtest.simulate()

    assert int(backtest.final_stats.MeanProfit) == -381
    assert int(backtest.final_stats.MaxLoss) == -1230
    assert int(backtest.final_stats.FinalProfit) == -1230

    assert backtest.final_stats["MeanProfitPer"] == -0.08
    assert backtest.final_stats["FinalProfitPer"] == -0.25
    assert backtest.final_stats["MaxLossPer"] == -0.25


def test_max_min_period_bias(data_loader):
    obj = strategies.BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        strategy=strategies.MaxMinPeriodBias,
        data_loader=data_loader,
    )
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 0
    assert int(obj.final_stats.MaxLoss) == 0
    assert int(obj.final_stats.FinalProfit) == 0

    assert obj.final_stats["MeanProfitPer"] == 0
    assert obj.final_stats["FinalProfitPer"] == 0
    assert obj.final_stats["MaxLossPer"] == 0


def test_max_min_period_bias_add_strategy(data_loader):
    obj = strategies.BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        # strategy=strategies.MaxMinPeriodBias,
        data_loader=data_loader,
    )
    obj.add_strategy(strategies.MaxMinPeriodBias)
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 0
    assert int(obj.final_stats.MaxLoss) == 0
    assert int(obj.final_stats.FinalProfit) == 0

    assert obj.final_stats["MeanProfitPer"] == 0
    assert obj.final_stats["FinalProfitPer"] == 0
    assert obj.final_stats["MaxLossPer"] == 0


def test__compute_div_income(data_loader):
    trader_fund = 10000000
    backtest = strategies.BackTest(
        stock_id="2330",
        start_date="2021-05-22",
        end_date="2023-06-22",
        trader_fund=trader_fund,
        fee=0.001425,
        data_loader=data_loader,
    )
    backtest.add_indicators(
        indicators_info_list=[
            IndicatorsInfo(name=Indicators.KD, formula_value=9)
        ]
    )
    backtest.add_buy_rule(
        buy_rule_list=[
            AddBuySellRule(
                indicators=Indicators.KD,
                more_or_less_than=Rule.LessThan,
                threshold=20,
            )
        ]
    )
    backtest.add_sell_rule(
        sell_rule_list=[
            AddBuySellRule(
                indicators=Indicators.KD,
                more_or_less_than=Rule.MoreThan,
                threshold=30,
            )
        ]
    )
    backtest.simulate()
    # 驗證 RealizedProfit 數據
    # 最終的資金，減掉已實現獲利，應該跟初始資金相同
    assert (
        round(
            backtest.trade_detail["trader_fund"].values[-1]
            - backtest.trade_detail["RealizedProfit"].values[-1]
        )
        == trader_fund
    )
