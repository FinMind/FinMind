import os

import pandas as pd

from FinMind.utility import request


def test_async_request_get():
    token = os.environ.get("FINMIND_API_TOKEN", "")
    url = (
        "https://api.finmindtrade.com/api/v4/taiwan_stock_trading_daily_report"
    )
    headers = {"Authorization": f"Bearer {token}"}
    parameter_list = [
        {
            "data_id": stock_id,
            "date": "2024-11-18",
        }
        for stock_id in [
            "2330",
            "2317",
            "0050",
            "0056",
            "1101",
            "00878",
            "00713",
            "00940",
        ]
    ]
    resp_list = request.async_request_get(
        url=url, params_list=parameter_list, headers=headers
    )
    data_list = []
    [data_list.extend(resp.json()["data"]) for resp in resp_list]
    df = pd.DataFrame(data_list)
    return df
