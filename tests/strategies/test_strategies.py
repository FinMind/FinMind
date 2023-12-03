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
    obj = strategies.BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        strategy=strategies.ContinueHolding,
        data_loader=data_loader,
    )
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 2810
    assert int(obj.final_stats.MaxLoss) == -9663
    assert int(obj.final_stats.FinalProfit) == 3407

    assert obj.final_stats["MeanProfitPer"] == 0.56
    assert obj.final_stats["FinalProfitPer"] == 0.68
    assert obj.final_stats["MaxLossPer"] == -1.93

    assert obj.trade_detail.to_dict("r")[1] == {
        "stock_id": "0056",
        "date": "2018-01-03",
        "EverytimeProfit": -96.83,
        "RealizedProfit": 0.0,
        "UnrealizedProfit": -96.83,
        "board_lot": 1000,
        "hold_cost": 25.18583875,
        "hold_volume": 1000,
        "signal": 1,
        "trade_price": 25.15,
        "trader_fund": 474814.16125,
        "EverytimeTotalProfit": 474717.33125,
        "CashEarningsDistribution": 0.0,
        "StockEarningsDistribution": 0.0,
    }

    assert obj.compare_market_detail.to_dict("r")[-1] == {
        "CumDailyReturn": -0.61003,
        "CumTaiExDailyReturn": -0.0963,
        "date": "2018-12-28",
    }
    assert obj.compare_market_stats["AnnualTaiexReturnPer"] == -9.6
    assert obj.compare_market_stats["AnnualReturnPer"] == 0.68


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
            IndicatorsInfo(name=Indicators.ContinueHolding, formula_value=30)
        ]
    )
    backtest.add_buy_rule(buy_rule_list=buy_rule_list)
    backtest.simulate()

    assert int(backtest.final_stats.MeanProfit) == 2810
    assert int(backtest.final_stats.MaxLoss) == -9663
    assert int(backtest.final_stats.FinalProfit) == 3407

    assert backtest.final_stats["MeanProfitPer"] == 0.56
    assert backtest.final_stats["FinalProfitPer"] == 0.68
    assert backtest.final_stats["MaxLossPer"] == -1.93

    assert backtest.trade_detail.to_dict("r")[1] == {
        "stock_id": "0056",
        "date": "2018-01-03",
        "EverytimeProfit": -96.83,
        "RealizedProfit": 0.0,
        "UnrealizedProfit": -96.83,
        "board_lot": 1000,
        "hold_cost": 25.18583875,
        "hold_volume": 1000,
        "signal": 1,
        "trade_price": 25.15,
        "trader_fund": 474814.16125,
        "EverytimeTotalProfit": 474717.33125,
        "CashEarningsDistribution": 0.0,
        "StockEarningsDistribution": 0.0,
    }

    assert backtest.compare_market_detail.to_dict("r")[-1] == {
        "CumDailyReturn": -0.61003,
        "CumTaiExDailyReturn": -0.0963,
        "date": "2018-12-28",
    }
    assert backtest.compare_market_stats["AnnualTaiexReturnPer"] == -9.6
    assert backtest.compare_market_stats["AnnualReturnPer"] == 0.68


def test_continue_holding_add_strategy(data_loader):
    obj = strategies.BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        data_loader=data_loader,
    )
    obj.add_strategy(strategies.ContinueHolding)
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 2810
    assert int(obj.final_stats.MaxLoss) == -9663
    assert int(obj.final_stats.FinalProfit) == 3407

    assert obj.final_stats["MeanProfitPer"] == 0.56
    assert obj.final_stats["FinalProfitPer"] == 0.68
    assert obj.final_stats["MaxLossPer"] == -1.93

    assert obj.trade_detail.to_dict("r")[1] == {
        "EverytimeProfit": -96.83,
        "RealizedProfit": 0.0,
        "UnrealizedProfit": -96.83,
        "board_lot": 1000.0,
        "date": "2018-01-03",
        "hold_cost": 25.18583875,
        "hold_volume": 1000.0,
        "signal": 1,
        "stock_id": "0056",
        "trade_price": 25.15,
        "trader_fund": 474814.16125,
        "EverytimeTotalProfit": 474717.33125,
        "CashEarningsDistribution": 0.0,
        "StockEarningsDistribution": 0.0,
    }


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
            IndicatorsInfo(name=Indicators.BIAS, formula_value=24)
        ]
    )
    backtest.add_buy_rule(buy_rule_list=buy_rule_list)
    backtest.add_sell_rule(sell_rule_list=sell_rule_list)
    backtest.simulate()

    assert int(backtest.final_stats.MeanProfit) == 893
    assert int(backtest.final_stats.MaxLoss) == -863
    assert int(backtest.final_stats.FinalProfit) == 2845

    assert backtest.final_stats["MeanProfitPer"] == 0.18
    assert backtest.final_stats["FinalProfitPer"] == 0.57
    assert backtest.final_stats["MaxLossPer"] == -0.17

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
        "CumDailyReturn": -0.39843,
        "CumTaiExDailyReturn": -0.0963,
        "date": "2018-12-28",
    }

    assert backtest.compare_market_stats["AnnualTaiexReturnPer"] == -9.6
    assert backtest.compare_market_stats["AnnualReturnPer"] == 0.57


