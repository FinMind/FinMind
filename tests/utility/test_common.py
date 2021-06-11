from FinMind.utility.common import (
    quarter2date,
    is_quarter,
    month2date,
    is_month,
)
import pytest


testdata_quarter2date = [
    ("2021-Q1", "2021-03-31"),
    ("2021-q1", "2021-03-31"),
    ("2021-Q2", "2021-06-30"),
    ("2021-q2", "2021-06-30"),
    ("2021-Q3", "2021-09-30"),
    ("2021-q3", "2021-09-30"),
    ("2021-Q4", "2021-12-31"),
    ("2021-q4", "2021-12-31"),
]


@pytest.mark.parametrize(
    "date, expected",
    testdata_quarter2date,
)
def test_quarter2date(date, expected):
    result = quarter2date(date)
    assert result == expected


testdata_is_quarter = [
    ("2021-Q1", True),
    ("2021-q1", True),
    ("2021-01-01", False),
]


@pytest.mark.parametrize(
    "date, expected",
    testdata_is_quarter,
)
def test_is_quarter(date, expected):
    result = is_quarter(date)
    assert result == expected


testdata_month2date = [
    ("2021-M1", "2021-02-01"),
    ("2021-m1", "2021-02-01"),
    ("2021-M2", "2021-03-01"),
    ("2021-m2", "2021-03-01"),
    ("2021-M12", "2022-01-01"),
    ("2021-m12", "2022-01-01"),
]


@pytest.mark.parametrize(
    "date, expected",
    testdata_month2date,
)
def test_month2date(date, expected):
    result = month2date(date)
    assert result == expected


testdata_is_month = [
    ("2021-M1", True),
    ("2021-m1", True),
    ("2021-01-01", False),
]


@pytest.mark.parametrize(
    "date, expected",
    testdata_is_month,
)
def test_is_month(date, expected):
    result = is_month(date)
    assert result == expected
