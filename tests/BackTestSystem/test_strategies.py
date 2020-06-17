import pytest

from FinMind.BackTestSystem import BackTest
from FinMind.BackTestSystem.Strategies.ContinueHolding import ContinueHolding
from FinMind.BackTestSystem.Strategies.Bias import Bias
from FinMind.BackTestSystem.Strategies.NaiveKd import NaiveKd

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
