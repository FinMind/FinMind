import os

import pandas as pd
import pytest

from FinMind.data import DataLoader
from FinMind.data import FinMindApi

user_id = os.environ.get("FINMIND_USER", "")
password = os.environ.get("FINMIND_PASSWORD", "")


@pytest.fixture(scope="module")
def api():
    api = FinMindApi()
    api.login(user_id, password)
    return api


def test_api_data(api):
    dataset = "TaiwanStockPrice"
    data_id = "2330"
    start_date = "2020-03-10"
    end_date = "2020-03-15"
    data = api.get_data(
        dataset=dataset,
        data_id=data_id,
        start_date=start_date,
        end_date=end_date,
    )
    assert all(
        data
        == pd.DataFrame(
            {
                "date": [
                    "2020-03-10",
                    "2020-03-11",
                    "2020-03-12",
                    "2020-03-13",
                ],
                "stock_id": ["2330", "2330", "2330", "2330"],
                "Trading_Volume": [74869130, 64923710, 114173351, 151268148],
                "Trading_money": [
                    22727941511,
                    19913151529,
                    33544278206,
                    42448997546,
                ],
                "open": [301.5, 309.0, 299.0, 275.0],
                "max": [309.0, 310.5, 299.0, 294.0],
                "min": [301.0, 302.0, 287.0, 272.5],
                "close": [307.0, 302.0, 294.0, 290.0],
                "spread": [1.5, -5.0, -8.0, -4.0],
                "Trading_turnover": [30268, 27176, 56989, 71990],
            }
        )
    )


def test_get_datalist(api):
    dataset = "TaiwanExchangeRate"
    data = api.get_datalist(dataset)
    assert data == [
        "AUD",
        "CAD",
        "CHF",
        "CNY",
        "EUR",
        "GBP",
        "HKD",
        "IDR",
        "JPY",
        "KRW",
        "MYR",
        "NZD",
        "PHP",
        "SEK",
        "SGD",
        "THB",
        "USD",
        "VND",
        "ZAR",
    ]


def test_translation(api):
    dataset = "TaiwanStockShareholding"
    data = api.translation(dataset=dataset)
    assert all(
        data
        == pd.DataFrame(
            {
                "name": [
                    "外資及陸資共用法令投資上限比率",
                    "外資尚可投資股數",
                    "全體外資持有股數",
                    "法令投資上限比率",
                    "與前日異動原因(註)",
                    "發行股數",
                    "最近一次上櫃公司申報外資持股異動日期",
                    "證券代號",
                    "證券名稱",
                ],
                "english": [
                    "ChineseInvestmentUpperLimitRatio",
                    "ForeignInvestmentRemainingShares",
                    "ForeignInvestmentShares",
                    "ForeignInvestmentUpperLimitRatio",
                    "note",
                    "NumberOfSharesIssued",
                    "RecentlyDeclareDate",
                    "stock_id",
                    "stock_name",
                ],
            }
        )
    )


@pytest.fixture(scope="module")
def data_loader():
    data_loader = DataLoader()
    data_loader.login(user_id, password)
    return data_loader


def test_api_login():
    api = FinMindApi()
    assert api.login(user_id, password)


def assert_data(data: pd.DataFrame, correct_columns_name: list):
    errors = []
    if not all(data.columns == correct_columns_name):
        errors.append("data columns mismatch")
    if not len(data) > 0:
        errors.append("data is empty")
    assert not errors, "errors :\n    {}".format("\n".join(errors))


def test_taiwan_stock_info(data_loader):
    stock_info = data_loader.taiwan_stock_info()
    assert_data(
        stock_info,
        ["industry_category", "stock_id", "stock_name", "type", "date"],
    )


def test_taiwan_stock_daily(data_loader):
    stock_price = data_loader.taiwan_stock_daily(
        "2330", "2018-01-01", "2021-03-06"
    )
    assert_data(
        stock_price,
        [
            "date",
            "stock_id",
            "Trading_Volume",
            "Trading_money",
            "open",
            "max",
            "min",
            "close",
            "spread",
            "Trading_turnover",
        ],
    )