def test_bias_add_strategy(data_loader):
    obj = strategies.BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        data_loader=data_loader,
    )
    obj.add_strategy(strategies.Bias)
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 893
    assert int(obj.final_stats.MaxLoss) == -863
    assert int(obj.final_stats.FinalProfit) == 2845

    assert obj.final_stats["MeanProfitPer"] == 0.18
    assert obj.final_stats["FinalProfitPer"] == 0.57
    assert obj.final_stats["MaxLossPer"] == -0.17

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


def test_naive_kd(data_loader):
    obj = strategies.BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        strategy=strategies.NaiveKd,
        data_loader=data_loader,
    )
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 5418
    assert int(obj.final_stats.MaxLoss) == -2094
    assert int(obj.final_stats.FinalProfit) == 15033

    assert obj.final_stats["MeanProfitPer"] == 1.08
    assert obj.final_stats["FinalProfitPer"] == 3.01
    assert obj.final_stats["MaxLossPer"] == -0.42


def test_naive_kd_add_strategy(data_loader):
    obj = strategies.BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        # strategy=strategies.NaiveKd,
        data_loader=data_loader,
    )
    obj.add_strategy(strategies.NaiveKd)
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 5418
    assert int(obj.final_stats.MaxLoss) == -2094
    assert int(obj.final_stats.FinalProfit) == 15033

    assert obj.final_stats["MeanProfitPer"] == 1.08
    assert obj.final_stats["FinalProfitPer"] == 3.01
    assert obj.final_stats["MaxLossPer"] == -0.42


def test_kd(data_loader):
    self = strategies.BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        token=FINMIND_API_TOKEN,
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
    obj = strategies.BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        strategy=strategies.KdCrossOver,
        data_loader=data_loader,
    )
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 349
    assert int(obj.final_stats.MaxLoss) == -1223
    assert int(obj.final_stats.FinalProfit) == 933

    assert obj.final_stats["MeanProfitPer"] == 0.07
    assert obj.final_stats["FinalProfitPer"] == 0.19
    assert obj.final_stats["MaxLossPer"] == -0.24


def test_kd_crossover_add_strategy(data_loader):
    obj = strategies.BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        # strategy=strategies.KdCrossOver,
        data_loader=data_loader,
    )
    obj.add_strategy(strategies.KdCrossOver)
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 349
    assert int(obj.final_stats.MaxLoss) == -1223
    assert int(obj.final_stats.FinalProfit) == 933

    assert obj.final_stats["MeanProfitPer"] == 0.07
    assert obj.final_stats["FinalProfitPer"] == 0.19
    assert obj.final_stats["MaxLossPer"] == -0.24


def test_kd_crossover_add_indicators():
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

    assert int(backtest.final_stats.MeanProfit) == 349
    assert int(backtest.final_stats.MaxLoss) == -1223
    assert int(backtest.final_stats.FinalProfit) == 933

    assert backtest.final_stats["MeanProfitPer"] == 0.07
    assert backtest.final_stats["FinalProfitPer"] == 0.19
    assert backtest.final_stats["MaxLossPer"] == -0.24


