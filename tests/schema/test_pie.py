import os

import pytest

from FinMind.data import DataLoader
from FinMind.schema import PiePlotSchema


@pytest.fixture(scope="module")
def df():
    user_id = os.environ.get("FINMIND_USER", "")
    password = os.environ.get("FINMIND_PASSWORD", "")
    data_loader = DataLoader()
    data_loader.login(user_id, password)
    df = data_loader.taiwan_stock_holding_shares_per(
        stock_id="2890", start_date="2021-06-01", end_date="2021-07-03"
    )
    df["labels"] = df["HoldingSharesLevel"]
    df["series"] = df["percent"]
    return df


def test_PiePlotSchema(df):
    pie_plot_data = PiePlotSchema(**df.to_dict("list"))
    assert isinstance(pie_plot_data, PiePlotSchema)


def test_PiePlotSchema_df_convert(df):
    pie_plot_data = PiePlotSchema.df_convert(df)
    assert isinstance(pie_plot_data, PiePlotSchema)
