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


STOCK_SNAPSHOT_COLUMNS = [
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
]
# 台股即時資訊新增欄位；有回傳時須整組都有
STOCK_SNAPSHOT_EXTRA_COLUMNS = [
    "yesterday_close",
    "limit_up",
    "limit_down",
    "buy_prices",
    "buy_volumes",
    "sell_prices",
    "sell_volumes",
    "inside_volume",
    "outside_volume",
    "after_hours_volume",
    "is_closed",
]
# 台股即時資訊盤中零股欄位；有回傳時須整組都有
STOCK_SNAPSHOT_ODD_LOT_COLUMNS = [
    "odd_lot_date",
    "odd_lot_open",
    "odd_lot_high",
    "odd_lot_low",
    "odd_lot_close",
    "odd_lot_change_price",
    "odd_lot_change_rate",
    "odd_lot_total_volume",
    "odd_lot_buy_price",
    "odd_lot_buy_volume",
    "odd_lot_sell_price",
    "odd_lot_sell_volume",
    "odd_lot_is_simulated",
]


def assert_stock_snapshot_data(data: pd.DataFrame, required_columns: list):
    errors = []
    columns = set(data.columns)
    missing = [column for column in required_columns if column not in columns]
    if missing:
        errors.append(f"missing columns: {missing}")
    extra_returned = [
        column for column in STOCK_SNAPSHOT_EXTRA_COLUMNS if column in columns
    ]
    if extra_returned and len(extra_returned) != len(
        STOCK_SNAPSHOT_EXTRA_COLUMNS
    ):
        errors.append(f"partial extra columns: {extra_returned}")
    odd_lot_returned = [
        column for column in STOCK_SNAPSHOT_ODD_LOT_COLUMNS if column in columns
    ]
    if odd_lot_returned and len(odd_lot_returned) != len(
        STOCK_SNAPSHOT_ODD_LOT_COLUMNS
    ):
        errors.append(f"partial odd lot columns: {odd_lot_returned}")
    if not len(data) > 0:
        errors.append("data is empty")
    assert not errors, "errors :\n    {}".format("\n".join(errors))


def test_taiwan_stock_info_2330(data_loader):
    data = data_loader.taiwan_stock_tick_snapshot(stock_id="2330")
    assert_stock_snapshot_data(data, STOCK_SNAPSHOT_COLUMNS)


def test_taiwan_stock_info_list(data_loader):
    data = data_loader.taiwan_stock_tick_snapshot(
        stock_id=["2330", "0050", "2317", "0056"]
    )
    assert_stock_snapshot_data(data, STOCK_SNAPSHOT_COLUMNS)


def test_taiwan_stock_info_all(data_loader):
    data = data_loader.taiwan_stock_tick_snapshot()
    assert_stock_snapshot_data(data, STOCK_SNAPSHOT_COLUMNS + ["name"])


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