def test_taiwan_stock_daily_adj(data_loader):
    stock_id = "2330"
    start_date = "2019-04-01"
    end_date = "2021-03-06"
    data = data_loader.taiwan_stock_daily_adj(
        stock_id=stock_id, start_date=start_date, end_date=end_date
    ).iloc[0][["open", "close", "max", "min"]]

    assert all(
        data
        == pd.Series(
            {"open": 231.35, "close": 228.11, "max": 231.35, "min": 228.11}
        )
    )


def test_taiwan_stock_daily_adj_2(data_loader):
    stock_id = "3288"
    start_date = "2005-01-01"
    end_date = "2021-05-28"
    df_size = data_loader.taiwan_stock_daily_adj(
        stock_id=stock_id, start_date=start_date, end_date=end_date
    ).size

    assert df_size == 36990


def test_taiwan_stock_daily_adj_empty_dataframe(data_loader):
    stock_id = "1230"
    start_date = "2015-01-01"
    end_date = "2021-06-19"
    df_size = data_loader.taiwan_stock_daily_adj(
        stock_id=stock_id, start_date=start_date, end_date=end_date
    ).size

    assert df_size == 0


def test_taiwan_stock_tick(data_loader):
    data = data_loader.taiwan_stock_tick("2330", "2021-04-01")
    assert_data(
        data, ["date", "stock_id", "deal_price", "volume", "Time", "TickType"]
    )


def test_taiwan_stock_tick_timely(data_loader):
    data = data_loader.taiwan_stock_tick_timely("2330")
    assert_data(
        data, ["date", "stock_id", "deal_price", "volume", "Time", "TickType"]
    )


def test_taiwan_stock_bid_ask(data_loader):
    data = data_loader.taiwan_stock_bid_ask("2330", "2021-04-01")
    assert_data(
        data,
        [
            "stock_id",
            "AskPrice",
            "AskVolume",
            "BidPrice",
            "BidVolume",
            "Time",
            "date",
        ],
    )


# def test_taiwan_stock_bid_ask_timely(data_loader):
#     data = data_loader.taiwan_stock_bid_ask_timely("2330")
#     assert_data(data,
#                 ['stock_id', 'AskPrice', 'AskVolume', 'BidPrice', 'BidVolume',
#                  'Time',
#                  'date'])


def test_taiwan_stock_book_and_trade(data_loader):
    data = data_loader.taiwan_stock_book_and_trade("2021-04-01")
    assert_data(
        data,
        [
            "Time",
            "TotalBuyOrder",
            "TotalBuyVolume",
            "TotalSellOrder",
            "TotalSellVolume",
            "TotalDealOrder",
            "TotalDealVolume",
            "TotalDealMoney",
            "date",
        ],
    )


def test_taiwan_stock_day_trading(data_loader):
    data = data_loader.taiwan_stock_day_trading(
        "2330", "2020-04-02", "2020-04-12"
    )
    assert_data(
        data,
        [
            "stock_id",
            "date",
            "BuyAfterSale",
            "Volume",
            "BuyAmount",
            "SellAmount",
        ],
    )


def test_taiwan_stock_per_pbr(data_loader):
    data = data_loader.taiwan_stock_per_pbr("2330", "2020-04-02")
    assert_data(data, ["date", "stock_id", "dividend_yield", "PER", "PBR"])


def test_taiwan_stock_margin_purchase_short_sale(data_loader):
    data = data_loader.taiwan_stock_margin_purchase_short_sale(
        "2330", "2020-04-02"
    )
    assert_data(
        data,
        [
            "date",
            "stock_id",
            "MarginPurchaseBuy",
            "MarginPurchaseCashRepayment",
            "MarginPurchaseLimit",
            "MarginPurchaseSell",
            "MarginPurchaseTodayBalance",
            "MarginPurchaseYesterdayBalance",
            "Note",
            "OffsetLoanAndShort",
            "ShortSaleBuy",
            "ShortSaleCashRepayment",
            "ShortSaleLimit",
            "ShortSaleSell",
            "ShortSaleTodayBalance",
            "ShortSaleYesterdayBalance",
        ],
    )


def test_taiwan_stock_margin_purchase_short_sale_total(data_loader):
    data = data_loader.taiwan_stock_margin_purchase_short_sale_total(
        "2020-04-02"
    )
    assert_data(
        data,
        [
            "TodayBalance",
            "YesBalance",
            "buy",
            "date",
            "name",
            "Return",
            "sell",
        ],
    )


