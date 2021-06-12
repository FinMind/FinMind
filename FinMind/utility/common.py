import datetime
from dateutil.relativedelta import relativedelta


def month2date(month_date: str) -> str:
    year, month = month_date.split("-")
    month = int(month.replace("m", "").replace("M", ""))
    month = str(month).zfill(2)
    date = f"{year}-{month}-01"
    date = str(
        datetime.datetime.strptime(date, "%Y-%m-%d").date()
        + relativedelta(months=1)
    )
    return date


def is_month(date: str) -> str:
    return "M" in date or "m" in date
