from FinMind import plotting
from FinMind.data import DataLoader
import pytest


testdata_kline = [
    ("1220", "2015-01-01", "2020-05-19"),
    ("2330", "2018-01-01", "2021-03-03"),
]


@pytest.mark.parametrize("stock_id, start_date, end_date", testdata_kline)
def test_kline(stock_id, start_date, end_date):
    dl = DataLoader()
    stock_data = dl.taiwan_stock_daily_adj(stock_id, start_date, end_date)
    assert plotting.kline(stock_data)
