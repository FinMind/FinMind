import os

import pandas as pd
import pytest

from FinMind.data import DataLoader
from FinMind.strategies.utils import (
    get_asset_underlying_type,
    get_underlying_trading_tax,
    calculate_datenbr,
    calculate_sharp_ratio,
    period_return2annual_return,
    days2years,
)

user_id = os.environ.get("FINMIND_USER", "")
password = os.environ.get("FINMIND_PASSWORD", "")


@pytest.fixture(scope="module")
def data_loader():
    data_loader = DataLoader()
    data_loader.login(user_id, password)
    return data_loader


testdata_get_asset_underlying_type = [
    (
        "2330",
        pd.DataFrame(
            [
                {
                    "industry_category": "半導體業",
                    "stock_id": "2330",
                    "stock_name": "台積電",
                    "type": "twse",
                    "date": "2020-05-31",
                }
            ]
        ),
    )
]


@pytest.mark.parametrize(
    "stock_id, return_value",
    testdata_get_asset_underlying_type,
)
def test_get_asset_underlying_type(stock_id, return_value, data_loader):
    underlying_type = get_asset_underlying_type(stock_id, data_loader)
    assert underlying_type == "半導體業"


testdata_get_underlying_trading_tax = [("半導體", 0.003), ("ETF", 0.001)]


@pytest.mark.parametrize(
    "underlying_type, expected",
    testdata_get_underlying_trading_tax,
)
def test_get_underlying_trading_tax(underlying_type, expected):
    resp = get_underlying_trading_tax(underlying_type)
    assert resp == expected


testdata_calculate_Datenbr = [
    ("2020-01-01", "2020-01-05", 4),
    ("2019-12-29", "2020-01-03", 5),
]


@pytest.mark.parametrize(
    "day1, day2, expected",
    testdata_calculate_Datenbr,
)
def test_calculate_Datenbr(day1, day2, expected):
    resp = calculate_datenbr(day1, day2)
    assert resp == expected


testdata_calculate_sharp_ratio = [(0.05, 0.01, 79.37), (0.1, 0.21, 7.56)]


@pytest.mark.parametrize(
    "retrun, std, expected",
    testdata_calculate_sharp_ratio,
)
def test_calculate_sharp_ratio(retrun, std, expected):
    resp = calculate_sharp_ratio(retrun, std)
    assert resp == expected


testdata_convert_Return2Annual = [(0.2, 2, 0.0954), (0.5, 5, 0.0845)]


@pytest.mark.parametrize(
    "period_return, period_years, expected",
    testdata_convert_Return2Annual,
)
def test_return2annual(period_return, period_years, expected):
    resp = period_return2annual_return(period_return, period_years)
    assert resp == expected


testdata_period_days2years = [
    (180, 0.4931506849315068),
    (30, 0.0821917808219178),
]


@pytest.mark.parametrize(
    "days, expected",
    testdata_period_days2years,
)
def test_period_days2years(days, expected):
    resp = days2years(days)
    assert resp == expected
