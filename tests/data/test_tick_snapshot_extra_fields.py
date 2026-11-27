import json
from unittest import mock

import pandas as pd
import pytest
import requests

import FinMind.data.finmind_api as finmind_api
from FinMind.data import DataLoader

BASE_ROW = {
    "open": 1000.0,
    "high": 1010.0,
    "low": 995.0,
    "close": 1005.0,
    "change_price": 5.0,
    "change_rate": 0.5,
    "average_price": 1003.2,
    "volume": 3,
    "total_volume": 12345,
    "amount": 3015000,
    "total_amount": 12384567000,
    "yesterday_volume": 23456.0,
    "buy_price": 1005.0,
    "buy_volume": 120.0,
    "sell_price": 1010.0,
    "sell_volume": 88.0,
    "volume_ratio": 0.53,
    "date": "2026-11-23 10:00:00.000",
    "stock_id": "2330",
    "TickType": 1,
}
EXTRA_FIELDS = {
    "yesterday_close": 1000.0,
    "limit_up": 1100.0,
    "limit_down": 900.0,
    "buy_prices": [1005.0, 1000.0, 995.0, 990.0, 985.0],
    "buy_volumes": [120, 300, 210, 150, 98],
    "sell_prices": [1010.0, 1015.0, 1020.0, 1025.0, 1030.0],
    "sell_volumes": [88, 140, 260, 175, 66],
    "inside_volume": 6000,
    "outside_volume": 6345,
    "after_hours_volume": 0,
    "is_closed": False,
}
# Sponsor Pro 上市櫃盤中零股欄位（量單位為股）
ODD_LOT_FIELDS = {
    "odd_lot_date": "2026-11-23 10:00:00.000",
    "odd_lot_open": 998.0,
    "odd_lot_high": 1010.0,
    "odd_lot_low": 995.0,
    "odd_lot_close": 1005.0,
    "odd_lot_change_price": 5.0,
    "odd_lot_change_rate": 0.5,
    "odd_lot_total_volume": 152340,
    "odd_lot_buy_price": 1005.0,
    "odd_lot_buy_volume": 320,
    "odd_lot_sell_price": 1010.0,
    "odd_lot_sell_volume": 185,
    "odd_lot_is_simulated": False,
}
ROW_WITH_EXTRA = {**BASE_ROW, **EXTRA_FIELDS}
ROW_WITH_ODD_LOT = {**ROW_WITH_EXTRA, **ODD_LOT_FIELDS}
# 興櫃股票沒有盤中零股，odd_lot_ 欄位為 null
ROW_WITH_NULL_ODD_LOT = {
    **ROW_WITH_EXTRA,
    "stock_id": "6488",
    **{field: None for field in ODD_LOT_FIELDS},
}
# Sponsor Pro 新欄位缺值時為 null，仍須能正常轉成 DataFrame
ROW_WITH_NULL_EXTRA = {
    **BASE_ROW,
    "stock_id": "001",
    **{field: None for field in EXTRA_FIELDS},
}


def make_response(body: dict) -> requests.Response:
    response = requests.Response()
    response.status_code = 200
    response._content = json.dumps(body, ensure_ascii=False).encode("utf-8")
    response.encoding = "utf-8"
    return response


@pytest.fixture
def data_loader():
    # 不帶 token、不打真的 API：建構時的登入與 session.get 一律 mock
    with mock.patch.object(DataLoader, "login_by_token", return_value=True):
        return DataLoader()


@pytest.fixture(autouse=True)
def reset_profile_notice_flag():
    finmind_api._realtime_profile_notice_logged = False
    yield
    finmind_api._realtime_profile_notice_logged = False


def get_snapshot(data_loader, rows: list, **kwargs) -> pd.DataFrame:
    response = make_response({"msg": "success", "status": 200, "data": rows})
    with mock.patch.object(
        data_loader._FinMindApi__session, "get", return_value=response
    ):
        return data_loader.taiwan_stock_tick_snapshot(**kwargs)