def test_institutional_investors_follower(data_loader):
    obj = strategies.BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        strategy=strategies.InstitutionalInvestorsFollower,
        token=FINMIND_API_TOKEN,
    )
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 6021
    assert int(obj.final_stats.MaxLoss) == -15410
    assert int(obj.final_stats.FinalProfit) == 10699

    assert obj.final_stats["MeanProfitPer"] == 1.2
    assert obj.final_stats["FinalProfitPer"] == 2.14
    assert obj.final_stats["MaxLossPer"] == -3.08


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
                indicators="InstitutionalInvestorsOverBuy",
                more_or_less_than="equal",
                threshold=-1,
            ),
        ],
        [
            dict(
                indicators="InstitutionalInvestorsOverBuy",
                more_or_less_than="equal",
                threshold=1,
            ),
        ],
    ),
    (
        [
            dict(
                indicators="InstitutionalInvestorsOverBuy",
                more_or_less_than="=",
                threshold=-1,
            ),
        ],
        [
            dict(
                indicators="InstitutionalInvestorsOverBuy",
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
            IndicatorsInfo(name=Indicators.InstitutionalInvestorsFollower)
        ]
    )
    backtest.add_buy_rule(buy_rule_list=buy_rule_list)
    backtest.add_sell_rule(sell_rule_list=sell_rule_list)
    backtest.simulate()

    assert int(backtest.final_stats.MeanProfit) == 6021
    assert int(backtest.final_stats.MaxLoss) == -15410
    assert int(backtest.final_stats.FinalProfit) == 10699

    assert backtest.final_stats["MeanProfitPer"] == 1.2
    assert backtest.final_stats["FinalProfitPer"] == 2.14
    assert backtest.final_stats["MaxLossPer"] == -3.08


def test_institutional_investors_follower_add_strategy(data_loader):
    obj = strategies.BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        data_loader=data_loader,
    )
    obj.add_strategy(strategies.InstitutionalInvestorsFollower)
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 6021
    assert int(obj.final_stats.MaxLoss) == -15410
    assert int(obj.final_stats.FinalProfit) == 10699

    assert obj.final_stats["MeanProfitPer"] == 1.2
    assert obj.final_stats["FinalProfitPer"] == 2.14
    assert obj.final_stats["MaxLossPer"] == -3.08


def test_short_sale_margin_purchase_ratio(data_loader):
    obj = strategies.BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        strategy=strategies.ShortSaleMarginPurchaseRatio,
        data_loader=data_loader,
    )
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 12946
    assert int(obj.final_stats.MaxLoss) == -14706
    assert int(obj.final_stats.FinalProfit) == 22576

    assert obj.final_stats["MeanProfitPer"] == 2.59
    assert obj.final_stats["FinalProfitPer"] == 4.52
    assert obj.final_stats["MaxLossPer"] == -2.94


def test_short_sale_margin_purchase_ratio_add_strategy(data_loader):
    obj = strategies.BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        # strategy=strategies.ShortSaleMarginPurchaseRatio,
        data_loader=data_loader,
    )
    obj.add_strategy(strategies.ShortSaleMarginPurchaseRatio)
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 12946
    assert int(obj.final_stats.MaxLoss) == -14706
    assert int(obj.final_stats.FinalProfit) == 22576

    assert obj.final_stats["MeanProfitPer"] == 2.59
    assert obj.final_stats["FinalProfitPer"] == 4.52
    assert obj.final_stats["MaxLossPer"] == -2.94


def test_macd_crossover(data_loader):
    obj = strategies.BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        strategy=strategies.MacdCrossOver,
        data_loader=data_loader,
    )
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 1347
    assert int(obj.final_stats.MaxLoss) == -397
    assert int(obj.final_stats.FinalProfit) == 3232

    assert obj.final_stats["MeanProfitPer"] == 0.27
    assert obj.final_stats["FinalProfitPer"] == 0.65
    assert obj.final_stats["MaxLossPer"] == -0.08


def test_macd_crossover_add_strategy(data_loader):
    obj = strategies.BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        # strategy=strategies.MacdCrossOver,
        data_loader=data_loader,
    )
    obj.add_strategy(strategies.MacdCrossOver)
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 1347
    assert int(obj.final_stats.MaxLoss) == -397
    assert int(obj.final_stats.FinalProfit) == 3232

    assert obj.final_stats["MeanProfitPer"] == 0.27
    assert obj.final_stats["FinalProfitPer"] == 0.65
    assert obj.final_stats["MaxLossPer"] == -0.08


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