def test_taiwan_stock_institutional_investors(data_loader):
    data = data_loader.taiwan_stock_institutional_investors(
        "2330", "2020-04-02"
    )
    assert_data(data, ["date", "stock_id", "buy", "name", "sell"])


def test_taiwan_stock_institutional_investors_total(data_loader):
    data = data_loader.taiwan_stock_institutional_investors_total("2020-04-02")
    assert_data(data, ["buy", "date", "name", "sell"])


def test_taiwan_stock_shareholding(data_loader):
    data = data_loader.taiwan_stock_shareholding("2330", "2020-04-02")
    assert_data(
        data,
        [
            "date",
            "stock_id",
            "stock_name",
            "InternationalCode",
            "ForeignInvestmentRemainingShares",
            "ForeignInvestmentShares",
            "ForeignInvestmentRemainRatio",
            "ForeignInvestmentSharesRatio",
            "ForeignInvestmentUpperLimitRatio",
            "ChineseInvestmentUpperLimitRatio",
            "NumberOfSharesIssued",
            "RecentlyDeclareDate",
            "note",
        ],
    )


def test_taiwan_stock_securities_lending(data_loader):
    data = data_loader.taiwan_stock_securities_lending("2330", "2020-04-02")
    assert_data(
        data,
        [
            "date",
            "stock_id",
            "transaction_type",
            "volume",
            "fee_rate",
            "close",
            "original_return_date",
            "original_lending_period",
        ],
    )


def test_taiwan_stock_financial_statement_date(data_loader):
    data = data_loader.taiwan_stock_financial_statement(
        stock_id="2330", start_date="2020-01-01", end_date="2021-04-01"
    )
    assert_data(
        data,
        ["date", "stock_id", "type", "value", "origin_name"],
    )


def test_taiwan_stock_financial_statement_quarter(data_loader):
    data = data_loader.taiwan_stock_financial_statement(
        stock_id="2330", start_date="2020-Q1", end_date="2021-Q1"
    )
    assert_data(
        data,
        ["date", "stock_id", "type", "value", "origin_name"],
    )


def test_taiwan_stock_balance_sheet_date(data_loader):
    data = data_loader.taiwan_stock_balance_sheet(
        stock_id="2330", start_date="2020-01-01", end_date="2021-04-01"
    )
    assert_data(
        data,
        ["date", "stock_id", "type", "value", "origin_name"],
    )


def test_taiwan_stock_balance_sheet_quarter(data_loader):
    data = data_loader.taiwan_stock_balance_sheet(
        stock_id="2330", start_date="2020-Q1", end_date="2021-Q1"
    )
    assert_data(
        data,
        ["date", "stock_id", "type", "value", "origin_name"],
    )


def test_taiwan_stock_cash_flows_statement_date(data_loader):
    data = data_loader.taiwan_stock_cash_flows_statement(
        stock_id="2330", start_date="2020-01-01", end_date="2021-04-01"
    )
    assert_data(
        data,
        ["date", "stock_id", "type", "value", "origin_name"],
    )


def test_taiwan_stock_cash_flows_statement_quarter(data_loader):
    data = data_loader.taiwan_stock_cash_flows_statement(
        stock_id="2330", start_date="2020-Q1", end_date="2021-Q1"
    )
    assert_data(
        data,
        ["date", "stock_id", "type", "value", "origin_name"],
    )


def test_taiwan_stock_month_revenue_date(data_loader):
    data = data_loader.taiwan_stock_month_revenue(
        stock_id="2330", start_date="2020-01-01", end_date="2021-06-01"
    )
    assert_data(
        data,
        [
            "date",
            "stock_id",
            "country",
            "revenue",
            "revenue_month",
            "revenue_year",
        ],
    )


def test_taiwan_stock_month_revenue_month(data_loader):
    data = data_loader.taiwan_stock_month_revenue(
        stock_id="2330", start_date="2020-1M", end_date="2021-1M"
    )
    assert_data(
        data,
        [
            "date",
            "stock_id",
            "country",
            "revenue",
            "revenue_month",
            "revenue_year",
        ],
    )


def test_taiwan_stock_total_return_index(data_loader):
    data = data_loader.taiwan_stock_total_return_index(
        index_id="TAIEX", start_date="2020-01-01", end_date="2021-01-01"
    )
    assert_data(
        data,
        [
            "price",
            "index_id",
            "date",
        ],
    )
