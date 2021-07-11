import typing

import pandas as pd

from FinMind.data.finmind_api import FinMindApi
from FinMind.schema.data import Dataset


class DataLoader(FinMindApi):
    def __init__(self):
        super(DataLoader, self).__init__()
        self.feature = Feature(self)

    def taiwan_stock_info(self) -> pd.DataFrame:
        """get 台股總覽
        :return: 台股總覽 TaiwanStockInfo
        :rtype pd.DataFrame
        :rtype column industry_category (str)
        :rtype column stock_id (str)
        :rtype column stock_name (str)
        :rtype column type (str)
        """
        stock_info = self.get_data(dataset=Dataset.TaiwanStockInfo)
        return stock_info

    def taiwan_stock_daily(
        self, stock_id: str = "", start_date: str = "", end_date: str = ""
    ) -> pd.DataFrame:
        """get 台灣股價資料表
        :param stock_id (str): 股票代號("2330")
        :param start_date (str): 開始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")

        :return: 台灣股價資料表 TaiwanStockPrice
        :rtype pd.DataFrame
        :rtype column date (str)
        :rtype column stock_id (str)
        :rtype column Trading_Volume (int)
        :rtype column Trading_money (int)
        :rtype column open (float)
        :rtype column max (float)
        :rtype column min (float)
        :rtype column close (float)
        :rtype column spread (float)
        :rtype column Trading_turnover (float)
        """
        stock_price = self.get_data(
            dataset=Dataset.TaiwanStockPrice,
            data_id=stock_id,
            start_date=start_date,
            end_date=end_date,
        )
        return stock_price

    def taiwan_stock_daily_adj(
        self, stock_id: str, start_date: str, end_date: str
    ) -> pd.DataFrame:
        """get 還原股價
        :param stock_id (str):stock_id: 股票代號("2330")
        :param start_date (str): 開始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")
        :return: 還原股價
        :rtype pd.DataFrame
        :rtype date datetime64[ns])
        :rtype stock_id (str)
        :rtype Trading_Volume (float)
        :rtype Trading_money (float)
        :rtype open (float)
        :rtype max (float)
        :rtype min (float)
        :rtype close (float)
        :rtype spread (float)
        :rtype Trading_turnover (float)
        """
        stock_price = self.taiwan_stock_daily(
            stock_id=stock_id,
            start_date=start_date,
            end_date=end_date,
        )
        if stock_price.empty:
            return stock_price

        stock_price = stock_price[stock_price.close != 0]
        ex_dividend_price = self.taiwan_stock_dividend_result(
            stock_id=stock_id,
            start_date=start_date,
            end_date=end_date,
        )
        if len(ex_dividend_price) == 0:
            return stock_price

        ex_dividend_price = ex_dividend_price[
            ["date", "stock_and_cache_dividend"]
        ]
        stock_price["date"] = pd.to_datetime(stock_price["date"])
        ex_dividend_price["date"] = pd.to_datetime(ex_dividend_price["date"])
        stock_price["change"] = stock_price["close"].pct_change(periods=1)
        ex_dividend_price = ex_dividend_price.iloc[::-1].reset_index(drop=True)
        stock_price = stock_price.iloc[::-1].reset_index(drop=True)
        stock_price["retroactive_open"] = stock_price["open"]
        stock_price["retroactive_max"] = stock_price["max"]
        stock_price["retroactive_min"] = stock_price["min"]
        stock_price["retroactive_close"] = stock_price["close"]
        stock_price["retroactive_change"] = stock_price["change"]
        for index, data in ex_dividend_price.iterrows():
            ex_dividend_date = data["date"]
            ex_dividend_date_y1 = stock_price[
                stock_price["date"] <= ex_dividend_date
            ].iloc[1][0]
            calibration_price = (
                stock_price[stock_price["date"] == ex_dividend_date_y1][
                    "retroactive_close"
                ].iloc[0]
                - data["stock_and_cache_dividend"]
            )

            stock_price.loc[
                stock_price["date"] == ex_dividend_date_y1,
                ["retroactive_close"],
            ] = calibration_price
            calibration_change = (
                stock_price[stock_price["date"] >= ex_dividend_date][
                    "retroactive_close"
                ].iloc[-1]
                - calibration_price
            ) / calibration_price
            stock_price.loc[
                stock_price["date"] == ex_dividend_date, ["retroactive_change"]
            ] = calibration_change
        for i in range(len(stock_price)):
            stock_price.loc[i + 1, "retroactive_close"] = stock_price.loc[
                i, "retroactive_close"
            ] / (1 + stock_price.loc[i, "retroactive_change"])
            stock_price.loc[i, "retroactive_open"] = stock_price.loc[
                i, "retroactive_close"
            ] * (
                1
                + (stock_price.loc[i, "open"] - stock_price.loc[i, "close"])
                / stock_price.loc[i, "close"]
            )
            stock_price.loc[i, "retroactive_max"] = stock_price.loc[
                i, "retroactive_close"
            ] * (
                1
                + (stock_price.loc[i, "max"] - stock_price.loc[i, "close"])
                / stock_price.loc[i, "close"]
            )
            stock_price.loc[i, "retroactive_min"] = stock_price.loc[
                i, "retroactive_close"
            ] * (
                1
                + (stock_price.loc[i, "min"] - stock_price.loc[i, "close"])
                / stock_price.loc[i, "close"]
            )
        stock_price["open"] = stock_price["retroactive_open"].round(2)
        del stock_price["retroactive_open"]
        stock_price["max"] = stock_price["retroactive_max"].round(2)
        del stock_price["retroactive_max"]
        stock_price["min"] = stock_price["retroactive_min"].round(2)
        del stock_price["retroactive_min"]
        stock_price["close"] = stock_price["retroactive_close"].round(2)
        del stock_price["retroactive_close"]
        del stock_price["change"]
        del stock_price["retroactive_change"]
        stock_price["spread"] = stock_price["close"] - stock_price[
            "close"
        ].shift(-1)
        stock_price = stock_price.dropna()
        stock_price = stock_price.iloc[::-1].reset_index(drop=True)
        stock_price["date"] = stock_price["date"].astype(str)
        return stock_price

    def taiwan_stock_tick(self, stock_id: str, date: str) -> pd.DataFrame:
        """get 台灣股價歷史逐筆資料表 TaiwanStockPriceTick
        :param stock_id (str): 股票代號("2330")
        :param date (str): 資料日期 ("2021-03-06")

        :return: 台灣股價歷史逐筆資料表 TaiwanStockPriceTick
        :rtype pd.DataFrame
        :rtype column date (str)
        :rtype column stock_id (str)
        :rtype column deal_price (float)
        :rtype column volume (int)
        """
        stock_tick = self.get_data(
            dataset=Dataset.TaiwanStockPriceTick,
            data_id=stock_id,
            start_date=date,
        )
        return stock_tick

    def taiwan_stock_tick_timely(
        self, stock_id: str, streaming_all_data: bool = False
    ) -> pd.DataFrame:
        """get 台灣股價即時資料表 top 100
        :param stock_id (str): 股票代號("2330")
        :param streaming_all_data (bool): 是否拿取當天所有即時資料

        :return: 台灣股價即時資料表 top 100 TaiwanStockPriceTick
        :rtype pd.DataFrame
        :rtype column date (str)
        :rtype column stock_id (str)
        :rtype column deal_price (float)
        :rtype column volume (int)
        """
        stock_tick = self.get_data(
            dataset=Dataset.TaiwanStockPriceTick,
            data_id=stock_id,
            streaming_all_data=streaming_all_data,
        )
        return stock_tick

    def taiwan_stock_bid_ask(self, stock_id: str, date: str) -> pd.DataFrame:
        """get 歷史台股最佳五檔
        :param stock_id (str): 股票代號("2330")
        :param date (str): 資料日期 ("2021-03-06")

        :return: 歷史台股最佳五檔 TaiwanStockPriceBidAsk
        :rtype pd.DataFrame
        :rtype column stock_id (str)
        :rtype column AskPrice (List[float])
        :rtype column AskVolume (List[int])
        :rtype column BidPrice (List[float])
        :rtype column BidVolume (List[int])
        :rtype column Time (str)
        """
        bid_ask = self.get_data(
            dataset=Dataset.TaiwanStockPriceBidAsk,
            data_id=stock_id,
            start_date=date,
        )
        return bid_ask

    def taiwan_stock_bid_ask_timely(self, stock_id: str) -> pd.DataFrame:
        """get 台股即時最佳五檔 top 100
        :param stock_id (str): 股票代號("2330")

        :return: 台股即時最佳五檔 top 100 TaiwanStockPriceBidAsk
        :rtype pd.DataFrame
        :rtype column stock_id (str)
        :rtype column AskPrice (List[float])
        :rtype column AskVolume (List[int])
        :rtype column BidPrice (List[float])
        :rtype column BidVolume (List[int])
        :rtype column Time (str)
        :rtype column date (str)
        """
        bid_ask = self.get_data(
            dataset=Dataset.TaiwanStockPriceBidAsk,
            data_id=stock_id,
        )
        return bid_ask

    def taiwan_stock_per_pbr(
        self, stock_id: str = "", start_date: str = "", end_date: str = ""
    ) -> pd.DataFrame:
        """get 個股 PER、PBR 資料
        :param stock_id (str): 股票代號("2330")
        :param start_date (str): 起始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")

        :return: 個股 PER、PBR 資料表 TaiwanStockPER
        :rtype pd.DataFrame
        :rtype column date (str)
        :rtype column stock_id (str)
        :rtype column dividend_yield (float)
        :rtype column PER (float)
        :rtype column PBR (float)
        """
        stock_per_pbr = self.get_data(
            dataset=Dataset.TaiwanStockPER,
            data_id=stock_id,
            start_date=start_date,
            end_date=end_date,
        )
        return stock_per_pbr

    def taiwan_stock_book_and_trade(self, date: str) -> pd.DataFrame:
        """get 每 5 秒委託成交統計
        :param date (str): 資料日期 ("2021-03-06")

        :return: 每 5 秒委託成交統計 TaiwanStockStatisticsOfOrderBookAndTrade
        :rtype pd.DataFrame
        :rtype column Time (str)
        :rtype column TotalBuyOrder (int)
        :rtype column TotalBuyVolume (int)
        :rtype column TotalSellOrder (int)
        :rtype column TotalSellVolume (int)
        :rtype column TotalDealOrder (int)
        :rtype column TotalDealVolume (int)
        :rtype column TotalDealMoney (int)
        :rtype column date (str)
        """
        stock_book_and_trade = self.get_data(
            dataset=Dataset.TaiwanStockStatisticsOfOrderBookAndTrade,
            start_date=date,
        )
        return stock_book_and_trade

    def tse(self, date: str) -> pd.DataFrame:
        """get 加權指數
        :param start_date (str): 日期("2018-01-01")

        :return: 加權指數 TaiwanVariousIndicators5Seconds
        :rtype pd.DataFrame
        :rtype column date (str)
        :rtype column TAIEX (float)
        """
        tse = self.get_data(
            dataset=Dataset.TaiwanVariousIndicators5Seconds,
            start_date=date,
        )
        return tse

    def taiwan_stock_day_trading(
        self, stock_id: str = "", start_date: str = "", end_date: str = ""
    ) -> pd.DataFrame:
        """get 當日沖銷交易標的及成交量值
        :param stock_id (str): 股票代號("2330")
        :param start_date (str): 開始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")

        :return: 當日沖銷交易標的及成交量值 TaiwanStockDayTrading
        :rtype pd.DataFrame
        :rtype column stock_id (str)
        :rtype column date (str)
        :rtype column BuyAfterSale (str)
        :rtype column Volume (int)
        :rtype column BuyAmount (int)
        :rtype column SellAmount (int)
        """
        stock_day_trading = self.get_data(
            dataset=Dataset.TaiwanStockDayTrading,
            data_id=stock_id,
            start_date=start_date,
            end_date=end_date,
        )
        return stock_day_trading

    def taiwan_stock_margin_purchase_short_sale(
        self, stock_id: str = "", start_date: str = "", end_date: str = ""
    ) -> pd.DataFrame:
        """get 個股融資融劵表
        :param stock_id (str): 股票代號("2330")
        :param start_date (str): 起始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")

        :return: 個股融資融劵表 TaiwanStockMarginPurchaseShortSale
        :rtype pd.DataFrame
        :rtype column date (str)
        :rtype column stock_id (str)
        :rtype column MarginPurchaseBuy (int)
        :rtype column MarginPurchaseCashRepayment (int)
        :rtype column MarginPurchaseLimit (int)
        :rtype column MarginPurchaseSell (int)
        :rtype column MarginPurchaseTodayBalance (int)
        :rtype column MarginPurchaseYesterdayBalance (int)
        :rtype column Note (str)
        :rtype column OffsetLoanAndShort (int)
        :rtype column ShortSaleBuy (int)
        :rtype column ShortSaleCashRepayment (int)
        :rtype column ShortSaleLimit (int)
        :rtype column ShortSaleSell (int)
        :rtype column ShortSaleTodayBalance (int)
        :rtype column ShortSaleYesterdayBalance (int)
        """
        stock_margin = self.get_data(
            dataset=Dataset.TaiwanStockMarginPurchaseShortSale,
            data_id=stock_id,
            start_date=start_date,
            end_date=end_date,
        )
        return stock_margin

    def taiwan_stock_margin_purchase_short_sale_total(
        self, start_date: str, end_date: str = ""
    ) -> pd.DataFrame:
        """get 整體市場融資融劵表
        :param start_date (str): 起始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")

        :return: 整體市場融資融劵表 TaiwanStockTotalMarginPurchaseShortSale
        :rtype pd.DataFrame
        :rtype column TodayBalance (int)
        :rtype column YesBalance (int)
        :rtype column buy (int)
        :rtype column date (str)
        :rtype column name (str)
        :rtype column Return (int)
        :rtype column sell (int)
        """
        stock_margin_total = self.get_data(
            dataset=Dataset.TaiwanStockTotalMarginPurchaseShortSale,
            start_date=start_date,
            end_date=end_date,
        )
        return stock_margin_total

    def taiwan_stock_institutional_investors(
        self, stock_id: str = "", start_date: str = "", end_date: str = ""
    ) -> pd.DataFrame:
        """get 個股三大法人買賣表
        :param stock_id (str): 股票代號("2330")
        :param start_date (str): 起始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")

        :return: 個股三大法人買賣表 TaiwanStockInstitutionalInvestorsBuySell
        :rtype pd.DataFrame
        :rtype column date (str)
        :rtype column stock_id (str)
        :rtype column buy (int)
        :rtype column name (str)
        :rtype column sell (int)
        """
        stock_institutional_investors = self.get_data(
            dataset=Dataset.TaiwanStockInstitutionalInvestorsBuySell,
            data_id=stock_id,
            start_date=start_date,
            end_date=end_date,
        )
        return stock_institutional_investors

    def taiwan_stock_institutional_investors_total(
        self, start_date: str, end_date: str = ""
    ) -> pd.DataFrame:
        """get 整體三大市場法人買賣表
        :param start_date (str): 起始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")

        :return: 整體三大市場法人買賣表 TaiwanStockTotalInstitutionalInvestors
        :rtype pd.DataFrame
        :rtype column date (str)
        :rtype column buy (int)
        :rtype column name (str)
        :rtype column sell (int)
        """
        stock_institutional_investors_total = self.get_data(
            dataset=Dataset.TaiwanStockTotalInstitutionalInvestors,
            start_date=start_date,
            end_date=end_date,
        )
        return stock_institutional_investors_total

    def taiwan_stock_shareholding(
        self, stock_id: str = "", start_date: str = "", end_date: str = ""
    ) -> pd.DataFrame:
        """get 外資持股表
        :param stock_id (str): 股票代號("2330")
        :param start_date (str): 起始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")

        :return: 外資持股表 TaiwanStockShareholding
        :rtype pd.DataFrame
        :rtype column date (str)
        :rtype column stock_id (str)
        :rtype column stock_name (str)
        :rtype column InternationalCode (str)
        :rtype column ForeignInvestmentRemainingShares (int)
        :rtype column ForeignInvestmentShares (int)
        :rtype column ForeignInvestmentRemainRatio (float)
        :rtype column ForeignInvestmentSharesRatio (float)
        :rtype column ForeignInvestmentUpperLimitRatio (float)
        :rtype column ChineseInvestmentUpperLimitRatio (float)
        :rtype column NumberOfSharesIssued (int)
        :rtype column RecentlyDeclareDate (str)
        :rtype column note (str)
        """
        stock_shareholding = self.get_data(
            dataset=Dataset.TaiwanStockShareholding,
            data_id=stock_id,
            start_date=start_date,
            end_date=end_date,
        )
        return stock_shareholding

    def taiwan_stock_holding_shares_per(
        self, stock_id: str = "", start_date: str = "", end_date: str = ""
    ) -> pd.DataFrame:
        """get 股權持股分級表
        :param stock_id (str): 股票代號("2330")
        :param start_date (str): 起始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")

        :return: 股權持股分級表 TaiwanStockHoldingSharesPer
        :rtype pd.DataFrame
        :rtype column date (str)
        :rtype column stock_id (str)
        :rtype column HoldingSharesLevel (str)
        :rtype column people (int)
        :rtype column percent (float)
        :rtype column unit (int)
        """
        stock_shareholding_class = self.get_data(
            dataset=Dataset.TaiwanStockHoldingSharesPer,
            data_id=stock_id,
            start_date=start_date,
            end_date=end_date,
        )
        return stock_shareholding_class

    def taiwan_stock_securities_lending(
        self, stock_id: str = "", start_date: str = "", end_date: str = ""
    ) -> pd.DataFrame:
        """get 借券成交明細
        :param stock_id (str): 股票代號("2330")
        :param start_date (str): 起始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")

        :return: 借券成交明細 TaiwanStockSecuritiesLending
        :rtype pd.DataFrame
        :rtype column date (str)
        :rtype column stock_id (str)
        :rtype column transaction_type (str)
        :rtype column volume (int)
        :rtype column fee_rate (float)
        :rtype column close (float)
        :rtype column original_return_date (str)
        :rtype column original_lending_period (int)
        """
        stock_securities_lending = self.get_data(
            dataset=Dataset.TaiwanStockSecuritiesLending,
            data_id=stock_id,
            start_date=start_date,
            end_date=end_date,
        )
        return stock_securities_lending

    def taiwan_daily_short_sale_balances(
        self, stock_id: str = "", start_date: str = "", end_date: str = ""
    ) -> pd.DataFrame:
        """get 借券成交明細
        :param stock_id (str): 股票代號("2330")
        :param start_date (str): 起始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")

        :return: 融券借券賣出 TaiwanDailyShortSaleBalances
        :rtype pd.DataFrame
        :rtype column stock_id (str)
        :rtype column MarginShortSalesPreviousDayBalance (int)
        :rtype column MarginShortSalesShortSales (int)
        :rtype column MarginShortSalesShortCovering (int)
        :rtype column MarginShortSalesStockRedemption (int)
        :rtype column MarginShortSalesCurrentDayBalance (int)
        :rtype column MarginShortSalesQuota (int)
        :rtype column SBLShortSalesPreviousDayBalance (int)
        :rtype column SBLShortSalesShortSales (int)
        :rtype column SBLShortSalesReturns (int)
        :rtype column SBLShortSalesAdjustments (int)
        :rtype column SBLShortSalesCurrentDayBalance (int)
        :rtype column SBLShortSalesQuota (int)
        :rtype column SBLShortSalesShortCovering (int)
        :rtype column date (str)
        """
        short_sale_balances = self.get_data(
            dataset=Dataset.TaiwanDailyShortSaleBalances,
            data_id=stock_id,
            start_date=start_date,
            end_date=end_date,
        )
        return short_sale_balances

    def taiwan_stock_cash_flows_statement(
        self, stock_id: str = "", start_date: str = "", end_date: str = ""
    ) -> pd.DataFrame:
        """get 現金流量表
        :param stock_id (str): 股票代號("2330")
        :param start_date (str): 起始日期: "2018-03-31" or "2021-Q1"
        :param end_date (str): 結束日期 "2021-06-30" or "2021-Q2"

        :return: 現金流量表 TaiwanStockCashFlowsStatement
        :rtype pd.DataFrame
        :rtype column date (str)
        :rtype column stock_id (str)
        :rtype column type (str)
        :rtype column value (float)
        :rtype column origin_name (str)
        """
        stock_cash_flows_statement = self.get_data(
            dataset=Dataset.TaiwanStockCashFlowsStatement,
            data_id=stock_id,
            start_date=str(pd.Period(start_date).asfreq("D", "end")),
            end_date=str(pd.Period(end_date).asfreq("D", "end")),
        )
        return stock_cash_flows_statement

    def taiwan_stock_financial_statement(
        self, stock_id: str = "", start_date: str = "", end_date: str = ""
    ) -> pd.DataFrame:
        """get 綜合損益表
        :param stock_id (str): 股票代號("2330")
        :param start_date (str): 起始日期: "2018-03-31" or "2021-Q1"
        :param end_date (str): 結束日期 "2021-06-30" or "2021-Q2"

        :return: 綜合損益表 TaiwanStockFinancialStatements
        :rtype pd.DataFrame
        :rtype column date (str)
        :rtype column stock_id (str)
        :rtype column type (str)
        :rtype column value (float)
        :rtype column origin_name (str)
        """
        stock_financial_statement = self.get_data(
            dataset=Dataset.TaiwanStockFinancialStatements,
            data_id=stock_id,
            start_date=str(pd.Period(start_date).asfreq("D", "end")),
            end_date=str(pd.Period(end_date).asfreq("D", "end")),
        )
        return stock_financial_statement

    def taiwan_stock_balance_sheet(
        self, stock_id: str = "", start_date: str = "", end_date: str = ""
    ) -> pd.DataFrame:
        """get 資產負債表
        :param stock_id (str): 股票代號("2330")
        :param start_date (str): 起始日期: "2018-03-31" or "2021-Q1"
        :param end_date (str): 結束日期 "2021-06-30" or "2021-Q2"

        :return: 資產負債表 TaiwanStockBalanceSheet
        :rtype pd.DataFrame
        :rtype column date (str)
        :rtype column stock_id (str)
        :rtype column type (str)
        :rtype column value (float)
        :rtype column origin_name (str)
        """
        stock_balance_sheet = self.get_data(
            dataset=Dataset.TaiwanStockBalanceSheet,
            data_id=stock_id,
            start_date=str(pd.Period(start_date).asfreq("D", "end")),
            end_date=str(pd.Period(end_date).asfreq("D", "end")),
        )
        return stock_balance_sheet

    def taiwan_stock_dividend(
        self, stock_id: str = "", start_date: str = "", end_date: str = ""
    ) -> pd.DataFrame:
        """股利政策表
        :param stock_id (str): 股票代號("2330")
        :param start_date (str): 起始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")

        :return: 股利政策表 TaiwanStockDividend
        :rtype pd.DataFrame
        :rtype column date (str)
        :rtype column stock_id (str)
        :rtype column year (str)
        :rtype column StockEarningsDistribution (float)
        :rtype column StockStatutorySurplus (float)
        :rtype column StockExDividendTradingDate (str)
        :rtype column TotalEmployeeStockDividend (float)
        :rtype column TotalEmployeeStockDividendAmount (float)
        :rtype column RatioOfEmployeeStockDividendOfTotal (float)
        :rtype column RatioOfEmployeeStockDividend (float)
        :rtype column CashEarningsDistribution (float)
        :rtype column CashStatutorySurplus (float)
        :rtype column CashExDividendTradingDate (str)
        :rtype column CashDividendPaymentDate (str)
        :rtype column TotalEmployeeCashDividend (float)
        :rtype column TotalNumberOfCashCapitalIncrease (float)
        :rtype column CashIncreaseSubscriptionRate (float)
        :rtype column CashIncreaseSubscriptionpRrice (float)
        :rtype column RemunerationOfDirectorsAndSupervisors (float)
        :rtype column ParticipateDistributionOfTotalShares (float)
        :rtype column AnnouncementDate (str)
        :rtype column AnnouncementTime (str)
        """
        stock_dividend = self.get_data(
            dataset=Dataset.TaiwanStockDividend,
            data_id=stock_id,
            start_date=start_date,
            end_date=end_date,
        )
        return stock_dividend

    def taiwan_stock_dividend_result(
        self, stock_id: str = "", start_date: str = "", end_date: str = ""
    ) -> pd.DataFrame:
        """get 除權除息結果表
        :param stock_id (str): 股票代號("2330")
        :param start_date (str): 起始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")

        :return: 除權除息結果表 TaiwanStockDividendResult
        :rtype pd.DataFrame
        :rtype column date (str)
        :rtype column stock_id (str)
        :rtype column before_price (float)
        :rtype column after_price (float)
        :rtype column stock_and_cache_dividend (float)
        :rtype column stock_or_cache_dividend (str)
        :rtype column max_price (float)
        :rtype column min_price (float)
        :rtype column open_price (float)
        :rtype column reference_price (float)
        """
        stock_dividend_result = self.get_data(
            dataset=Dataset.TaiwanStockDividendResult,
            data_id=stock_id,
            start_date=start_date,
            end_date=end_date,
        )
        return stock_dividend_result

    def taiwan_stock_month_revenue(
        self, stock_id: str = "", start_date: str = "", end_date: str = ""
    ) -> pd.DataFrame:
        """get 月營收表
        Since the revenue in January,
        the public time is usually only announced in February,
        so the date plus one month
        :param stock_id (str): 股票代號("2330")
        :param start_date (str): 起始日期: "2018-02-01" or "2021-1M"
        :param end_date (str): 結束日期 "2021-03-01" or "2021-2M"

        :return: 月營收表 TaiwanStockMonthRevenue
        :rtype pd.DataFrame
        :rtype column date (str)
        :rtype column stock_id (str)
        :rtype column country (str)
        :rtype column revenue (int)
        :rtype column revenue_month (int)
        :rtype column revenue_year (int)
        """
        stock_month_revenue = self.get_data(
            dataset=Dataset.TaiwanStockMonthRevenue,
            data_id=stock_id,
            start_date=str(
                (
                    pd.Period(start_date).asfreq("M") + pd.offsets.MonthEnd(1)
                ).asfreq("D", "start")
            ),
            end_date=str(
                (
                    pd.Period(end_date).asfreq("M") + pd.offsets.MonthEnd(1)
                ).asfreq("D", "start")
            ),
        )
        return stock_month_revenue

    def taiwan_futopt_tick_info(self) -> pd.DataFrame:
        """get 期貨, 選擇權即時報價總覽
        :return: 期貨, 選擇權即時報價總覽 TaiwanFutOptTickInfo
        :rtype pd.DataFrame
        :rtype column code (str)
        :rtype column callput (str)
        :rtype column date (str)
        :rtype column name (str)
        :rtype column listing_date (str)
        :rtype column update_date (str)
        :rtype column expire_price (float)
        """
        futopt_tick_info = self.get_data(
            dataset=Dataset.TaiwanFutOptTickInfo,
        )
        return futopt_tick_info

    def taiwan_futopt_tick_realtime(self, data_id: str) -> pd.DataFrame:
        """get 期貨, 選擇權即時報價
        :param data_id: 期貨、選擇權代碼("TXFL1")

        :return: 期貨, 選擇權即時報價 TaiwanFutOptTick
        :rtype pd.DataFrame
        :rtype column date (str)
        :rtype column Time (str)
        :rtype column Close (List[float])
        :rtype column Volume (List[int])
        :rtype column futopt_id (str)
        :rtype column TickType (int)
        """
        futopt_tick = self.get_data(
            dataset=Dataset.TaiwanFutOptTick,
            data_id=data_id,
        )
        return futopt_tick

    def taiwan_futopt_daily_info(self) -> pd.DataFrame:
        """get 期貨, 選擇權日成交資訊總覽

        :return: 期貨, 選擇權日成交資訊總覽 TaiwanOptionFutureInfo
        :rtype pd.DataFrame
        :rtype column code (str)
        :rtype column type (str)
        """
        futopt_daily_info = self.get_data(
            dataset=Dataset.TaiwanOptionFutureInfo,
        )
        return futopt_daily_info

    def taiwan_futures_daily(
        self, futures_id: str = "", start_date: str = "", end_date: str = ""
    ) -> pd.DataFrame:
        """get 期貨日成交資訊
        :param futures_id: 期貨代號("TX")
        :param start_date (str): 起始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")

        :return: 期貨日成交資訊 TaiwanFuturesDaily
        :rtype pd.DataFrame
        :rtype column date (str)
        :rtype column future_id (str)
        :rtype column contract_date (str)
        :rtype column open (float)
        :rtype column max (float)
        :rtype column min (float)
        :rtype column close (float)
        :rtype column spread (float)
        :rtype column spread_per (float)
        :rtype column volume (int)
        :rtype column settlement_price (float)
        :rtype column open_interest (int)
        :rtype column trading_session (str)
        """
        futures_daily = self.get_data(
            dataset=Dataset.TaiwanFuturesDaily,
            data_id=futures_id,
            start_date=start_date,
            end_date=end_date,
        )
        return futures_daily

    def taiwan_option_daily(
        self, option_id: str = "", start_date: str = "", end_date: str = ""
    ) -> pd.DataFrame:
        """get 選擇權日成交資訊
        :param option_id: 選擇權代號("TXO")
        :param start_date (str): 起始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")

        :return: 選擇權日成交資訊 TaiwanOptionDaily
        :rtype pd.DataFrame
        :rtype column date (str)
        :rtype column option_id (str)
        :rtype column contract_date (str)
        :rtype column strike_price (float)
        :rtype column call_put (str)
        :rtype column open (float)
        :rtype column max (float)
        :rtype column min (float)
        :rtype column close (float)
        :rtype column volume (int)
        :rtype column settlement_price (float)
        :rtype column open_interest (int)
        :rtype column trading_session (str)
        """
        option_daily = self.get_data(
            dataset=Dataset.TaiwanOptionDaily,
            data_id=option_id,
            start_date=start_date,
            end_date=end_date,
        )
        return option_daily

    def taiwan_futures_tick(self, futures_id: str, date: str) -> pd.DataFrame:
        """get 期貨交易明細表, 資料量超過10萬筆, 需等一段時間
        :param futures_id: 期貨代號("TX")
        :param date (str): 日期("2018-01-01")

        :return: 期貨交易明細表 TaiwanFuturesTick
        :rtype pd.DataFrame
        :rtype column contract_date (str)
        :rtype column date (str)
        :rtype column futures_id (str)
        :rtype column price (float)
        :rtype column volume (int)
        """
        futures_tick = self.get_data(
            dataset=Dataset.TaiwanFuturesTick,
            data_id=futures_id,
            start_date=date,
        )
        return futures_tick

    def taiwan_option_tick(self, option_id: str, date: str) -> pd.DataFrame:
        """get 選擇權交易明細表, 資料量超過10萬筆, 需等一段時間
        :param option_id: 選擇權代號("TXO")
        :param date (str): 日期("2018-01-01")

        :return: 選擇權交易明細表 TaiwanOptionTick
        :rtype pd.DataFrame
        :rtype column ExercisePrice (float)
        :rtype column PutCall (str)
        :rtype column contract_date (str)
        :rtype column date (str)
        :rtype column option_id (str)
        :rtype column price (float)
        :rtype column volume (int)
        """
        option_tick = self.get_data(
            dataset=Dataset.TaiwanOptionTick,
            data_id=option_id,
            start_date=date,
        )
        return option_tick

    def taiwan_futopt_institutional_investors(
        self, data_id: str = "", start_date: str = "", end_date: str = ""
    ) -> pd.DataFrame:
        """get 選擇權, 期貨三大法人買賣
        :param data_id: 期貨, 選擇權代號("TXO")
        :param start_date (str): 起始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")

        :return: 選擇權, 期貨三大法人買賣 TaiwanFutOptInstitutionalInvestors
        :rtype pd.DataFrame
        :rtype column name (str)
        :rtype column date (str)
        :rtype column institutional_investors (str)
        :rtype column long_deal_volume (int)
        :rtype column long_deal_amount (int)
        :rtype column short_deal_volume (int)
        :rtype column short_deal_amount (int)
        :rtype column long_open_interest_balance_volume (int)
        :rtype column long_open_interest_balance_amount (int)
        :rtype column short_open_interest_balance_volume (int)
        :rtype column short_open_interest_balance_amount (int)
        """
        futopt_institutional_investors = self.get_data(
            dataset=Dataset.TaiwanFutOptInstitutionalInvestors,
            data_id=data_id,
            start_date=start_date,
            end_date=end_date,
        )
        return futopt_institutional_investors

    def taiwan_futures_dealer_trading_volume_daily(
        self, futures_id: str = "", start_date: str = "", end_date: str = ""
    ) -> pd.DataFrame:
        """get 期貨各卷商每日交易
        :param futures_id: 期貨代號("TX")
        :param start_date (str): 起始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")

        :return: 期貨各卷商每日交易 TaiwanFuturesDealerTradingVolumeDaily
        :rtype pd.DataFrame
        :rtype column date (str)
        :rtype column dealer_code (str)
        :rtype column dealer_name (str)
        :rtype column futures_id (str)
        :rtype column volume (int)
        :rtype column is_after_hour (str)
        """
        futures_dealer_trading_volume_daily = self.get_data(
            dataset=Dataset.TaiwanFuturesDealerTradingVolumeDaily,
            data_id=futures_id,
            start_date=start_date,
            end_date=end_date,
        )
        return futures_dealer_trading_volume_daily

    def taiwan_option_dealer_trading_volume_daily(
        self, option_id: str = "", start_date: str = "", end_date: str = ""
    ) -> pd.DataFrame:
        """get 選擇權各卷商每日交易
        :param option_id: 選擇權代號("TXO")
        :param start_date (str): 起始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")

        :return: 選擇權各卷商每日交易 TaiwanOptionDealerTradingVolumeDaily
        :rtype pd.DataFrame
        :rtype column date (str)
        :rtype column dealer_code (str)
        :rtype column dealer_name (str)
        :rtype column option_id (str)
        :rtype column volume (int)
        :rtype column is_after_hour (str)
        """
        option_dealer_trading_volume_daily = self.get_data(
            dataset=Dataset.TaiwanOptionDealerTradingVolumeDaily,
            data_id=option_id,
            start_date=start_date,
            end_date=end_date,
        )
        return option_dealer_trading_volume_daily

    def taiwan_stock_news(
        self, stock_id: str = "", start_date: str = "", end_date: str = ""
    ) -> pd.DataFrame:
        """get 相關新聞
        :param stock_id: 股票代號("2330")
        :param start_date (str): 起始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")

        :return: 相關新聞 TaiwanStockNews
        :rtype pd.DataFrame
        :rtype column date (str)
        :rtype column stock_id (str)
        :rtype column description (str)
        :rtype column link (str)
        :rtype column source (str)
        :rtype column title (str)
        """
        stock_news = self.get_data(
            dataset=Dataset.TaiwanStockNews,
            data_id=stock_id,
            start_date=start_date,
            end_date=end_date,
        )
        return stock_news

    def taiwan_stock_total_return_index(
        self, index_id: str = "", start_date: str = "", end_date: str = ""
    ) -> pd.DataFrame:
        """get 加權, 櫃買報酬指數
        :param index_id: index 代號,
            "TAIEX" (發行量加權股價報酬指數),
            "TPEx" (櫃買指數與報酬指數)
        :param start_date (str): 起始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")

        :return: 加權, 櫃買報酬指數 TaiwanStockTotalReturnIndex
        :rtype pd.DataFrame
        :rtype column price (float)
        :rtype column stock_id (str)
        :rtype column date (str)
        """
        stock_total_return_index = self.get_data(
            dataset=Dataset.TaiwanStockTotalReturnIndex,
            data_id=index_id,
            start_date=start_date,
            end_date=end_date,
        )
        stock_total_return_index.columns = stock_total_return_index.columns.map(
            dict(
                price="price",
                stock_id="index_id",
                date="date",
            )
        )
        return stock_total_return_index


