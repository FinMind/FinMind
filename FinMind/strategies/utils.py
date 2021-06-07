import datetime

import numpy as np

from FinMind.data import DataLoader


def get_asset_underlying_type(stock_id: str, data_loader: DataLoader) -> str:
    taiwan_stock_info = data_loader.get_data(dataset="TaiwanStockInfo", date="")
    underlying_type = taiwan_stock_info[
        taiwan_stock_info["stock_id"] == stock_id
    ]["industry_category"].values[0]
    return underlying_type


def get_underlying_trading_tax(underlying_type: str) -> float:
    mapping = {"ETF": 0.001, "上櫃指數股票型基金(ETF)": 0.001}
    return mapping.get(underlying_type, 0.003)


def calculate_datenbr(day1: str, day2: str) -> int:
    assert day1 <= day2, "day2 必須大於等於 day1"

    dis_day = datetime.datetime.strptime(
        day2, "%Y-%m-%d"
    ) - datetime.datetime.strptime(day1, "%Y-%m-%d")
    return int(dis_day.days)


def calculate_sharp_ratio(strategy_return: float, std: float) -> float:
    risk_free_rate = 0
    return (
        0
        if std == 0
        else round(((strategy_return - risk_free_rate) / std) * np.sqrt(252), 2)
    )


def period_return2annual_return(
    period_return: float, period_years: float
) -> float:
    annual_return = round(
        ((period_return + 1) ** (1 / period_years) - 1),
        4,
    )
    return annual_return


def days2years(days: int) -> float:
    return days / 365
