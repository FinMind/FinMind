import pandas as pd

from FinMind.BackTestSystem import BackTest
from FinMind.BackTestSystem.Strategies.Bias import Bias
from FinMind.BackTestSystem.Strategies.ContinueHolding import ContinueHolding
from FinMind.BackTestSystem.Strategies.InstitutionalInvestorsFollower import (
    InstitutionalInvestorsFollower,
)
from FinMind.BackTestSystem.Strategies.Kd import Kd
from FinMind.BackTestSystem.Strategies.KdCrossOver import KdCrossOver
from FinMind.BackTestSystem.Strategies.MaCrossOver import MaCrossOver
from FinMind.BackTestSystem.Strategies.MacdCrossOver import MacdCrossOver
from FinMind.BackTestSystem.Strategies.MaxMinPeriodBias import MaxMinPeriodBias
from FinMind.BackTestSystem.Strategies.NaiveKd import NaiveKd
from FinMind.BackTestSystem.Strategies.ShortSaleMarginPurchaseRatio import (
    ShortSaleMarginPurchaseRatio,
)


def test_get_stock_price():
    obj = BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        # strategy=ContinueHolding,
    )
    assert isinstance(obj.stock_price, pd.DataFrame)


def test_ContinueHolding():
    obj = BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        strategy=ContinueHolding,
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
        "CumDailyRetrun": -0.61003,
        "CumTaiexDailyRetrun": -0.0963,
        "date": "2018-12-28",
    }
    assert obj.compare_market_stats["AnnualTaiexReturnPer"] == -9.6
    assert obj.compare_market_stats["AnnualReturnPer"] == 0.68


def test_ContinueHolding_add_strategy():
    obj = BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        # strategy=ContinueHolding,
    )
    obj.add_strategy(ContinueHolding)
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


def test_Bias():
    obj = BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        strategy=Bias,
    )
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 984
    assert int(obj.final_stats.MaxLoss) == -863
    assert int(obj.final_stats.FinalProfit) == 2845

    assert obj.final_stats["MeanProfitPer"] == 0.20
    assert obj.final_stats["FinalProfitPer"] == 0.57
    assert obj.final_stats["MaxLossPer"] == -0.17

    assert obj.trade_detail.to_dict("r")[1] == {
        "EverytimeProfit": 0.0,
        "RealizedProfit": 0.0,
        "UnrealizedProfit": 0.0,
        "board_lot": 1000.0,
        "date": "2018-02-05",
        "hold_cost": 0.0,
        "hold_volume": 0.0,
        "signal": 0.0,
        "stock_id": "0056",
        "trade_price": 26.1,
        "trader_fund": 500000.0,
        "EverytimeTotalProfit": 500000.0,
        "CashEarningsDistribution": 0.0,
        "StockEarningsDistribution": 0.0,
    }

    assert obj.compare_market_detail.to_dict("r")[-1] == {
        "CumDailyRetrun": -0.39843,
        "CumTaiexDailyRetrun": -0.0963,
        "date": "2018-12-28",
    }

    assert obj.compare_market_stats["AnnualTaiexReturnPer"] == -9.6
    assert obj.compare_market_stats["AnnualReturnPer"] == 0.57


def test_Bias_add_strategy():
    obj = BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        # strategy=Bias,
    )
    obj.add_strategy(Bias)
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 984
    assert int(obj.final_stats.MaxLoss) == -863
    assert int(obj.final_stats.FinalProfit) == 2845

    assert obj.final_stats["MeanProfitPer"] == 0.20
    assert obj.final_stats["FinalProfitPer"] == 0.57
    assert obj.final_stats["MaxLossPer"] == -0.17

    assert obj.trade_detail.to_dict("r")[1] == {
        "EverytimeProfit": 0.0,
        "RealizedProfit": 0.0,
        "UnrealizedProfit": 0.0,
        "board_lot": 1000.0,
        "date": "2018-02-05",
        "hold_cost": 0.0,
        "hold_volume": 0.0,
        "signal": 0.0,
        "stock_id": "0056",
        "trade_price": 26.1,
        "trader_fund": 500000.0,
        "EverytimeTotalProfit": 500000.0,
        "CashEarningsDistribution": 0.0,
        "StockEarningsDistribution": 0.0,
    }


