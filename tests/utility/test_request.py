import hashlib

import pytest
import requests

from FinMind.utility import request


def test_async_request_get(monkeypatch):
    session = object()
    url = "https://example.test/data"
    parameter_list = [
        {
            "data_id": stock_id,
        }
        for stock_id in ["2330", "2317", "0050", "0056"]
    ]

    def request_get(
        received_session,
        received_url,
        params,
        timeout,
        max_retry_times,
        verbose,
    ):
        assert received_session is session
        assert received_url == url
        assert timeout == 5
        assert max_retry_times == 2
        assert verbose is False
        return params["data_id"]

    monkeypatch.setattr(request, "request_get", request_get)

    resp_list = request.async_request_get(
        session=session,
        url=url,
        params_list=parameter_list,
        timeout=5,
        max_retry_times=2,
        auto_tune=False,
        max_concurrency=2,
        batch_size=2,
    )

    assert sorted(resp_list) == ["0050", "0056", "2317", "2330"]


class _ApiResponse:
    def __init__(self, status_code, location="", content=b"", text=""):
        self.status_code = status_code
        self.headers = {"Location": location} if location else {}
        self.content = content
        self.text = text


class _FakeSession:
    def __init__(self, responses=None):
        self.responses = responses
        self.calls = 0

    def get(self, url, **kwargs):
        assert kwargs["allow_redirects"] is False
        self.calls += 1
        if self.responses:
            return self.responses.pop(0)
        return _ApiResponse(307, location=f"https://object.test/{self.calls}")


class _ObjectResponse:
    def __init__(self, status_code, body=b"", headers=None, fail_after=None):
        self.status_code = status_code
        self.body = body
        self.headers = headers or {}
        self.fail_after = fail_after

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def iter_content(self, chunk_size=1):
        if self.fail_after is None:
            yield self.body
            return
        yield self.body[: self.fail_after]
        raise requests.exceptions.ChunkedEncodingError("IncompleteRead")


def _etag(body):
    return f'"{hashlib.md5(body).hexdigest()}"'


def _patch_object_get(monkeypatch, handler):
    calls = []

    def fake_get(url, headers=None, stream=False, timeout=None):
        assert stream is True
        assert "Authorization" not in (headers or {})
        calls.append(dict(headers or {}))
        return handler(len(calls), headers or {})

    monkeypatch.setattr(request.requests, "get", fake_get)
    monkeypatch.setattr(request.time, "sleep", lambda seconds: None)
    return calls


BODY = bytes(range(256)) * 40


def test_download_storage_object_full(monkeypatch):
    def handler(n, headers):
        return _ObjectResponse(
            200,
            BODY,
            {"ETag": _etag(BODY), "Content-Length": str(len(BODY))},
        )

    calls = _patch_object_get(monkeypatch, handler)
    content = request.download_storage_object(
        _FakeSession(), "https://api.test"
    )
    assert content == BODY
    assert calls == [{}]


def test_download_storage_object_resume_after_interrupt(monkeypatch):
    cut = 3000

    def handler(n, headers):
        if n == 1:
            return _ObjectResponse(
                200,
                BODY,
                {"ETag": _etag(BODY), "Content-Length": str(len(BODY))},
                fail_after=cut,
            )
        assert headers == {"Range": f"bytes={cut}-", "If-Match": _etag(BODY)}
        return _ObjectResponse(206, BODY[cut:], {"ETag": _etag(BODY)})

    session = _FakeSession()
    calls = _patch_object_get(monkeypatch, handler)
    content = request.download_storage_object(session, "https://api.test")
    assert content == BODY
    assert len(calls) == 2
    # 每次重試都重新取得下載網址
    assert session.calls == 2


def test_download_storage_object_restart_when_object_changed(monkeypatch):
    new_body = BODY[::-1]

    def handler(n, headers):
        if n == 1:
            return _ObjectResponse(
                200,
                BODY,
                {"ETag": _etag(BODY), "Content-Length": str(len(BODY))},
                fail_after=3000,
            )
        if n == 2:
            return _ObjectResponse(412)
        assert headers == {}
        return _ObjectResponse(
            200,
            new_body,
            {"ETag": _etag(new_body), "Content-Length": str(len(new_body))},
        )

    calls = _patch_object_get(monkeypatch, handler)
    content = request.download_storage_object(
        _FakeSession(), "https://api.test"
    )
    assert content == new_body
    assert len(calls) == 3


def test_download_storage_object_resume_silent_truncation(monkeypatch):
    cut = 5000

    def handler(n, headers):
        if n == 1:
            # 連線提前結束但沒有丟例外
            return _ObjectResponse(
                200,
                BODY[:cut],
                {"ETag": _etag(BODY), "Content-Length": str(len(BODY))},
            )
        assert headers["Range"] == f"bytes={cut}-"
        return _ObjectResponse(206, BODY[cut:], {"ETag": _etag(BODY)})

    _patch_object_get(monkeypatch, handler)
    content = request.download_storage_object(
        _FakeSession(), "https://api.test"
    )
    assert content == BODY


def test_download_storage_object_retry_on_md5_mismatch(monkeypatch):
    corrupted = b"x" + BODY[1:]

    def handler(n, headers):
        body = corrupted if n == 1 else BODY
        return _ObjectResponse(
            200,
            body,
            {"ETag": _etag(BODY), "Content-Length": str(len(BODY))},
        )

    calls = _patch_object_get(monkeypatch, handler)
    content = request.download_storage_object(
        _FakeSession(), "https://api.test"
    )
    assert content == BODY
    assert calls == [{}, {}]


def test_download_storage_object_multipart_etag_skips_md5(monkeypatch):
    def handler(n, headers):
        return _ObjectResponse(
            200,
            BODY,
            {"ETag": '"abc-1"', "Content-Length": str(len(BODY))},
        )

    _patch_object_get(monkeypatch, handler)
    content = request.download_storage_object(
        _FakeSession(), "https://api.test"
    )
    assert content == BODY


def test_download_storage_object_api_error(monkeypatch):
    session = _FakeSession(
        [_ApiResponse(404, text='{"detail":"Object not found"}')]
    )
    _patch_object_get(monkeypatch, lambda n, headers: None)
    with pytest.raises(Exception, match="Final response status: 404"):
        request.download_storage_object(session, "https://api.test")


def test_download_storage_object_give_up(monkeypatch):
    def handler(n, headers):
        return _ObjectResponse(
            200,
            BODY,
            {"ETag": _etag(BODY), "Content-Length": str(len(BODY))},
            fail_after=10,
        )

    _patch_object_get(monkeypatch, handler)
    with pytest.raises(Exception, match="failed after 3 retries"):
        request.download_storage_object(
            _FakeSession(), "https://api.test", max_retry_times=3
        )
