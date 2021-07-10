import os

import pytest

from FinMind.data import DataLoader
from FinMind.schema import BarPlotSchema


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
    df["series"] = df["revenue"].map(lambda value: round(value * 1e-8, 2))
    return df


def test_BarPlotSchema(df):
    bar_plot_data = BarPlotSchema(**df.to_dict("list"))
    assert isinstance(bar_plot_data, BarPlotSchema)


def test_BarPlotSchema_df_convert(df):
    bar_plot_data = BarPlotSchema.df_convert(df)
    assert isinstance(bar_plot_data, BarPlotSchema)