class Feature:
    def __init__(self, data_loader: DataLoader):
        self.data_loader = data_loader

    def get_stock_params(
        self,
        stock_data: pd.DataFrame,
    ) -> typing.Tuple[str, str, str]:
        stock_data["date"] = stock_data["date"].astype(str)
        stock_id = stock_data["stock_id"].values[0]
        start_date = min(stock_data["date"])
        end_date = max(stock_data["date"])
        return stock_id, start_date, end_date

    def add_kline_institutional_investors(
        self, stock_data: pd.DataFrame
    ) -> pd.DataFrame:
        stock_id, start_date, end_date = self.get_stock_params(stock_data)
        institutional_investors_df = (
            self.data_loader.taiwan_stock_institutional_investors(
                stock_id=stock_id, start_date=start_date, end_date=end_date
            )
        )
        # 外資
        foreign_investor_df = institutional_investors_df.loc[
            institutional_investors_df["name"] == "Foreign_Investor",
            ["date", "buy", "sell"],
        ]
        foreign_investor_df["Foreign_Investor_diff"] = (
            foreign_investor_df["buy"] - foreign_investor_df["sell"]
        )
        # 投信
        investment_trust_df = institutional_investors_df.loc[
            institutional_investors_df["name"] == "Investment_Trust",
            ["date", "buy", "sell"],
        ]
        investment_trust_df["Investment_Trust_diff"] = (
            investment_trust_df["buy"] - investment_trust_df["sell"]
        )
        foreign_investor_df = foreign_investor_df.drop(["buy", "sell"], axis=1)
        investment_trust_df = investment_trust_df.drop(["buy", "sell"], axis=1)
        stock_data = stock_data.merge(foreign_investor_df, on="date").merge(
            investment_trust_df, on="date"
        )
        return stock_data

    def add_kline_margin_purchase_short_sale(
        self, stock_data: pd.DataFrame
    ) -> pd.DataFrame:
        stock_id, start_date, end_date = self.get_stock_params(stock_data)
        margin_purchase_short_sale_df = (
            self.data_loader.taiwan_stock_margin_purchase_short_sale(
                stock_id=stock_id, start_date=start_date, end_date=end_date
            )
        )
        # 融資
        margin_purchase_df = margin_purchase_short_sale_df[
            ["date", "MarginPurchaseBuy", "MarginPurchaseSell"]
        ].copy()
        margin_purchase_df["Margin_Purchase_diff"] = (
            margin_purchase_df["MarginPurchaseBuy"]
            - margin_purchase_df["MarginPurchaseSell"]
        )
        # 融券
        short_sale_df = margin_purchase_short_sale_df[
            ["date", "ShortSaleBuy", "ShortSaleSell"]
        ].copy()
        short_sale_df["Short_Sale_diff"] = (
            short_sale_df["ShortSaleBuy"] - short_sale_df["ShortSaleSell"]
        )
        margin_purchase_df = margin_purchase_df.drop(
            ["MarginPurchaseBuy", "MarginPurchaseSell"], axis=1
        )
        short_sale_df = short_sale_df.drop(
            ["ShortSaleBuy", "ShortSaleSell"], axis=1
        )
        stock_data = stock_data.merge(margin_purchase_df, on="date").merge(
            short_sale_df, on="date"
        )
        return stock_data
