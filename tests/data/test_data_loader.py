import os

import pandas as pd
import pytest

from FinMind.data import DataLoader, FinMindApi

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


def test_taiwan_stock_info_with_warrant(data_loader):
    stock_info = data_loader.taiwan_stock_info_with_warrant()
    assert_data(
        stock_info,
        ["industry_category", "stock_id", "stock_name", "type", "date"],
    )
    assert len(stock_info) > 10000


def test_taiwan_securities_trader_info(data_loader):
    securities_trader_info = data_loader.taiwan_securities_trader_info()
    assert_data(
        securities_trader_info,
        [
            "securities_trader_id",
            "securities_trader",
            "date",
            "address",
            "phone",
        ],
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
    stock_price = data_loader.taiwan_stock_daily_adj(
        stock_id="2330", start_date="2018-01-01", end_date="2021-03-06"
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


def test_taiwan_stock_tick(data_loader):
    data = data_loader.taiwan_stock_tick("2330", "2021-04-01")
    assert_data(
        data, ["date", "stock_id", "deal_price", "volume", "Time", "TickType"]
    )


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


def test_taiwan_stock_government_bank_buy_sell(data_loader):
    data = data_loader.taiwan_stock_government_bank_buy_sell("2023-01-10")
    assert_data(
        data,
        [
            "date",
            "stock_id",
            "buy_amount",
            "sell_amount",
            "buy",
            "sell",
            "bank_name",
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


def test_taiwan_stock_financial_statement_date_no_end_date(data_loader):
    data = data_loader.taiwan_stock_financial_statement(
        stock_id="2330", start_date="2020-01-01"
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


def test_taiwan_stock_balance_sheet_date_no_end_date(data_loader):
    data = data_loader.taiwan_stock_balance_sheet(
        stock_id="2330", start_date="2020-01-01"
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


def test_taiwan_stock_cash_flows_statement_date_no_date(data_loader):
    data = data_loader.taiwan_stock_cash_flows_statement(
        stock_id="2330", start_date="2020-01-01"
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


def test_taiwan_stock_month_revenue_date_no_date(data_loader):
    data = data_loader.taiwan_stock_month_revenue(
        stock_id="2330", start_date="2020-01-01"
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


def test_taiwan_stock_market_value_weight(data_loader):
    data = data_loader.taiwan_stock_market_value_weight(
        stock_id="2330", start_date="2024-01-01", end_date="2025-01-01"
    )
    assert_data(
        data,
        [
            "rank",
            "stock_id",
            "stock_name",
            "weight_per",
            "date",
            "type",
        ],
    )


def test_taiwan_option_institutional_investors(data_loader):
    data = data_loader.taiwan_option_institutional_investors(
        data_id="TXO", start_date="2019-04-03", end_date="2019-04-04"
    )
    assert_data(
        data,
        [
            "option_id",
            "date",
            "call_put",
            "institutional_investors",
            "long_deal_volume",
            "long_deal_amount",
            "short_deal_volume",
            "short_deal_amount",
            "long_open_interest_balance_volume",
            "long_open_interest_balance_amount",
            "short_open_interest_balance_volume",
            "short_open_interest_balance_amount",
        ],
    )


def test_taiwan_futures_institutional_investors(data_loader):
    data = data_loader.taiwan_futures_institutional_investors(
        data_id="TX", start_date="2019-04-03", end_date="2019-04-04"
    )
    assert_data(
        data,
        [
            "futures_id",
            "date",
            "institutional_investors",
            "long_deal_volume",
            "long_deal_amount",
            "short_deal_volume",
            "short_deal_amount",
            "long_open_interest_balance_volume",
            "long_open_interest_balance_amount",
            "short_open_interest_balance_volume",
            "short_open_interest_balance_amount",
        ],
    )


def test_taiwan_option_institutional_investors_after_hours(data_loader):
    data = data_loader.taiwan_option_institutional_investors_after_hours(
        data_id="TXO", start_date="2021-10-12", end_date="2021-11-12"
    )
    assert_data(
        data,
        [
            "option_id",
            "date",
            "call_put",
            "institutional_investors",
            "long_deal_volume",
            "long_deal_amount",
            "short_deal_volume",
            "short_deal_amount",
        ],
    )


def test_taiwan_futures_institutional_investors_after_hours(data_loader):
    data = data_loader.taiwan_futures_institutional_investors_after_hours(
        data_id="TX", start_date="2021-10-12", end_date="2021-11-12"
    )
    assert_data(
        data,
        [
            "futures_id",
            "date",
            "institutional_investors",
            "long_deal_volume",
            "long_deal_amount",
            "short_deal_volume",
            "short_deal_amount",
        ],
    )


def test_taiwan_stock_capital_reduction_reference_price(data_loader):
    data = data_loader.taiwan_stock_capital_reduction_reference_price(
        stock_id="2327", start_date="2000-01-01", end_date="2021-04-01"
    )
    assert_data(
        data,
        [
            "date",
            "stock_id",
            "ClosingPriceonTheLastTradingDay",
            "PostReductionReferencePrice",
            "LimitUp",
            "LimitDown",
            "OpeningReferencePrice",
            "ExrightReferencePrice",
            "ReasonforCapitalReduction",
        ],
    )


def test_taiwan_stock_market_value(data_loader):
    data = data_loader.taiwan_stock_market_value(
        stock_id="2330", start_date="2000-01-01", end_date="2023-06-01"
    )
    assert_data(
        data,
        [
            "date",
            "stock_id",
            "market_value",
        ],
    )


def test_taiwan_stock_10year(data_loader):
    data = data_loader.taiwan_stock_10year(
        stock_id="2330", start_date="2000-01-01", end_date="2023-06-01"
    )
    assert_data(
        data,
        [
            "date",
            "stock_id",
            "close",
        ],
    )


def test_taiwan_stock_weekly(data_loader):
    data = data_loader.taiwan_stock_weekly(
        stock_id="2330", start_date="2000-01-01", end_date="2023-06-01"
    )
    assert_data(
        data,
        [
            "stock_id",
            "yweek",
            "max",
            "min",
            "trading_volume",
            "trading_money",
            "trading_turnover",
            "date",
            "close",
            "open",
            "spread",
        ],
    )


def test_taiwan_stock_monthly(data_loader):
    data = data_loader.taiwan_stock_monthly(
        stock_id="2330", start_date="2000-01-01", end_date="2023-06-01"
    )
    assert_data(
        data,
        [
            "stock_id",
            "ymonth",
            "max",
            "min",
            "trading_volume",
            "trading_money",
            "trading_turnover",
            "date",
            "close",
            "open",
            "spread",
        ],
    )


def test_taiwan_stock_bar(data_loader):
    data = data_loader.taiwan_stock_bar(stock_id="2330", date="2023-01-05")
    assert_data(
        data,
        [
            "date",
            "minute",
            "stock_id",
            "open",
            "high",
            "low",
            "close",
            "volume",
        ],
    )


def test_taiwan_stock_delisting(data_loader):
    data = data_loader.taiwan_stock_delisting(stock_id="1230")
    assert_data(
        data,
        [
            "date",
            "stock_id",
            "stock_name",
        ],
    )


def test_taiwan_total_exchange_margin_maintenance(data_loader):
    data = data_loader.taiwan_total_exchange_margin_maintenance(
        start_date="2024-01-01", end_date="2024-01-20"
    )
    assert_data(
        data,
        [
            "date",
            "TotalExchangeMarginMaintenance",
        ],
    )


def test_us_stock_info(data_loader):
    data = data_loader.us_stock_info()
    assert_data(
        data,
        [
            "date",
            "stock_id",
            "Country",
            "IPOYear",
            "MarketCap",
            "Subsector",
            "stock_name",
        ],
    )


def test_us_stock_price(data_loader):
    data = data_loader.us_stock_price(
        stock_id="VOO", start_date="2023-01-01", end_date="2023-01-31"
    )
    assert_data(
        data,
        [
            "date",
            "stock_id",
            "Adj_Close",
            "Close",
            "High",
            "Low",
            "Open",
            "Volume",
        ],
    )


def test_taiwan_stock_convertible_bond_info(data_loader):
    df = data_loader.taiwan_stock_convertible_bond_info()
    assert_data(
        df,
        [
            "cb_id",
            "cb_name",
            "InitialDateOfConversion",
            "DueDateOfConversion",
            "IssuanceAmount",
        ],
    )


def test_taiwan_stock_convertible_bond_daily(data_loader):
    df = data_loader.taiwan_stock_convertible_bond_daily(
        cb_id="15131",
        start_date="2020-04-01",
        end_date="2020-04-10",
    )
    assert_data(
        df,
        [
            "cb_id",
            "cb_name",
            "transaction_type",
            "close",
            "change",
            "open",
            "max",
            "min",
            "no_of_transactions",
            "unit",
            "trading_value",
            "avg_price",
            "next_ref_price",
            "next_max_limit",
            "next_min_limit",
            "date",
        ],
    )


def test_taiwan_stock_convertible_bond_institutional_investors(data_loader):
    df = data_loader.taiwan_stock_convertible_bond_institutional_investors(
        cb_id="15131",
        start_date="2020-04-01",
        end_date="2020-04-10",
    )
    assert_data(
        df,
        [
            "Foreign_Investor_Buy",
            "Foreign_Investor_Sell",
            "Foreign_Investor_Overbuy",
            "Investment_Trust_Buy",
            "Investment_Trust_Sell",
            "Investment_Trust_Overbuy",
            "Dealer_self_Buy",
            "Dealer_self_Sell",
            "Dealer_self_Overbuy",
            "Total_Overbuy",
            "cb_id",
            "cb_name",
            "date",
        ],
    )


def test_taiwan_stock_convertible_bond_daily_overview(data_loader):
    df = data_loader.taiwan_stock_convertible_bond_daily_overview(
        cb_id="15131",
        start_date="2020-04-01",
        end_date="2020-04-10",
    )
    assert_data(
        df,
        [
            "cb_id",
            "cb_name",
            "date",
            "InitialDateOfConversion",
            "DueDateOfConversion",
            "InitialDateOfStopConversion",
            "DueDateOfStopConversion",
            "ConversionPrice",
            "NextEffectiveDateOfConversionPrice",
            "LatestInitialDateOfPut",
            "LatestDueDateOfPut",
            "LatestPutPrice",
            "InitialDateOfEarlyRedemption",
            "DueDateOfEarlyRedemption",
            "EarlyRedemptionPrice",
            "DateOfDelisted",
            "IssuanceAmount",
            "OutstandingAmount",
            "ReferencePrice",
            "PriceOfUnderlyingStock",
            "InitialDateOfSuspension",
            "DueDateOfSuspension",
            "CouponRate",
        ],
    )


def test_taiwan_stock_margin_short_sale_suspension(data_loader):
    df = data_loader.taiwan_stock_margin_short_sale_suspension(
        stock_id="2330",
        start_date="2020-04-01",
        end_date="2020-04-10",
    )
    assert_data(
        df,
        [
            "stock_id",
            "date",
            "end_date",
            "reason",
        ],
    )


def test_taiwan_stock_trading_daily_report_secid_agg(data_loader):
    df = data_loader.taiwan_stock_trading_daily_report_secid_agg(
        stock_id="2330",
        securities_trader_id="1020",
        start_date="2024-07-30",
        end_date="2024-07-31",
    )
    assert_data(
        df,
        [
            "securities_trader",
            "securities_trader_id",
            "stock_id",
            "date",
            "buy_volume",
            "sell_volume",
            "buy_price",
            "sell_price",
        ],
    )


def test_taiwan_stock_trading_daily_report(data_loader):
    df = data_loader.taiwan_stock_trading_daily_report(
        stock_id="2330",
        securities_trader_id="1020",
        date="2024-07-30",
    )
    assert_data(
        df,
        [
            "securities_trader",
            "price",
            "buy",
            "sell",
            "securities_trader_id",
            "stock_id",
            "date",
        ],
    )


def test_taiwan_futures_open_interest_large_traders(data_loader):
    df = data_loader.taiwan_futures_open_interest_large_traders(
        futures_id="TJF",
        start_date="2024-09-01",
        end_date="2024-09-02",
    )
    assert_data(
        df,
        [
            "name",
            "contract_type",
            "buy_top5_trader_open_interest",
            "buy_top5_trader_open_interest_per",
            "buy_top10_trader_open_interest",
            "buy_top10_trader_open_interest_per",
            "sell_top5_trader_open_interest",
            "sell_top5_trader_open_interest_per",
            "sell_top10_trader_open_interest",
            "sell_top10_trader_open_interest_per",
            "market_open_interest",
            "buy_top5_specific_open_interest",
            "buy_top5_specific_open_interest_per",
            "buy_top10_specific_open_interest",
            "buy_top10_specific_open_interest_per",
            "sell_top5_specific_open_interest",
            "sell_top5_specific_open_interest_per",
            "sell_top10_specific_open_interest",
            "sell_top10_specific_open_interest_per",
            "date",
            "futures_id",
        ],
    )


def test_taiwan_option_open_interest_large_traders(data_loader):
    df = data_loader.taiwan_option_open_interest_large_traders(
        option_id="CA",
        start_date="2024-09-01",
        end_date="2024-09-02",
    )
    assert_data(
        df,
        [
            "contract_type",
            "buy_top5_trader_open_interest",
            "buy_top5_trader_open_interest_per",
            "buy_top10_trader_open_interest",
            "buy_top10_trader_open_interest_per",
            "sell_top5_trader_open_interest",
            "sell_top5_trader_open_interest_per",
            "sell_top10_trader_open_interest",
            "sell_top10_trader_open_interest_per",
            "market_open_interest",
            "buy_top5_specific_open_interest",
            "buy_top5_specific_open_interest_per",
            "buy_top10_specific_open_interest",
            "buy_top10_specific_open_interest_per",
            "sell_top5_specific_open_interest",
            "sell_top5_specific_open_interest_per",
            "sell_top10_specific_open_interest",
            "sell_top10_specific_open_interest_per",
            "date",
            "put_call",
            "name",
            "option_id",
        ],
    )

def test_cnn_fear_greed_index(data_loader):
    df = data_loader.cnn_fear_greed_index(
        start_date="2020-04-01",
        end_date="2020-04-10",
    )
    assert_data(
        df,
        [
            "date",
            "fear_greed",
            "fear_greed_emotion",
            "reason",
        ],
    )