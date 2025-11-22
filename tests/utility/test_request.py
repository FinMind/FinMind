import os

import pandas as pd
import requests

from FinMind.utility import request


def test_async_request_get():
    token = os.environ.get("FINMIND_API_TOKEN", "")
    url = (
        "https://api.finmindtrade.com/api/v4/taiwan_stock_trading_daily_report"
    )
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
    session = requests.Session()
    session.headers.update(
        {
            "Authorization": f"Bearer {token}",
        }
    )
    resp_list = request.async_request_get(
        session=session,
        url=url,
        params_list=parameter_list,
    )
    data_list = []
    [data_list.extend(resp.json()["data"]) for resp in resp_list]
    df = pd.DataFrame(data_list)
    return df