def test_NaiveKd():
    obj = BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        strategy=NaiveKd,
    )
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 5418
    assert int(obj.final_stats.MaxLoss) == -2094
    assert int(obj.final_stats.FinalProfit) == 15033

    assert obj.final_stats["MeanProfitPer"] == 1.08
    assert obj.final_stats["FinalProfitPer"] == 3.01
    assert obj.final_stats["MaxLossPer"] == -0.42


def test_NaiveKd_add_strategy():
    obj = BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        # strategy=NaiveKd,
    )
    obj.add_strategy(NaiveKd)
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 5418
    assert int(obj.final_stats.MaxLoss) == -2094
    assert int(obj.final_stats.FinalProfit) == 15033

    assert obj.final_stats["MeanProfitPer"] == 1.08
    assert obj.final_stats["FinalProfitPer"] == 3.01
    assert obj.final_stats["MaxLossPer"] == -0.42


def test_Kd():
    obj = BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        strategy=Kd,
    )
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 2356
    assert int(obj.final_stats.MaxLoss) == -1425
    assert int(obj.final_stats.FinalProfit) == 6196

    assert obj.final_stats["MeanProfitPer"] == 0.47
    assert obj.final_stats["FinalProfitPer"] == 1.24
    assert obj.final_stats["MaxLossPer"] == -0.29


def test_Kd_add_strategy():
    obj = BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        # strategy=Kd,
    )
    obj.add_strategy(Kd)
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 2356
    assert int(obj.final_stats.MaxLoss) == -1425
    assert int(obj.final_stats.FinalProfit) == 6196

    assert obj.final_stats["MeanProfitPer"] == 0.47
    assert obj.final_stats["FinalProfitPer"] == 1.24
    assert obj.final_stats["MaxLossPer"] == -0.29


def test_KdCrossOver():
    obj = BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        strategy=KdCrossOver,
    )
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 349
    assert int(obj.final_stats.MaxLoss) == -1223
    assert int(obj.final_stats.FinalProfit) == 933

    assert obj.final_stats["MeanProfitPer"] == 0.07
    assert obj.final_stats["FinalProfitPer"] == 0.19
    assert obj.final_stats["MaxLossPer"] == -0.24


def test_KdCrossOver_add_strategy():
    obj = BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        # strategy=KdCrossOver,
    )
    obj.add_strategy(KdCrossOver)
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 349
    assert int(obj.final_stats.MaxLoss) == -1223
    assert int(obj.final_stats.FinalProfit) == 933

    assert obj.final_stats["MeanProfitPer"] == 0.07
    assert obj.final_stats["FinalProfitPer"] == 0.19
    assert obj.final_stats["MaxLossPer"] == -0.24


def test_InstitutionalInvestorsFollower():
    obj = BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        strategy=InstitutionalInvestorsFollower,
    )
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 6021
    assert int(obj.final_stats.MaxLoss) == -15410
    assert int(obj.final_stats.FinalProfit) == 10699

    assert obj.final_stats["MeanProfitPer"] == 1.2
    assert obj.final_stats["FinalProfitPer"] == 2.14
    assert obj.final_stats["MaxLossPer"] == -3.08


def test_InstitutionalInvestorsFollower_add_strategy():
    obj = BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        # strategy=InstitutionalInvestorsFollower,
    )
    obj.add_strategy(InstitutionalInvestorsFollower)
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 6021
    assert int(obj.final_stats.MaxLoss) == -15410
    assert int(obj.final_stats.FinalProfit) == 10699

    assert obj.final_stats["MeanProfitPer"] == 1.2
    assert obj.final_stats["FinalProfitPer"] == 2.14
    assert obj.final_stats["MaxLossPer"] == -3.08


