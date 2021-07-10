import pytest
import os

from FinMind import plotting
from FinMind.data import DataLoader

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
    df = df[df["date"] == max(df["date"])]
    df = df[df["HoldingSharesLevel"] != "total"]
    df["labels"] = df["HoldingSharesLevel"]
    df["series"] = df["percent"]
    assert plotting.pie(labels=df["labels"], series=df["series"])


def test_pie_failed():
    user_id = os.environ.get("FINMIND_USER", "")
    password = os.environ.get("FINMIND_PASSWORD", "")
    data_loader = DataLoader()
    data_loader.login(user_id, password)
    df = data_loader.taiwan_stock_month_revenue(
        stock_id="2330", start_date="2018-01-01", end_date="2021-03-03"
    )
    df["series"] = (
        df[["revenue_year", "revenue_month"]]
        .astype(str)
        .apply(lambda date: f"{date[0]}-{date[1]}M", axis=1)
    )
    df["labels"] = df["revenue"].map(lambda value: round(value * 1e-8, 2))
    with (pytest.raises(Exception)):
        plotting.pie(labels=df["labels"], series=df["series"])
