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

FINMIND_API_TOKEN = os.environ.get("FINMIND_API_TOKEN", "")


@pytest.fixture(scope="module")
def data_loader():
    data_loader = DataLoader()
    data_loader.login_by_token(FINMIND_API_TOKEN)
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


class FakeDataLoader:
    def __init__(self, industry_category_list):
        self._industry_category_list = industry_category_list

    def taiwan_stock_info(self):
        return pd.DataFrame(
            [
                {
                    "industry_category": industry_category,
                    "stock_id": "2330",
                    "stock_name": "台積電",
                    "type": "twse",
                    "date": "2026-08-09",
                }
                for industry_category in self._industry_category_list
            ]
        )


# TaiwanStockInfo 同一檔股票可能有多列，industry_category 除了產業別還會出現
# 「產業總稱」(電子工業/化學生技醫療) 與板別(創新板股票)。不論回傳順序如何，
# 都要拿到同一個產業別。
testdata_get_asset_underlying_type_duplicated = [
    (["半導體業", "電子工業"], "半導體業"),
    (["電子工業", "半導體業"], "半導體業"),
    (["其他電子業", "電子工業"], "其他電子業"),
    (["化學生技醫療", "化學工業"], "化學工業"),
    (["創新板股票", "汽車工業"], "汽車工業"),
    (["創新版股票", "創新板股票", "汽車工業"], "汽車工業"),
    (["水泥工業"], "水泥工業"),
    # 只剩總稱那列時，寧可回總稱也不要回空
    (["電子工業"], "電子工業"),
]


@pytest.mark.parametrize(
    "industry_category_list, expected",
    testdata_get_asset_underlying_type_duplicated,
)
def test_get_asset_underlying_type_duplicated(industry_category_list, expected):
    underlying_type = get_asset_underlying_type(
        "2330", FakeDataLoader(industry_category_list)
    )
    assert underlying_type == expected


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
