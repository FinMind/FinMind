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
ROW_WITH_EXTRA = {**BASE_ROW, **EXTRA_FIELDS}
# 新欄位缺值時為 null（例：無漲跌停價、指數沒有五檔）
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
