import datetime

import pandas as pd
import pytest

from FinMind.BackTestSystem.utils import (
    get_asset_underlying_type,
    get_underlying_trading_tax,
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
    "stock_id, return_value", testdata_get_asset_underlying_type,
)
def test_get_asset_underlying_type(stock_id, return_value, mocker):
    mock_load = mocker.patch("FinMind.Data.Load.FinData")
    mock_load.get_data.return_value = return_value
    underlying_type = get_asset_underlying_type(stock_id)
    assert underlying_type == "半導體業"


testdata_get_underlying_trading_tax = [("半導體", 0.003), ("ETF", 0.001)]


@pytest.mark.parametrize(
    "underlying_type, expected", testdata_get_underlying_trading_tax,
)
def test_get_underlying_trading_tax(underlying_type, expected):
    resp = get_underlying_trading_tax(underlying_type)
    assert resp == expected