def test_tick_snapshot_extra_fields(data_loader):
    df = get_snapshot(data_loader, [ROW_WITH_EXTRA], stock_id="2330")
    assert list(df.columns) == list(ROW_WITH_EXTRA)
    assert len(df) == 1
    row = df.iloc[0]
    assert row["yesterday_close"] == 1000.0
    assert row["limit_up"] == 1100.0
    assert row["limit_down"] == 900.0
    assert row["buy_prices"] == EXTRA_FIELDS["buy_prices"]
    assert row["buy_volumes"] == EXTRA_FIELDS["buy_volumes"]
    assert row["sell_prices"] == EXTRA_FIELDS["sell_prices"]
    assert row["sell_volumes"] == EXTRA_FIELDS["sell_volumes"]
    assert row["inside_volume"] == 6000
    assert row["outside_volume"] == 6345
    assert row["after_hours_volume"] == 0
    assert bool(row["is_closed"]) is False


def test_tick_snapshot_extra_fields_with_null(data_loader):
    df = get_snapshot(
        data_loader,
        [ROW_WITH_EXTRA, ROW_WITH_NULL_EXTRA],
        stock_id=["2330", "001"],
    )
    assert list(df.columns) == list(ROW_WITH_EXTRA)
    assert df["stock_id"].tolist() == ["2330", "001"]
    index_row = df.iloc[1]
    for field in EXTRA_FIELDS:
        assert pd.isna(index_row[field]), field
    # list 欄位每格保留為長度 5 的 list，可直接展開成五檔
    buy_prices = pd.DataFrame(
        df["buy_prices"].iloc[:1].tolist(),
        columns=[f"buy_price_{i}" for i in range(1, 6)],
    )
    assert buy_prices.iloc[0].tolist() == EXTRA_FIELDS["buy_prices"]


def test_tick_snapshot_without_extra_fields(data_loader):
    # 回應沒有新欄位時維持原本欄位
    df = get_snapshot(data_loader, [BASE_ROW], stock_id="2330")
    pd.testing.assert_frame_equal(df, pd.DataFrame([BASE_ROW]))


def test_tick_snapshot_sponsor_response_without_extra_fields(data_loader):
    # Sponsor 會員的回應只有原本欄位（沒有 Sponsor Pro 新欄位），多檔也能正常轉成 DataFrame
    rows = [
        BASE_ROW,
        {**BASE_ROW, "stock_id": "2317", "close": 210.5, "TickType": 2},
    ]
    df = get_snapshot(data_loader, rows, stock_id=["2330", "2317"])
    assert list(df.columns) == list(BASE_ROW)
    assert not set(EXTRA_FIELDS) & set(df.columns)
    assert df["stock_id"].tolist() == ["2330", "2317"]
    assert df["close"].tolist() == [1005.0, 210.5]
    assert df["TickType"].tolist() == [1, 2]


def test_tick_snapshot_odd_lot_fields(data_loader):
    df = get_snapshot(data_loader, [ROW_WITH_ODD_LOT], stock_id="2330")
    assert list(df.columns) == list(ROW_WITH_ODD_LOT)
    row = df.iloc[0]
    for field, value in ODD_LOT_FIELDS.items():
        assert row[field] == value, field
    assert bool(row["odd_lot_is_simulated"]) is False


def test_tick_snapshot_odd_lot_fields_with_null(data_loader):
    df = get_snapshot(
        data_loader,
        [ROW_WITH_ODD_LOT, ROW_WITH_NULL_ODD_LOT],
        stock_id=["2330", "6488"],
    )
    assert list(df.columns) == list(ROW_WITH_ODD_LOT)
    assert df["stock_id"].tolist() == ["2330", "6488"]
    assert df["odd_lot_total_volume"].iloc[0] == 152340
    emerging_row = df.iloc[1]
    for field in ODD_LOT_FIELDS:
        assert pd.isna(emerging_row[field]), field