def test_ShortSaleMarginPurchaseRatio():
    obj = BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        strategy=ShortSaleMarginPurchaseRatio,
    )
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 12946
    assert int(obj.final_stats.MaxLoss) == -14706
    assert int(obj.final_stats.FinalProfit) == 22576

    assert obj.final_stats["MeanProfitPer"] == 2.59
    assert obj.final_stats["FinalProfitPer"] == 4.52
    assert obj.final_stats["MaxLossPer"] == -2.94


def test_ShortSaleMarginPurchaseRatio_add_strategy():
    obj = BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        # strategy=ShortSaleMarginPurchaseRatio,
    )
    obj.add_strategy(ShortSaleMarginPurchaseRatio)
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 12946
    assert int(obj.final_stats.MaxLoss) == -14706
    assert int(obj.final_stats.FinalProfit) == 22576

    assert obj.final_stats["MeanProfitPer"] == 2.59
    assert obj.final_stats["FinalProfitPer"] == 4.52
    assert obj.final_stats["MaxLossPer"] == -2.94


def test_MacdCrossOver():
    obj = BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        strategy=MacdCrossOver,
    )
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 1347
    assert int(obj.final_stats.MaxLoss) == -397
    assert int(obj.final_stats.FinalProfit) == 3232

    assert obj.final_stats["MeanProfitPer"] == 0.27
    assert obj.final_stats["FinalProfitPer"] == 0.65
    assert obj.final_stats["MaxLossPer"] == -0.08


def test_MacdCrossOver_add_strategy():
    obj = BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        # strategy=MacdCrossOver,
    )
    obj.add_strategy(MacdCrossOver)
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 1347
    assert int(obj.final_stats.MaxLoss) == -397
    assert int(obj.final_stats.FinalProfit) == 3232

    assert obj.final_stats["MeanProfitPer"] == 0.27
    assert obj.final_stats["FinalProfitPer"] == 0.65
    assert obj.final_stats["MaxLossPer"] == -0.08


def test_MaCrossOver():
    obj = BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        strategy=MaCrossOver,
    )
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == -381
    assert int(obj.final_stats.MaxLoss) == -1230
    assert int(obj.final_stats.FinalProfit) == -1230

    assert obj.final_stats["MeanProfitPer"] == -0.08
    assert obj.final_stats["FinalProfitPer"] == -0.25
    assert obj.final_stats["MaxLossPer"] == -0.25


def test_MaCrossOver_add_strategy():
    obj = BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        # strategy=MaCrossOver,
    )
    obj.add_strategy(MaCrossOver)
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == -381
    assert int(obj.final_stats.MaxLoss) == -1230
    assert int(obj.final_stats.FinalProfit) == -1230

    assert obj.final_stats["MeanProfitPer"] == -0.08
    assert obj.final_stats["FinalProfitPer"] == -0.25
    assert obj.final_stats["MaxLossPer"] == -0.25


def test_MaxMinPeriodBias():
    obj = BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        strategy=MaxMinPeriodBias,
    )
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 0
    assert int(obj.final_stats.MaxLoss) == 0
    assert int(obj.final_stats.FinalProfit) == 0

    assert obj.final_stats["MeanProfitPer"] == 0
    assert obj.final_stats["FinalProfitPer"] == 0
    assert obj.final_stats["MaxLossPer"] == 0


def test_MaxMinPeriodBias_add_strategy():
    obj = BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=500000.0,
        fee=0.001425,
        # strategy=MaxMinPeriodBias,
    )
    obj.add_strategy(MaxMinPeriodBias)
    obj.simulate()

    assert int(obj.final_stats.MeanProfit) == 0
    assert int(obj.final_stats.MaxLoss) == 0
    assert int(obj.final_stats.FinalProfit) == 0

    assert obj.final_stats["MeanProfitPer"] == 0
    assert obj.final_stats["FinalProfitPer"] == 0
    assert obj.final_stats["MaxLossPer"] == 0
