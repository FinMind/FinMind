import datetime
from dateutil.relativedelta import relativedelta

QUARTER_DICT = dict(
    q1="03-31",
    Q1="03-31",
    Q2="06-30",
    q2="06-30",
    Q3="09-30",
    q3="09-30",
    Q4="12-31",
    q4="12-31",
)


def quarter2date(quarter_date: str) -> str:
    year, quarter = quarter_date.split("-")
    month_day = QUARTER_DICT.get(quarter)
    return f"{year}-{month_day}"


def is_quarter(date: str) -> str:
    return "Q" in date or "q" in date


def month2date(month_date: str) -> str:
    year, month = month_date.split("-")
    month = int(month.replace("m", "").replace("M", ""))
    month = month if month > 9 else f"0{month}"
    date = f"{year}-{month}-01"
    date = str(
        datetime.datetime.strptime(date, "%Y-%m-%d").date()
        + relativedelta(months=1)
    )
    return date


def is_month(date: str) -> str:
    return "M" in date or "m" in date
