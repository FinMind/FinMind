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
    df = data_loader.taiwan_stock_holding_shares_per(
        stock_id="2890", start_date="2021-06-01", end_date="2021-07-03"
    )
    df["labels"] = df["HoldingSharesLevel"]
    df["series"] = df["percent"]
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
