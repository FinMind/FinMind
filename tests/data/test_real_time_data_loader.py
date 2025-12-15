import os

import pandas as pd
import pytest

from FinMind.data import DataLoader

FINMIND_API_TOKEN = os.environ.get("FINMIND_API_TOKEN", "")


@pytest.fixture(scope="module")
def data_loader():
    data_loader = DataLoader(token=FINMIND_API_TOKEN)
    return data_loader


def assert_data(data: pd.DataFrame, correct_columns_name: list):
    errors = []
    if not all(data.columns == correct_columns_name):
        errors.append("data columns mismatch")
    if not len(data) > 0:
        errors.append("data is empty")
    assert not errors, "errors :\n    {}".format("\n".join(errors))


def test_taiwan_stock_info_2330(data_loader):
    data = data_loader.taiwan_stock_tick_snapshot(stock_id="2330")
    assert_data(
        data,
        [
            "open",
            "high",
            "low",
            "close",
            "change_price",
            "change_rate",
            "average_price",
            "volume",
            "total_volume",
            "amount",
            "total_amount",
            "yesterday_volume",
            "buy_price",
            "buy_volume",
            "sell_price",
            "sell_volume",
            "volume_ratio",
            "date",
            "stock_id",
            "TickType",
        ],
    )


def test_taiwan_stock_info_list(data_loader):
    data = data_loader.taiwan_stock_tick_snapshot(
        stock_id=["2330", "0050", "2317", "0056"]
    )
    assert_data(
        data,
        [
            "open",
            "high",
            "low",
            "close",
            "change_price",
            "change_rate",
            "average_price",
            "volume",
            "total_volume",
            "amount",
            "total_amount",
            "yesterday_volume",
            "buy_price",
            "buy_volume",
            "sell_price",
            "sell_volume",
            "volume_ratio",
            "date",
            "stock_id",
            "TickType",
        ],
    )


def test_taiwan_stock_info_all(data_loader):
    data = data_loader.taiwan_stock_tick_snapshot()
    assert_data(
        data,
        [
            "open",
            "high",
            "low",
            "close",
            "change_price",
            "change_rate",
            "average_price",
            "volume",
            "total_volume",
            "amount",
            "total_amount",
            "yesterday_volume",
            "buy_price",
            "buy_volume",
            "sell_price",
            "sell_volume",
            "volume_ratio",
            "date",
            "stock_id",
            "TickType",
        ],
    )


def test_taiwan_futures_snapshot(data_loader):
    data = data_loader.taiwan_futures_snapshot(futures_id="TXF")
    assert_data(
        data,
        [
            "open",
            "high",
            "low",
            "close",
            "change_price",
            "change_rate",
            "average_price",
            "volume",
            "total_volume",
            "amount",
            "total_amount",
            "yesterday_volume",
            "buy_price",
            "buy_volume",
            "sell_price",
            "sell_volume",
            "volume_ratio",
            "date",
            "futures_id",
            "TickType",
        ],
    )


def test_taiwan_options_snapshot(data_loader):
    data = data_loader.taiwan_options_snapshot(options_id="TXO")
    assert_data(
        data,
        [
            "open",
            "high",
            "low",
            "close",
            "change_price",
            "change_rate",
            "average_price",
            "volume",
            "total_volume",
            "amount",
            "total_amount",
            "yesterday_volume",
            "buy_price",
            "buy_volume",
            "sell_price",
            "sell_volume",
            "volume_ratio",
            "date",
            "options_id",
            "TickType",
        ],
    )
