import os

import pytest

from FinMind.data import DataLoader
from FinMind.schema.plot import Labels, Series, convert_labels_series_schema


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


def test_Labels(df):
    labels = df.to_dict("list")["labels"]
    assert Labels(labels=labels)


def test_Series(df):
    series = df.to_dict("list")["series"]
    assert Series(series=series)


def test_convert_labels_series_schema(df):
    labels = df.to_dict("list")["labels"]
    series = df.to_dict("list")["series"]
    labels, series = convert_labels_series_schema(labels=labels, series=series)
    assert isinstance(labels, Labels)
    assert isinstance(series, Series)
