import pytest
import os

from FinMind import plotting
from FinMind.data import DataLoader
from FinMind.schema import PiePlotSchema

testdata_pie = [
    ("1220", "2021-06-01", "2021-07-03"),
    ("2330", "2021-06-01", "2021-07-03"),
]


@pytest.mark.parametrize("stock_id, start_date, end_date", testdata_pie)
def test_pie(stock_id, start_date, end_date):
    user_id = os.environ.get("FINMIND_USER", "")
    password = os.environ.get("FINMIND_PASSWORD", "")
    data_loader = DataLoader()
    data_loader.login(user_id, password)
    df = data_loader.taiwan_stock_holding_shares_per(
        stock_id=stock_id, start_date=start_date, end_date=end_date
    )
    df["labels"] = df["HoldingSharesLevel"]
    df["series"] = df["percent"]
    pie_plot_data = PiePlotSchema.df_convert(df)
    assert plotting.pie(pie_plot_data)
