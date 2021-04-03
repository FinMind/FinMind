import pandas as pd
import pytest

from FinMind.BackTestSystem.utils import (
    get_asset_underlying_type,
    get_underlying_trading_tax,
    calculate_Datenbr,
    calculate_sharp_ratio,
    convert_Return2Annual,
    convert_period_days2years,
)

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
def test_get_asset_underlying_type(stock_id, return_value, mocker):
    mock_load = mocker.patch("FinMind.Data.Load.FinData")
    mock_load.return_value = return_value
    underlying_type = get_asset_underlying_type(stock_id)
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
    resp = calculate_Datenbr(day1, day2)
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
def test_convert_Return2Annual(period_return, period_years, expected):
    resp = convert_Return2Annual(period_return, period_years)
    assert resp == expected


testdata_convert_period_days2years = [(180, 0.4931506849315068), (30, 0.0821917808219178)]


@pytest.mark.parametrize(
    "days, expected",
    testdata_convert_period_days2years,
)
def test_convert_period_days2years(days, expected):
    resp = convert_period_days2years(days)
    assert resp == expected
