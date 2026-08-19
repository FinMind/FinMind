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
