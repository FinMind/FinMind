import pytest

from FinMind.BackTestSystem import BackTest
from FinMind.BackTestSystem.Strategies.ContinueHolding import ContinueHolding
from FinMind.BackTestSystem.Strategies.Bias import Bias
from FinMind.BackTestSystem.Strategies.NaiveKd import NaiveKd
from FinMind.BackTestSystem.Strategies.Kd import Kd
from FinMind.BackTestSystem.Strategies.KdCrossOver import KdCrossOver
from FinMind.BackTestSystem.Strategies.InstitutionalInvestorsFollower import (
    InstitutionalInvestorsFollower,
)
from FinMind.BackTestSystem.Strategies.ShortSaleMarginPurchaseRatio import (
    ShortSaleMarginPurchaseRatio,
)
from FinMind.BackTestSystem.Strategies.MacdCrossOver import MacdCrossOver
from FinMind.BackTestSystem.Strategies.MaCrossOver import MaCrossOver
from FinMind.BackTestSystem.Strategies.MaxMinPeriodBias import MaxMinPeriodBias


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
    final_stats = obj.get_final_stats()

    assert int(final_stats.MeanProfit) == 2821
    assert int(final_stats.MaxLoss) == -9663
    assert int(final_stats.FinalProfit) == 3407

    assert final_stats["MeanProfitPer[%]"] == 0.56
    assert final_stats["FinalProfitPer[%]"] == 0.68
    assert final_stats["MaxLossPer[%]"] == -1.93


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
    final_stats = obj.get_final_stats()

    assert int(final_stats.MeanProfit) == 989
    assert int(final_stats.MaxLoss) == -863
    assert int(final_stats.FinalProfit) == 2845

    assert final_stats["MeanProfitPer[%]"] == 0.20
    assert final_stats["FinalProfitPer[%]"] == 0.57
    assert final_stats["MaxLossPer[%]"] == -0.17


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
    final_stats = obj.get_final_stats()

    assert int(final_stats.MeanProfit) == 11959
    assert int(final_stats.MaxLoss) == -16840
    assert int(final_stats.FinalProfit) == 20442

    assert final_stats["MeanProfitPer[%]"] == 2.39
    assert final_stats["FinalProfitPer[%]"] == 4.09
    assert final_stats["MaxLossPer[%]"] == -3.37


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
    final_stats = obj.get_final_stats()

    assert int(final_stats.MeanProfit) == 5658
    assert int(final_stats.MaxLoss) == -6243
    assert int(final_stats.FinalProfit) == 10233

    assert final_stats["MeanProfitPer[%]"] == 1.13
    assert final_stats["FinalProfitPer[%]"] == 2.05
    assert final_stats["MaxLossPer[%]"] == -1.25


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
    final_stats = obj.get_final_stats()

    assert int(final_stats.MeanProfit) == 4240
    assert int(final_stats.MaxLoss) == -17322
    assert int(final_stats.FinalProfit) == 5197

    assert final_stats["MeanProfitPer[%]"] == 0.85
    assert final_stats["FinalProfitPer[%]"] == 1.04
    assert final_stats["MaxLossPer[%]"] == -3.46


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
    final_stats = obj.get_final_stats()

    assert int(final_stats.MeanProfit) == 7201
    assert int(final_stats.MaxLoss) == -23650
    assert int(final_stats.FinalProfit) == 13633

    assert final_stats["MeanProfitPer[%]"] == 1.44
    assert final_stats["FinalProfitPer[%]"] == 2.73
    assert final_stats["MaxLossPer[%]"] == -4.73


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
    final_stats = obj.get_final_stats()

    assert int(final_stats.MeanProfit) == 12179
    assert int(final_stats.MaxLoss) == -17331
    assert int(final_stats.FinalProfit) == 19952

    assert final_stats["MeanProfitPer[%]"] == 2.44
    assert final_stats["FinalProfitPer[%]"] == 3.99
    assert final_stats["MaxLossPer[%]"] == -3.47


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
    final_stats = obj.get_final_stats()

    assert int(final_stats.MeanProfit) == 2497
    assert int(final_stats.MaxLoss) == -3797
    assert int(final_stats.FinalProfit) == 5036

    assert final_stats["MeanProfitPer[%]"] == 0.5
    assert final_stats["FinalProfitPer[%]"] == 1.01
    assert final_stats["MaxLossPer[%]"] == -0.76


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
    final_stats = obj.get_final_stats()

    assert int(final_stats.MeanProfit) == 675
    assert int(final_stats.MaxLoss) == -6842
    assert int(final_stats.FinalProfit) == 444

    assert final_stats["MeanProfitPer[%]"] == 0.14
    assert final_stats["FinalProfitPer[%]"] == 0.09
    assert final_stats["MaxLossPer[%]"] == -1.37


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
    final_stats = obj.get_final_stats()

    assert int(final_stats.MeanProfit) == 0
    assert int(final_stats.MaxLoss) == 0
    assert int(final_stats.FinalProfit) == 0

    assert final_stats["MeanProfitPer[%]"] == 0
    assert final_stats["FinalProfitPer[%]"] == 0
    assert final_stats["MaxLossPer[%]"] == 0
