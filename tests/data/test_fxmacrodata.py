import io
import json
import socket
import urllib.error

import pytest

from FinMind.data.fxmacrodata import FXMacroDataApi, FXMacroDataError


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def read(self):
        return self.payload


def test_request_uses_v1_url_and_forwards_api_key_header(monkeypatch):
    captured = {}

    def fake_urlopen(request, timeout):
        captured["url"] = request.full_url
        captured["api_key"] = request.get_header("X-api-key")
        captured["timeout"] = timeout
        return FakeResponse(b'{"data": []}')

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    api = FXMacroDataApi(api_key="placeholder-token", timeout=12)

    assert api.request("calendar/USD", {"limit": 2}) == {"data": []}
    assert captured == {
        "url": "https://api.fxmacrodata.com/v1/calendar/USD?limit=2",
        "api_key": "placeholder-token",
        "timeout": 12,
    }


def test_predictions_flattens_nested_sources(monkeypatch):
    payload = {
        "data": [
            {
                "announcement_id": "usd_inflation_2026-08-31",
                "currency": "USD",
                "indicator": "inflation",
                "date": "2026-08-31",
                "predictions": [
                    {
                        "predicted_value": 2.5,
                        "prediction_source": "survey",
                    },
                    {
                        "predicted_value": 2.4,
                        "prediction_source": "model",
                    },
                ],
            }
        ]
    }
    monkeypatch.setattr(
        "urllib.request.urlopen",
        lambda request, timeout: FakeResponse(json.dumps(payload).encode()),
    )

    frame = FXMacroDataApi().predictions("USD", "inflation")

    assert frame["prediction_source"].tolist() == ["survey", "model"]
    assert frame["predicted_value"].tolist() == [2.5, 2.4]
    assert frame["announcement_id"].tolist() == [
        "usd_inflation_2026-08-31",
        "usd_inflation_2026-08-31",
    ]
    assert "predictions" not in frame.columns


def test_empty_data_returns_empty_frame(monkeypatch):
    monkeypatch.setattr(
        "urllib.request.urlopen",
        lambda request, timeout: FakeResponse(b'{"data": []}'),
    )

    assert FXMacroDataApi().calendar("USD").empty


@pytest.mark.parametrize(
    "failure",
    [
        urllib.error.URLError("DNS unavailable"),
        socket.timeout("request timed out"),
    ],
)
def test_transport_failures_use_client_exception(monkeypatch, failure):
    def fail(request, timeout):
        raise failure

    monkeypatch.setattr("urllib.request.urlopen", fail)

    with pytest.raises(FXMacroDataError, match="request to 'calendar/usd'"):
        FXMacroDataApi().calendar("USD")


def test_non_2xx_uses_client_exception(monkeypatch):
    def fail(request, timeout):
        raise urllib.error.HTTPError(
            request.full_url,
            503,
            "service unavailable",
            {},
            io.BytesIO(b'{"detail": "unavailable"}'),
        )

    monkeypatch.setattr("urllib.request.urlopen", fail)

    with pytest.raises(
        FXMacroDataError, match="failed with HTTP 503"
    ) as raised:
        FXMacroDataApi().calendar("USD")

    assert raised.value.__cause__ is None


def test_invalid_json_uses_client_exception(monkeypatch):
    monkeypatch.setattr(
        "urllib.request.urlopen",
        lambda request, timeout: FakeResponse(b"not-json"),
    )

    with pytest.raises(FXMacroDataError, match="was not valid JSON"):
        FXMacroDataApi().calendar("USD")
