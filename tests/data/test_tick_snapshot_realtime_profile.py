import json
from unittest import mock

import pandas as pd
import pytest
import requests
from loguru import logger

import FinMind.data.finmind_api as finmind_api
from FinMind.data import DataLoader, RealtimeProfileRequiredError

PROFILE_NOTICE = (
    "依臺灣證券交易所規定，使用即時資料須於會員中心填寫姓名、電話、地址。"
    "2027-01-31 起未填寫者將無法使用即時資料："
    "https://finmindtrade.com/analysis/#/account/user"
)
PROFILE_REQUIRED_MSG = (
    "依臺灣證券交易所規定，使用即時資料須先於會員中心填寫姓名、電話、地址："
    "https://finmindtrade.com/analysis/#/account/user"
)
SOURCE_NOTICE = "資訊來源：臺灣證券交易所"
SNAPSHOT_ROW = {
    "open": 1000.0,
    "high": 1010.0,
    "low": 995.0,
    "close": 1005.0,
    "date": "2026-11-02 10:00:00.000",
    "stock_id": "2330",
}


def make_response(status_code: int, body: dict) -> requests.Response:
    # 用真的 requests.Response，保留 bool(response) 在 4xx 為 False 的行為
    response = requests.Response()
    response.status_code = status_code
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


@pytest.fixture
def warnings_log():
    messages = []
    sink_id = logger.add(
        lambda message: messages.append(message.record["message"]),
        level="WARNING",
    )
    yield messages
    logger.remove(sink_id)


def mock_session_get(data_loader, response):
    return mock.patch.object(
        data_loader._FinMindApi__session, "get", return_value=response
    )


def test_tick_snapshot_profile_completed_no_notice(data_loader, warnings_log):
    # 已填寫：回應只有 msg/status/data/source_notice，行為與原本相同、不提醒
    response = make_response(
        200,
        {
            "msg": "success",
            "status": 200,
            "data": [SNAPSHOT_ROW],
            "source_notice": SOURCE_NOTICE,
        },
    )
    with mock_session_get(data_loader, response) as session_get:
        df = data_loader.taiwan_stock_tick_snapshot(stock_id="2330")
    pd.testing.assert_frame_equal(df, pd.DataFrame([SNAPSHOT_ROW]))
    assert session_get.call_args.args[0].endswith(
        "/v4/taiwan_stock_tick_snapshot"
    )
    assert warnings_log == []
    assert finmind_api._realtime_profile_notice_logged is False


def test_tick_snapshot_profile_notice_logged_once(data_loader, warnings_log):
    # 未填寫、尚未到期：照常回資料，profile_notice 同一個 process 只提醒一次
    response = make_response(
        200,
        {
            "msg": "success",
            "status": 200,
            "data": [SNAPSHOT_ROW],
            "source_notice": SOURCE_NOTICE,
            "profile_notice": PROFILE_NOTICE,
        },
    )
    with mock_session_get(data_loader, response):
        first = data_loader.taiwan_stock_tick_snapshot(stock_id="2330")
        second = data_loader.taiwan_stock_tick_snapshot(stock_id="2330")
    expected = pd.DataFrame([SNAPSHOT_ROW])
    pd.testing.assert_frame_equal(first, expected)
    pd.testing.assert_frame_equal(second, expected)
    assert warnings_log == [PROFILE_NOTICE]
    assert "2027-01-31" in warnings_log[0]
    assert "https://finmindtrade.com/analysis/#/account/user" in (
        warnings_log[0]
    )


def test_tick_snapshot_profile_required_403_raises(data_loader, warnings_log):
    # 未填寫、已到期：403，raise 帶 api msg 全文（含會員中心連結）的例外
    response = make_response(
        403,
        {
            "msg": PROFILE_REQUIRED_MSG,
            "status": 403,
            "token_tail": "abcd",
        },
    )
    with mock_session_get(data_loader, response) as session_get:
        with pytest.raises(RealtimeProfileRequiredError) as exc_info:
            data_loader.taiwan_stock_tick_snapshot(stock_id="2330")
    assert str(exc_info.value) == PROFILE_REQUIRED_MSG
    # 403 不重試
    session_get.assert_called_once()
    assert warnings_log == []


def test_tick_snapshot_other_403_keeps_original_error(data_loader):
    # 其他 403（非用戶資料提醒）維持原本的錯誤
    response = make_response(403, {"msg": "Forbidden", "status": 403})
    with mock_session_get(data_loader, response):
        with pytest.raises(Exception, match="Forbidden") as exc_info:
            data_loader.taiwan_stock_tick_snapshot(stock_id="2330")
    assert not isinstance(exc_info.value, RealtimeProfileRequiredError)
