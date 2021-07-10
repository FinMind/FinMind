import os

import pytest

from FinMind.data import DataLoader
from FinMind.schema import LinePlotSchema


@pytest.fixture(scope="module")
def df():
    user_id = os.environ.get("FINMIND_USER", "")
    password = os.environ.get("FINMIND_PASSWORD", "")
    data_loader = DataLoader()
    data_loader.login(user_id, password)
    df = data_loader.taiwan_stock_month_revenue(
        stock_id="2890", start_date="2018-1M", end_date="2021-7M"
    )
    df["labels"] = (
        df[["revenue_year", "revenue_month"]]
        .astype(str)
        .apply(lambda date: f"{date[0]}-{date[1]}M", axis=1)
    )
    df["series"] = df["revenue"].apply(lambda value: round(value * 1e-8, 2))
    return df


def test_LinePlotSchema(df):
    line_plot_data = LinePlotSchema(**df.to_dict("list"))
    assert isinstance(line_plot_data, LinePlotSchema)


def test_LinePlotSchema_df_convert(df):
    line_plot_data = LinePlotSchema.df_convert(df)
    assert isinstance(line_plot_data, LinePlotSchema)
