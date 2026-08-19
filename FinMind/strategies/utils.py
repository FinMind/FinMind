import datetime

import numpy as np

from FinMind.data import DataLoader


# TaiwanStockInfo 對部分上市股票會回超過一列，industry_category 不只放產業別：
#   電子工業 / 化學生技醫療 是 TWSE 類股選單裡的「產業總稱」，各自是底下子類的
#     聯集（電子工業 = 半導體業~其他電子業、化學生技醫療 = 化學工業+生技醫療業），
#     所以 2330 會同時有「半導體業」和「電子工業」兩列
#   創新板股票 是板別不是產業，該檔在自己的產業別也還有一列
#   創新版股票 是舊資料的錯字（板 vs 版）
# 直接取第一列會因為回傳順序而不穩定，先把這些非產業別的值排掉。
NOT_INDUSTRY_CATEGORY = [
    "電子工業",
    "化學生技醫療",
    "創新板股票",
    "創新版股票",
]


def get_asset_underlying_type(stock_id: str, data_loader: DataLoader) -> str:
    taiwan_stock_info = data_loader.taiwan_stock_info()
    industry_category = taiwan_stock_info[
        taiwan_stock_info["stock_id"] == stock_id
    ]["industry_category"]
    real_industry_category = industry_category[
        ~industry_category.isin(NOT_INDUSTRY_CATEGORY)
    ]
    # 全部都被排掉時（例如只收到總稱那列）就退回原本的值，寧可回總稱也不要回空
    if len(real_industry_category) > 0:
        industry_category = real_industry_category
    # 排序後取第一個，確保同一檔股票每次都回一樣的結果
    return sorted(industry_category.values)[0]


# ETF 的證交稅是 0.1%，一般股票是 0.3%。TaiwanStockInfo 對上櫃 ETF 的
# industry_category 有「上櫃指數股票型基金(ETF)」與「上櫃ETF」兩種寫法，
# 同一檔可能只出現其中一種，兩種都要對應到 ETF 稅率。
UNDERLYING_TRADING_TAX = {
    "ETF": 0.001,
    "上櫃指數股票型基金(ETF)": 0.001,
    "上櫃ETF": 0.001,
}


def get_underlying_trading_tax(underlying_type: str) -> float:
    return UNDERLYING_TRADING_TAX.get(underlying_type, 0.003)


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
