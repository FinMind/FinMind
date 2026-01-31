import typing

import pandas as pd

from FinMind.data.finmind_api import FinMindApi
from FinMind.schema.data import Dataset


class DataLoader(FinMindApi):
    def __init__(self, token: str = ""):
        super(DataLoader, self).__init__(token=token)
        self.login_by_token(api_token=token)
        self.feature = Feature(self)

    def taiwan_stock_info(self, timeout: int = None) -> pd.DataFrame:
        """get 台股總覽
        :param timeout (int): timeout seconds, default None

        :return: 台股總覽 TaiwanStockInfo
        :rtype pd.DataFrame
        :rtype column industry_category (str)
        :rtype column stock_id (str)
        :rtype column stock_name (str)
        :rtype column type (str)
        """
        stock_info = self.get_data(
            dataset=Dataset.TaiwanStockInfo, timeout=timeout
        )
        return stock_info

    def taiwan_stock_info_with_warrant(
        self, timeout: int = None
    ) -> pd.DataFrame:
        """get 台股總覽(包含權證)
        :param timeout (int): timeout seconds, default None

        :return: 台股總覽 TaiwanStockInfoWithWarrant
        :rtype pd.DataFrame
        :rtype column industry_category (str)
        :rtype column stock_id (str)
        :rtype column stock_name (str)
        :rtype column type (str)
        """
        stock_info = self.get_data(
            dataset=Dataset.TaiwanStockInfoWithWarrant, timeout=timeout
        )
        return stock_info

    def taiwan_securities_trader_info(
        self, timeout: int = None
    ) -> pd.DataFrame:
        """get 證券商資訊表
        :param timeout (int): timeout seconds, default None

        :return: 證券商資訊表 TaiwanSecuritiesTraderInfo
        :rtype pd.DataFrame
        :rtype column securities_trader_id (str)
        :rtype column securities_trader (str)
        :rtype column date (str)
        :rtype column address (str)
        :rtype column phone (str)
        """
        securities_trader_info = self.get_data(
            dataset=Dataset.TaiwanSecuritiesTraderInfo, timeout=timeout
        )
        return securities_trader_info

    def taiwan_stock_daily(
        self,
        stock_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
        use_async: bool = False,
        stock_id_list: typing.List[str] = None,
    ) -> pd.DataFrame:
        """get 台灣股價資料表
        :param stock_id (str): 股票代號("2330")
        :param start_date (str): 開始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")
        :param timeout (int): timeout seconds, default None

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
            timeout=timeout,
            use_async=use_async,
            data_id_list=stock_id_list,
        )
        return stock_price

    def taiwan_stock_daily_adj(
        self,
        stock_id: str,
        start_date: str,
        end_date: str,
        timeout: int = None,
        use_async: bool = False,
        stock_id_list: typing.List[str] = None,
    ) -> pd.DataFrame:
        """get 還原股價, 主要採用向前還原
        :param stock_id (str):stock_id: 股票代號("2330")
        :param start_date (str): 開始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")
        :param timeout (int): timeout seconds, default None

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
        stock_price = self.get_data(
            dataset=Dataset.TaiwanStockPriceAdj,
            data_id=stock_id,
            start_date=start_date,
            end_date=end_date,
            timeout=timeout,
            use_async=use_async,
            data_id_list=stock_id_list,
        )
        return stock_price

    def taiwan_stock_tick(
        self,
        stock_id: str = None,
        date: str = "",
        stock_id_list: typing.List[str] = None,
        timeout: int = None,
        use_async: bool = False,
    ) -> pd.DataFrame:
        """get 台灣股價歷史逐筆資料表 TaiwanStockPriceTick
        :param stock_id (str): 股票代號("2330")
        :param date (str): 資料日期 ("2021-03-06")
        :param timeout (int): timeout seconds, default None

        :return: 台灣股價歷史逐筆資料表 TaiwanStockPriceTick
        :rtype pd.DataFrame
        :rtype column date (str)
        :rtype column stock_id (str)
        :rtype column deal_price (float)
        :rtype column volume (int)
        """
        if not stock_id and not stock_id_list:
            stock_id_list = self._get_stock_id_list(date, timeout)

        stock_tick = self.get_data(
            dataset=Dataset.TaiwanStockPriceTick,
            data_id=stock_id,
            data_id_list=stock_id_list,
            start_date=date,
            timeout=timeout,
            use_async=use_async,
        )
        return stock_tick

    def taiwan_stock_per_pbr(
        self,
        stock_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
        use_async: bool = False,
        stock_id_list: typing.List[str] = None,
    ) -> pd.DataFrame:
        """get 個股 PER、PBR 資料
        :param stock_id (str): 股票代號("2330")
        :param start_date (str): 起始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")
        :param timeout (int): timeout seconds, default None

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
            timeout=timeout,
            use_async=use_async,
            data_id_list=stock_id_list,
        )
        return stock_per_pbr

    def taiwan_stock_book_and_trade(
        self, date: str, timeout: int = None
    ) -> pd.DataFrame:
        """get 每 5 秒委託成交統計
        :param date (str): 資料日期 ("2021-03-06")
        :param timeout (int): timeout seconds, default None

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
            timeout=timeout,
        )
        return stock_book_and_trade

    def tse(self, date: str, timeout: int = None) -> pd.DataFrame:
        """get 加權指數
        :param start_date (str): 日期("2018-01-01")
        :param timeout (int): timeout seconds, default None

        :return: 加權指數 TaiwanVariousIndicators5Seconds
        :rtype pd.DataFrame
        :rtype column date (str)
        :rtype column TAIEX (float)
        """
        tse = self.get_data(
            dataset=Dataset.TaiwanVariousIndicators5Seconds,
            start_date=date,
            timeout=timeout,
        )
        return tse

    def taiwan_stock_day_trading(
        self,
        stock_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
        use_async: bool = False,
        stock_id_list: typing.List[str] = None,
    ) -> pd.DataFrame:
        """get 當日沖銷交易標的及成交量值
        :param stock_id (str): 股票代號("2330")
        :param start_date (str): 開始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")
        :param timeout (int): timeout seconds, default None

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
            timeout=timeout,
            use_async=use_async,
            data_id_list=stock_id_list,
        )
        return stock_day_trading

    def taiwan_stock_government_bank_buy_sell(
        self,
        start_date: str = "",
        timeout: int = None,
    ) -> pd.DataFrame:
        """get 當日八大行庫對各股買賣股數和金額
        :param start_date (str): 開始日期("2023-01-10")
        :param end_date (str): 結束日期("2023-01-10")
        :param timeout (int): timeout seconds, default None

        :return: 當日八大行庫對各股買賣股數和金 TaiwanStockGovernmentBankBuySell
        :rtype pd.DataFrame
        :rtype column stock_id (str)
        :rtype column date (str)
        :rtype column buy_amount (int)
        :rtype column sell_amount (int)
        :rtype column buy (int)
        :rtype column sell (int)
        :rtype column bank_name (str)
        """
        stock_government_bank_buy_sell = self.get_data(
            dataset=Dataset.TaiwanStockGovernmentBankBuySell,
            start_date=start_date,
            end_date="",
            timeout=timeout,
        )
        return stock_government_bank_buy_sell

    def taiwan_stock_margin_purchase_short_sale(
        self,
        stock_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
        use_async: bool = False,
        stock_id_list: typing.List[str] = None,
    ) -> pd.DataFrame:
        """get 個股融資融劵表
        :param stock_id (str): 股票代號("2330")
        :param start_date (str): 起始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")
        :param timeout (int): timeout seconds, default None

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
            timeout=timeout,
            use_async=use_async,
            data_id_list=stock_id_list,
        )
        return stock_margin

    def taiwan_stock_margin_purchase_short_sale_total(
        self, start_date: str, end_date: str = "", timeout: int = None
    ) -> pd.DataFrame:
        """get 整體市場融資融劵表
        :param start_date (str): 起始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")
        :param timeout (int): timeout seconds, default None

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
            timeout=timeout,
        )
        return stock_margin_total

    def taiwan_stock_institutional_investors(
        self,
        stock_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
        use_async: bool = False,
        stock_id_list: typing.List[str] = None,
    ) -> pd.DataFrame:
        """get 個股三大法人買賣表
        :param stock_id (str): 股票代號("2330")
        :param start_date (str): 起始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")
        :param timeout (int): timeout seconds, default None

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
            timeout=timeout,
            use_async=use_async,
            data_id_list=stock_id_list,
        )
        return stock_institutional_investors

    def taiwan_stock_institutional_investors_total(
        self, start_date: str, end_date: str = "", timeout: int = None
    ) -> pd.DataFrame:
        """get 整體三大市場法人買賣表
        :param start_date (str): 起始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")
        :param timeout (int): timeout seconds, default None

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
            timeout=timeout,
        )
        return stock_institutional_investors_total

    def taiwan_stock_shareholding(
        self,
        stock_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
        use_async: bool = False,
        stock_id_list: typing.List[str] = None,
    ) -> pd.DataFrame:
        """get 外資持股表
        :param stock_id (str): 股票代號("2330")
        :param start_date (str): 起始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")
        :param timeout (int): timeout seconds, default None

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
            timeout=timeout,
            use_async=use_async,
            data_id_list=stock_id_list,
        )
        return stock_shareholding

    def taiwan_stock_holding_shares_per(
        self,
        stock_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
        use_async: bool = False,
        stock_id_list: typing.List[str] = None,
    ) -> pd.DataFrame:
        """get 股權持股分級表
        :param stock_id (str): 股票代號("2330")
        :param start_date (str): 起始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")
        :param timeout (int): timeout seconds, default None

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
            timeout=timeout,
            use_async=use_async,
            data_id_list=stock_id_list,
        )
        return stock_shareholding_class

    def taiwan_stock_securities_lending(
        self,
        stock_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
        use_async: bool = False,
        stock_id_list: typing.List[str] = None,
    ) -> pd.DataFrame:
        """get 借券成交明細
        :param stock_id (str): 股票代號("2330")
        :param start_date (str): 起始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")
        :param timeout (int): timeout seconds, default None

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
            timeout=timeout,
            use_async=use_async,
            data_id_list=stock_id_list,
        )
        return stock_securities_lending

    def taiwan_daily_short_sale_balances(
        self,
        stock_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
        use_async: bool = False,
        stock_id_list: typing.List[str] = None,
    ) -> pd.DataFrame:
        """get 借券成交明細
        :param stock_id (str): 股票代號("2330")
        :param start_date (str): 起始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")
        :param timeout (int): timeout seconds, default None

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
            timeout=timeout,
            use_async=use_async,
            data_id_list=stock_id_list,
        )
        return short_sale_balances

    def taiwan_stock_cash_flows_statement(
        self,
        stock_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
        use_async: bool = False,
        stock_id_list: typing.List[str] = None,
    ) -> pd.DataFrame:
        """get 現金流量表
        :param stock_id (str): 股票代號("2330")
        :param start_date (str): 起始日期: "2018-03-31" or "2021-Q1"
        :param end_date (str): 結束日期 "2021-06-30" or "2021-Q2"
        :param timeout (int): timeout seconds, default None

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
            end_date=(
                str(pd.Period(end_date).asfreq("D", "end")) if end_date else ""
            ),
            timeout=timeout,
            use_async=use_async,
            data_id_list=stock_id_list,
        )
        return stock_cash_flows_statement

    def taiwan_stock_financial_statement(
        self,
        stock_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
        use_async: bool = False,
        stock_id_list: typing.List[str] = None,
    ) -> pd.DataFrame:
        """get 綜合損益表
        :param stock_id (str): 股票代號("2330")
        :param start_date (str): 起始日期: "2018-03-31" or "2021-Q1"
        :param end_date (str): 結束日期 "2021-06-30" or "2021-Q2"
        :param timeout (int): timeout seconds, default None

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
            end_date=(
                str(pd.Period(end_date).asfreq("D", "end")) if end_date else ""
            ),
            timeout=timeout,
            use_async=use_async,
            data_id_list=stock_id_list,
        )
        return stock_financial_statement

    def taiwan_stock_balance_sheet(
        self,
        stock_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
        use_async: bool = False,
        stock_id_list: typing.List[str] = None,
    ) -> pd.DataFrame:
        """get 資產負債表
        :param stock_id (str): 股票代號("2330")
        :param start_date (str): 起始日期: "2018-03-31" or "2021-Q1"
        :param end_date (str): 結束日期 "2021-06-30" or "2021-Q2"
        :param timeout (int): timeout seconds, default None

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
            end_date=(
                str(pd.Period(end_date).asfreq("D", "end")) if end_date else ""
            ),
            timeout=timeout,
            use_async=use_async,
            data_id_list=stock_id_list,
        )
        return stock_balance_sheet

    def taiwan_stock_dividend(
        self,
        stock_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
        use_async: bool = False,
        stock_id_list: typing.List[str] = None,
    ) -> pd.DataFrame:
        """股利政策表
        :param stock_id (str): 股票代號("2330")
        :param start_date (str): 起始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")
        :param timeout (int): timeout seconds, default None

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
            timeout=timeout,
            use_async=use_async,
            data_id_list=stock_id_list,
        )
        return stock_dividend

    def taiwan_stock_dividend_result(
        self,
        stock_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
        use_async: bool = False,
        stock_id_list: typing.List[str] = None,
    ) -> pd.DataFrame:
        """get 除權除息結果表
        :param stock_id (str): 股票代號("2330")
        :param start_date (str): 起始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")
        :param timeout (int): timeout seconds, default None

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
            timeout=timeout,
            use_async=use_async,
            data_id_list=stock_id_list,
        )
        return stock_dividend_result

    def taiwan_stock_month_revenue(
        self,
        stock_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
        use_async: bool = False,
        stock_id_list: typing.List[str] = None,
    ) -> pd.DataFrame:
        """get 月營收表
        Since the revenue in January,
        the public time is usually only announced in February,
        so the date plus one month
        :param stock_id (str): 股票代號("2330")
        :param start_date (str): 起始日期: "2018-02-01" or "2021-1M"
        :param end_date (str): 結束日期 "2021-03-01" or "2021-2M"
        :param timeout (int): timeout seconds, default None

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
            end_date=(
                str(
                    (
                        pd.Period(end_date).asfreq("M") + pd.offsets.MonthEnd(1)
                    ).asfreq("D", "start")
                )
                if end_date
                else ""
            ),
            timeout=timeout,
            use_async=use_async,
            data_id_list=stock_id_list,
        )
        return stock_month_revenue

    def taiwan_stock_market_value_weight(
        self,
        stock_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
        use_async: bool = False,
        stock_id_list: typing.List[str] = None,
    ) -> pd.DataFrame:
        """get 台股市值比重表
        :param stock_id (str): 股票代號("2330")
        :param start_date (str): 起始日期: "2018-02-01"
        :param end_date (str): 結束日期 "2021-03-01"
        :param timeout (int): timeout seconds, default None

        :return: 市值比重表 TaiwanStockMarketValueWeight
        :rtype pd.DataFrame
        :rtype column rank (int)
        :rtype column stock_id (str)
        :rtype column stock_name (str)
        :rtype column weight_per (float)
        :rtype column date (str)
        :rtype column type (str)
        """
        stock_market_value_weight = self.get_data(
            dataset=Dataset.TaiwanStockMarketValueWeight,
            data_id=stock_id,
            start_date=start_date,
            end_date=end_date,
            timeout=timeout,
            use_async=use_async,
            data_id_list=stock_id_list,
        )
        return stock_market_value_weight

    def taiwan_futopt_tick_info(self, timeout: int = None) -> pd.DataFrame:
        """get 期貨, 選擇權即時報價總覽
        :param timeout (int): timeout seconds, default None

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
            dataset=Dataset.TaiwanFutOptTickInfo, timeout=timeout
        )
        return futopt_tick_info

    def taiwan_futopt_tick_realtime(
        self, data_id: str, timeout: int = None
    ) -> pd.DataFrame:
        """get 期貨, 選擇權即時報價
        :param data_id: 期貨、選擇權代碼("TXFL1")
        :param timeout (int): timeout seconds, default None

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
            dataset=Dataset.TaiwanFutOptTick, data_id=data_id, timeout=timeout
        )
        return futopt_tick

    def taiwan_futopt_daily_info(self, timeout: int = None) -> pd.DataFrame:
        """get 期貨, 選擇權日成交資訊總覽
        :param timeout (int): timeout seconds, default None

        :return: 期貨, 選擇權日成交資訊總覽 TaiwanFutOptDailyInfo
        :rtype pd.DataFrame
        :rtype column code (str)
        :rtype column type (str)
        """
        futopt_daily_info = self.get_data(
            dataset=Dataset.TaiwanFutOptDailyInfo, timeout=timeout
        )
        return futopt_daily_info

    def taiwan_futures_daily(
        self,
        futures_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
        use_async: bool = False,
        futures_id_list: typing.List[str] = None,
    ) -> pd.DataFrame:
        """get 期貨日成交資訊
        :param futures_id: 期貨代號("TX")
        :param start_date (str): 起始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")
        :param timeout (int): timeout seconds, default None

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
            timeout=timeout,
            use_async=use_async,
            data_id_list=futures_id_list,
        )
        return futures_daily

    def taiwan_option_daily(
        self,
        option_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
        use_async: bool = False,
        option_id_list: typing.List[str] = None,
    ) -> pd.DataFrame:
        """get 選擇權日成交資訊
        :param option_id: 選擇權代號("TXO")
        :param start_date (str): 起始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")
        :param timeout (int): timeout seconds, default None

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
            timeout=timeout,
            use_async=use_async,
            data_id_list=option_id_list,
        )
        return option_daily

    def taiwan_futures_open_interest_large_traders(
        self,
        futures_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
        use_async: bool = False,
        futures_id_list: typing.List[str] = None,
    ) -> pd.DataFrame:
        """get 期貨大額交易人未沖銷部位
        :param futures_id: 期貨代號("TJF")
        :param start_date (str): 起始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")
        :param timeout (int): timeout seconds, default None

        :return: 期貨大額交易人未沖銷部位 TaiwanFuturesOpenInterestLargeTraders
        :rtype pd.DataFrame
        :rtype column name (str)
        :rtype column contract_type (str)
        :rtype column buy_top5_trader_open_interest (float)
        :rtype column buy_top5_trader_open_interest_per (float)
        :rtype column buy_top10_trader_open_interest (float)
        :rtype column buy_top10_trader_open_interest_per (float)
        :rtype column sell_top5_trader_open_interest (float)
        :rtype column sell_top5_trader_open_interest_per (float)
        :rtype column sell_top10_trader_open_interest (float)
        :rtype column sell_top10_trader_open_interest_per (float)
        :rtype column market_open_interest (int)
        :rtype column buy_top5_specific_open_interest (float)
        :rtype column buy_top5_specific_open_interest_per (float)
        :rtype column buy_top10_specific_open_interest (float)
        :rtype column buy_top10_specific_open_interest_per (float)
        :rtype column sell_top5_specific_open_interest (float)
        :rtype column sell_top5_specific_open_interest_per (float)
        :rtype column sell_top10_specific_open_interest (float)
        :rtype column sell_top10_specific_open_interest_per (float)
        :rtype column date (str)
        :rtype column futures_id (str)
        """
        futures_open_interest_large_traders = self.get_data(
            dataset=Dataset.TaiwanFuturesOpenInterestLargeTraders,
            data_id=futures_id,
            start_date=start_date,
            end_date=end_date,
            timeout=timeout,
            use_async=use_async,
            data_id_list=futures_id_list,
        )
        return futures_open_interest_large_traders

    def taiwan_option_open_interest_large_traders(
        self,
        option_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
        use_async: bool = False,
        option_id_list: typing.List[str] = None,
    ) -> pd.DataFrame:
        """get 選擇權大額交易人未沖銷部位
        :param option_id: 期貨代號("CA")
        :param start_date (str): 起始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")
        :param timeout (int): timeout seconds, default None

        :return: 選擇權大額交易人未沖銷部位 TaiwanOptionOpenInterestLargeTraders
        :rtype column contract_type (str)
        :rtype column buy_top5_trader_open_interest (float)
        :rtype column buy_top5_trader_open_interest_per (float)
        :rtype column buy_top10_trader_open_interest (float)
        :rtype column buy_top10_trader_open_interest_per (float)
        :rtype column sell_top5_trader_open_interest (float)
        :rtype column sell_top5_trader_open_interest_per (float)
        :rtype column sell_top10_trader_open_interest (float)
        :rtype column sell_top10_trader_open_interest_per (float)
        :rtype column market_open_interest (int)
        :rtype column buy_top5_specific_open_interest (float)
        :rtype column buy_top5_specific_open_interest_per (float)
        :rtype column buy_top10_specific_open_interest (float)
        :rtype column buy_top10_specific_open_interest_per (float)
        :rtype column sell_top5_specific_open_interest (float)
        :rtype column sell_top5_specific_open_interest_per (float)
        :rtype column sell_top10_specific_open_interest (float)
        :rtype column sell_top10_specific_open_interest_per (float)
        :rtype column date (str)
        :rtype column put_call (str)
        :rtype column name (str)
        :rtype column option_id (str)
        """
        option_open_interest_large_traders = self.get_data(
            dataset=Dataset.TaiwanOptionOpenInterestLargeTraders,
            data_id=option_id,
            start_date=start_date,
            end_date=end_date,
            timeout=timeout,
            use_async=use_async,
            data_id_list=option_id_list,
        )
        return option_open_interest_large_traders

    def taiwan_futures_tick(
        self, futures_id: str, date: str, timeout: int = None
    ) -> pd.DataFrame:
        """get 期貨交易明細表, 資料量超過10萬筆, 需等一段時間
        :param futures_id: 期貨代號("TX")
        :param date (str): 日期("2018-01-01")
        :param timeout (int): timeout seconds, default None

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
            timeout=timeout,
        )
        return futures_tick

    def taiwan_option_tick(
        self,
        option_id: str,
        date: str,
        timeout: int = None,
        use_async: bool = False,
        option_id_list: typing.List[str] = None,
    ) -> pd.DataFrame:
        """get 選擇權交易明細表, 資料量超過10萬筆, 需等一段時間
        :param option_id: 選擇權代號("TXO")
        :param date (str): 日期("2018-01-01")
        :param timeout (int): timeout seconds, default None

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
            timeout=timeout,
            use_async=use_async,
            data_id_list=option_id_list,
        )
        return option_tick

    def taiwan_futures_institutional_investors(
        self,
        futures_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
        use_async: bool = False,
        futures_id_list: typing.List[str] = None,
    ) -> pd.DataFrame:
        """get 期貨三大法人買賣
        :param futures_id: 期貨代號("TX")
        :param start_date (str): 起始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")
        :param timeout (int): timeout seconds, default None

        :return: 期貨三大法人買賣 TaiwanFuturesInstitutionalInvestors
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
        futures_institutional_investors = self.get_data(
            dataset=Dataset.TaiwanFuturesInstitutionalInvestors,
            data_id=futures_id,
            start_date=start_date,
            end_date=end_date,
            timeout=timeout,
            use_async=use_async,
            data_id_list=futures_id_list,
        )
        return futures_institutional_investors

    def taiwan_option_institutional_investors(
        self,
        option_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
        use_async: bool = False,
        option_id_list: typing.List[str] = None,
    ) -> pd.DataFrame:
        """get 選擇權三大法人買賣
        :param option_id: 選擇權代號("TXO")
        :param start_date (str): 起始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")
        :param timeout (int): timeout seconds, default None

        :return: 選擇權三大法人買賣 TaiwanOptionInstitutionalInvestors
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
        option_institutional_investors = self.get_data(
            dataset=Dataset.TaiwanOptionInstitutionalInvestors,
            data_id=option_id,
            start_date=start_date,
            end_date=end_date,
            timeout=timeout,
            use_async=use_async,
            data_id_list=option_id_list,
        )
        return option_institutional_investors

    def taiwan_futures_institutional_investors_after_hours(
        self,
        futures_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
        use_async: bool = False,
        futures_id_list: typing.List[str] = None,
    ) -> pd.DataFrame:
        """get 期貨夜盤三大法人買賣
        :param futures_id: 期貨代號("TX")
        :param start_date (str): 起始日期("2021-10-12")
        :param end_date (str): 結束日期("2023-11-12")
        :param timeout (int): timeout seconds, default None

        :return: 期貨夜盤三大法人買賣 TaiwanFuturesInstitutionalInvestorsAfterHours
        :rtype pd.DataFrame
        :rtype column name (str)
        :rtype column date (str)
        :rtype column institutional_investors (str)
        :rtype column long_deal_volume (int)
        :rtype column long_deal_amount (int)
        :rtype column short_deal_volume (int)
        :rtype column short_deal_amount (int)
        """
        futures_institutional_investors_after_hours = self.get_data(
            dataset=Dataset.TaiwanFuturesInstitutionalInvestorsAfterHours,
            data_id=futures_id,
            start_date=start_date,
            end_date=end_date,
            timeout=timeout,
            use_async=use_async,
            data_id_list=futures_id_list,
        )
        return futures_institutional_investors_after_hours

    def taiwan_option_institutional_investors_after_hours(
        self,
        option_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
        use_async: bool = False,
        option_id_list: typing.List[str] = None,
    ) -> pd.DataFrame:
        """get 選擇權夜盤三大法人買賣
        :param option_id: 選擇權代號("TXO")
        :param start_date (str): 起始日期("2021-10-12")
        :param end_date (str): 結束日期("2023-11-12")
        :param timeout (int): timeout seconds, default None

        :return: 選擇權夜盤三大法人買賣 TaiwanOptionInstitutionalInvestorsAfterHours
        :rtype pd.DataFrame
        :rtype column name (str)
        :rtype column date (str)
        :rtype column institutional_investors (str)
        :rtype column long_deal_volume (int)
        :rtype column long_deal_amount (int)
        :rtype column short_deal_volume (int)
        :rtype column short_deal_amount (int)
        """
        option_institutional_investors_after_hours = self.get_data(
            dataset=Dataset.TaiwanOptionInstitutionalInvestorsAfterHours,
            data_id=option_id,
            start_date=start_date,
            end_date=end_date,
            timeout=timeout,
            use_async=use_async,
            data_id_list=option_id_list,
        )
        return option_institutional_investors_after_hours

    def taiwan_futures_dealer_trading_volume_daily(
        self,
        futures_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
        use_async: bool = False,
        futures_id_list: typing.List[str] = None,
    ) -> pd.DataFrame:
        """get 期貨各卷商每日交易
        :param futures_id: 期貨代號("TX")
        :param start_date (str): 起始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")
        :param timeout (int): timeout seconds, default None

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
            timeout=timeout,
            use_async=use_async,
            data_id_list=futures_id_list,
        )
        return futures_dealer_trading_volume_daily

    def taiwan_option_dealer_trading_volume_daily(
        self,
        option_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
        use_async: bool = False,
        option_id_list: typing.List[str] = None,
    ) -> pd.DataFrame:
        """get 選擇權各卷商每日交易
        :param option_id: 選擇權代號("TXO")
        :param start_date (str): 起始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")
        :param timeout (int): timeout seconds, default None

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
            timeout=timeout,
            use_async=use_async,
            data_id_list=option_id_list,
        )
        return option_dealer_trading_volume_daily

    def taiwan_stock_news(
        self,
        stock_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
    ) -> pd.DataFrame:
        """get 相關新聞
        :param stock_id: 股票代號("2330")
        :param start_date (str): 起始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")
        :param timeout (int): timeout seconds, default None

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
            timeout=timeout,
        )
        return stock_news

    def taiwan_stock_total_return_index(
        self,
        index_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
    ) -> pd.DataFrame:
        """get 加權, 櫃買報酬指數
        :param index_id: index 代號,
            "TAIEX" (發行量加權股價報酬指數),
            "TPEx" (櫃買指數與報酬指數)
        :param start_date (str): 起始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")
        :param timeout (int): timeout seconds, default None

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
            timeout=timeout,
        )
        stock_total_return_index.columns = stock_total_return_index.columns.map(
            dict(
                price="price",
                stock_id="index_id",
                date="date",
            )
        )
        return stock_total_return_index

    def taiwan_stock_capital_reduction_reference_price(
        self,
        stock_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
        use_async: bool = False,
        stock_id_list: typing.List[str] = None,
    ) -> pd.DataFrame:
        """get 減資恢復買賣參考價格
        :param stock_id (str): 股票代號("2330")
        :param start_date (str): 起始日期: "2018-03-31" or "2021-Q1"
        :param end_date (str): 結束日期 "2021-06-30" or "2021-Q2"
        :param timeout (int): timeout seconds, default None

        :return: 減資恢復買賣參考價格 TaiwanStockCapitalReductionReferencePrice
        :rtype pd.DataFrame
        :rtype column date (str)
        :rtype column stock_id (str)
        :rtype column ClosingPriceonTheLastTradingDay (float)
        :rtype column PostReductionReferencePrice (float)
        :rtype column LimitUp (float)
        :rtype column LimitDown (float)
        :rtype column OpeningReferencePrice (float)
        :rtype column ExrightReferencePrice (float)
        :rtype column ReasonforCapitalReduction (str)
        """
        taiwan_stock_capital_reduction_reference_price = self.get_data(
            dataset=Dataset.TaiwanStockCapitalReductionReferencePrice,
            data_id=stock_id,
            start_date=str(pd.Period(start_date).asfreq("D", "end")),
            end_date=(
                str(pd.Period(end_date).asfreq("D", "end")) if end_date else ""
            ),
            timeout=timeout,
            use_async=use_async,
            data_id_list=stock_id_list,
        )
        return taiwan_stock_capital_reduction_reference_price

    def taiwan_stock_market_value(
        self,
        stock_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
        use_async: bool = False,
        stock_id_list: typing.List[str] = None,
    ) -> pd.DataFrame:
        """get 台灣個股市值
        :param timeout (int): timeout seconds, default None

        :return: 台灣個股市值 TaiwanStockMarketValue
        :rtype pd.DataFrame
        :rtype column date (str)
        :rtype column stock_id (str)
        :rtype column market_value (float)
        """
        tw_stock_market_value = self.get_data(
            dataset=Dataset.TaiwanStockMarketValue,
            data_id=stock_id,
            start_date=start_date,
            end_date=end_date,
            timeout=timeout,
            use_async=use_async,
            data_id_list=stock_id_list,
        )
        return tw_stock_market_value

    def taiwan_stock_10year(
        self,
        stock_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
        use_async: bool = False,
        stock_id_list: typing.List[str] = None,
    ) -> pd.DataFrame:
        """get 台灣個股10年平均收盤價
        :param timeout (int): timeout seconds, default None

        :return: 台灣個股10年平均收盤價 TaiwanStock10Year
        :rtype pd.DataFrame
        :rtype column date (str)
        :rtype column stock_id (str)
        :rtype column close (float)
        """
        tw_stock_10year = self.get_data(
            dataset=Dataset.TaiwanStock10Year,
            data_id=stock_id,
            start_date=start_date,
            end_date=end_date,
            timeout=timeout,
            use_async=use_async,
            data_id_list=stock_id_list,
        )
        return tw_stock_10year

    def taiwan_stock_weekly(
        self,
        stock_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
        use_async: bool = False,
        stock_id_list: typing.List[str] = None,
    ) -> pd.DataFrame:
        """get 台股週 K 資料表
        :param timeout (int): timeout seconds, default None

        :return: 台股週 K 資料表 TaiwanStockWeekPrice
        :rtype pd.DataFrame
        :rtype column stock_id (str)
        :rtype column yweek (str)
        :rtype column max (float)
        :rtype column min (float)
        :rtype column trading_volume (int))
        :rtype column trading_money (int)
        :rtype column trading_turnover (int)
        :rtype column date (str)
        :rtype column close (float)
        :rtype column open (float)
        :rtype column spread (float)
        """
        tw_stock_weekly = self.get_data(
            dataset=Dataset.TaiwanStockWeekPrice,
            data_id=stock_id,
            start_date=start_date,
            end_date=end_date,
            timeout=timeout,
            use_async=use_async,
            data_id_list=stock_id_list,
        )
        return tw_stock_weekly

    def taiwan_stock_monthly(
        self,
        stock_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
        use_async: bool = False,
        stock_id_list: typing.List[str] = None,
    ) -> pd.DataFrame:
        """get 台股月 K 資料表
        :param timeout (int): timeout seconds, default None

        :return: 台股月 K 資料表 TaiwanStockMonthPrice
        :rtype pd.DataFrame
        :rtype column stock_id (str)
        :rtype column ymonth (str)
        :rtype column max (float)
        :rtype column min (float)
        :rtype column trading_volume (int))
        :rtype column trading_money (int)
        :rtype column trading_turnover (int)
        :rtype column date (str)
        :rtype column close (float)
        :rtype column open (float)
        :rtype column spread (float)
        """
        tw_stock_monthly = self.get_data(
            dataset=Dataset.TaiwanStockMonthPrice,
            data_id=stock_id,
            start_date=start_date,
            end_date=end_date,
            timeout=timeout,
            use_async=use_async,
            data_id_list=stock_id_list,
        )
        return tw_stock_monthly

    def taiwan_stock_kbar(
        self,
        stock_id: str = "",
        stock_id_list: typing.List[str] = None,
        date: str = "",
        timeout: int = None,
        use_async: bool = False,
    ) -> pd.DataFrame:
        """get 台股分 K 資料表
        :param timeout (int): timeout seconds, default None

        :return: 台股分 K 資料表 TaiwanStockKBar
        :rtype pd.DataFrame
        :rtype column date (str)
        :rtype column minute (str)
        :rtype column stock_id (str)
        :rtype column open (float)
        :rtype column high (float)
        :rtype column low (float)
        :rtype column close (float)
        :rtype column volume (int)
        """
        taiwan_stock_bar = self.get_data(
            dataset=Dataset.TaiwanStockKBar,
            data_id=stock_id,
            data_id_list=stock_id_list,
            start_date=date,
            timeout=timeout,
            use_async=use_async,
        )
        return taiwan_stock_bar

    def taiwan_stock_delisting(
        self,
        stock_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
        use_async: bool = False,
        stock_id_list: typing.List[str] = None,
    ) -> pd.DataFrame:
        """get 台股個股下市下櫃表
        :param timeout (int): timeout seconds, default None

        :return: 台股個股下市下櫃表 TaiwanStockDelisting
        :rtype pd.DataFrame
        :rtype column date (str)
        :rtype column stock_id (str)
        :rtype column stock_name (str)
        """
        taiwan_stock_delisting = self.get_data(
            dataset=Dataset.TaiwanStockDelisting,
            data_id=stock_id,
            start_date=start_date,
            end_date=end_date,
            timeout=timeout,
            use_async=use_async,
            data_id_list=stock_id_list,
        )
        return taiwan_stock_delisting

    def taiwan_total_exchange_margin_maintenance(
        self,
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
    ) -> pd.DataFrame:
        """get 台灣大盤融資維持率
        :param start_date (str): 開始日期("2023-01-01")
        :param end_date (str): 結束日期("2023-01-31")
        :param timeout (int): timeout seconds, default None

        :return: 台灣大盤融資維持率 TaiwanTotalExchangeMarginMaintenance
        :rtype pd.DataFrame
        :rtype column date (str)
        :rtype column TotalExchangeMarginMaintenance (float)
        """
        tw_total_exchange_mMargin_maintenance = self.get_data(
            dataset=Dataset.TaiwanTotalExchangeMarginMaintenance,
            start_date=start_date,
            end_date=end_date,
            timeout=timeout,
        )
        return tw_total_exchange_mMargin_maintenance

    def us_stock_info(self, timeout: int = None) -> pd.DataFrame:
        """get 美國股票代碼總覽
        :param timeout (int): timeout seconds, default None

        :return: 美國股票代碼總覽 USStockInfo
        :rtype pd.DataFrame
        :rtype column date (str)
        :rtype column stock_id (str)
        :rtype column Country (str)
        :rtype column IPOYear (str)
        :rtype column MarketCap (str)
        :rtype column Subsector (str)
        :rtype column stock_name (str)
        """
        stock_info = self.get_data(
            dataset=Dataset.USStockInfo,
            timeout=timeout,
        )
        return stock_info

    def us_stock_price(
        self,
        stock_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
    ) -> pd.DataFrame:
        """get 美國股價資料表
        :param stock_id (str): 股票代號("VOO")
        :param start_date (str): 開始日期("2023-01-01")
        :param end_date (str): 結束日期("2023-01-31")
        :param timeout (int): timeout seconds, default None

        :return: 美國股價資料表 USStockPrice
        :rtype pd.DataFrame
        :rtype column date (str)
        :rtype column stock_id (str)
        :rtype column Adj_Close (float)
        :rtype column Close (float)
        :rtype column High (float)
        :rtype column Low (float)
        :rtype column Open (float)
        :rtype column Volume (int)
        """
        stock_price = self.get_data(
            dataset=Dataset.USStockPrice,
            data_id=stock_id,
            start_date=start_date,
            end_date=end_date,
            timeout=timeout,
        )
        return stock_price

    def taiwan_stock_tick_snapshot(
        self,
        stock_id: typing.Union[str, typing.List[str]] = "",
        timeout: int = None,
    ) -> pd.DataFrame:
        """get 台股即時資訊 taiwan_stock_tick_snapshot (只限 sponsor 會員使用)
        :param stock_id (Union(str, List[str])): 股票代號("2330")
        :param timeout (int): timeout seconds, default None

        :return: 台股即時資訊 taiwan_stock_tick_snapshot
        :rtype pd.DataFrame
        :rtype column open (float)
        :rtype column high (float)
        :rtype column low (float)
        :rtype column close (float)
        :rtype column change_price (float)
        :rtype column change_rate (float)
        :rtype column average_price (float)
        :rtype column volume (int)
        :rtype column total_volume (int)
        :rtype column amount (int)
        :rtype column total_amount (int)
        :rtype column yesterday_volume (int)
        :rtype column buy_price (float)
        :rtype column buy_volume (int)
        :rtype column sell_price (float)
        :rtype column sell_volume (int)
        :rtype column volume_ratio (float)
        :rtype column date (str)
        :rtype column stock_id (str)
        :rtype column TickType (int)
        """
        taiwan_stock_tick_snapshot = self.get_taiwan_stock_tick_snapshot(
            dataset=Dataset.TaiwanStockTickSnapshot,
            data_id=stock_id,
            timeout=timeout,
        )
        return taiwan_stock_tick_snapshot

    def taiwan_futures_snapshot(
        self,
        futures_id: str = "",
        timeout: int = None,
    ) -> pd.DataFrame:
        """get 台股期貨即時資訊 taiwan_futures_snapshot (只限 sponsor 會員使用)
        (目前支援台指期、約 10 秒更新一次)
        :param futures_id (str): 股票代號("TXF")
        :param timeout (int): timeout seconds, default None

        :return: 台股期貨即時資訊 taiwan_futures_snapshot
        :rtype pd.DataFrame
        :rtype column open (float)
        :rtype column high (float)
        :rtype column low (float)
        :rtype column close (float)
        :rtype column change_price (float)
        :rtype column change_rate (float)
        :rtype column average_price (float)
        :rtype column volume (int)
        :rtype column total_volume (int)
        :rtype column amount (int)
        :rtype column total_amount (int)
        :rtype column yesterday_volume (int)
        :rtype column buy_price (float)
        :rtype column buy_volume (int)
        :rtype column sell_price (float)
        :rtype column sell_volume (int)
        :rtype column volume_ratio (float)
        :rtype column date (str)
        :rtype column futures_id (str)
        :rtype column TickType (int)
        """
        futures_snapshot = self.get_taiwan_futures_snapshot(
            dataset=Dataset.TaiwanFuturesSnapshot,
            data_id=futures_id,
            timeout=timeout,
        )
        return futures_snapshot

    def taiwan_options_snapshot(
        self,
        options_id: str = "",
        timeout: int = None,
    ) -> pd.DataFrame:
        """get 台股選擇權即時資訊 taiwan_options_snapshot (只限 sponsor 會員使用)
        (目前支援台指選擇權、約 10 秒更新一次)
        :param options_id (str): 股票代號("TXO")
        :param timeout (int): timeout seconds, default None

        :return: 台股選擇權即時資訊 taiwan_options_snapshot
        :rtype pd.DataFrame
        :rtype column open (float)
        :rtype column high (float)
        :rtype column low (float)
        :rtype column close (float)
        :rtype column change_price (float)
        :rtype column change_rate (float)
        :rtype column average_price (float)
        :rtype column volume (int)
        :rtype column total_volume (int)
        :rtype column amount (int)
        :rtype column total_amount (int)
        :rtype column yesterday_volume (int)
        :rtype column buy_price (float)
        :rtype column buy_volume (int)
        :rtype column sell_price (float)
        :rtype column sell_volume (int)
        :rtype column volume_ratio (float)
        :rtype column date (str)
        :rtype column options_id (str)
        :rtype column TickType (int)
        """
        options_snapshot = self.get_taiwan_options_snapshot(
            dataset=Dataset.TaiwanOptionsSnapshot,
            data_id=options_id,
            timeout=timeout,
        )
        return options_snapshot

    def taiwan_stock_convertible_bond_info(
        self, timeout: int = None
    ) -> pd.DataFrame:
        """get 可轉債總覽
        :param timeout (int): timeout seconds, default None

        :return: 可轉債總覽 TaiwanStockConvertibleBondInfo
        :rtype pd.DataFrame
        :rtype column cb_id (str)
        :rtype column cb_name (str)
        :rtype column InitialDateOfConversion (str)
        :rtype column DueDateOfConversion (str)
        :rtype column IssuanceAmount (int)
        """
        df = self.get_data(
            dataset=Dataset.TaiwanStockConvertibleBondInfo,
            timeout=timeout,
        )
        return df

    def taiwan_stock_convertible_bond_daily(
        self,
        cb_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
    ) -> pd.DataFrame:
        """get 可轉債日成交資訊
        :param cb_id (str): 可轉債代號("2330")
        :param start_date (str): 開始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")
        :param timeout (int): timeout seconds, default None

        :return: 可轉債日成交資訊 TaiwanStockConvertibleBondDaily
        :rtype pd.DataFrame
        :rtype column cb_id: (str)
        :rtype column cb_name: (str)
        :rtype column transaction_type: (str)
        :rtype column close: (float)
        :rtype column change: (float)
        :rtype column open: (float)
        :rtype column max: (float)
        :rtype column min: (float)
        :rtype column no_of_transactions: (int)
        :rtype column unit: (int)
        :rtype column trading_value: (int)
        :rtype column avg_price: (float)
        :rtype column next_ref_price: (float)
        :rtype column next_max_limit: (float)
        :rtype column next_min_limit: (float)
        :rtype column date: (str)
        """
        df = self.get_data(
            dataset=Dataset.TaiwanStockConvertibleBondDaily,
            data_id=cb_id,
            start_date=start_date,
            end_date=end_date,
            timeout=timeout,
        )
        return df

    def taiwan_stock_convertible_bond_institutional_investors(
        self,
        cb_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
    ) -> pd.DataFrame:
        """get 可轉債三大法人日交易資訊
        :param cb_id (str): 可轉債代號("2330")
        :param start_date (str): 開始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")
        :param timeout (int): timeout seconds, default None

        :return: 可轉債三大法人日交易資訊 TaiwanStockConvertibleBondInstitutionalInvestors
        :rtype pd.DataFrame
        :rtype column Foreign_Investor_Buy: (int)
        :rtype column Foreign_Investor_Sell: (int)
        :rtype column Foreign_Investor_Overbuy: (int)
        :rtype column Investment_Trust_Buy: (int)
        :rtype column Investment_Trust_Sell: (int)
        :rtype column Investment_Trust_Overbuy: (int)
        :rtype column Dealer_self_Buy: (int)
        :rtype column Dealer_self_Sell: (int)
        :rtype column Dealer_self_Overbuy: (int)
        :rtype column Total_Overbuy: (int)
        :rtype column cb_id: (str)
        :rtype column cb_name: (str)
        :rtype column date: (str)
        """
        df = self.get_data(
            dataset=Dataset.TaiwanStockConvertibleBondInstitutionalInvestors,
            data_id=cb_id,
            start_date=start_date,
            end_date=end_date,
            timeout=timeout,
        )
        return df

    def taiwan_stock_convertible_bond_daily_overview(
        self,
        cb_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
    ) -> pd.DataFrame:
        """get 可轉債每日總覽資訊
        :param cb_id (str): 可轉債代號("2330")
        :param start_date (str): 開始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")
        :param timeout (int): timeout seconds, default None

        :return: 可轉債每日總覽資訊 TaiwanStockConvertibleBondDailyOverview
        :rtype pd.DataFrame
        :rtype column cb_id: (str)
        :rtype column cb_name: (str)
        :rtype column date: (str)
        :rtype column InitialDateOfConversion: (str)
        :rtype column DueDateOfConversion: (str)
        :rtype column InitialDateOfStopConversion: (str)
        :rtype column DueDateOfStopConversion: (str)
        :rtype column ConversionPrice: (float)
        :rtype column NextEffectiveDateOfConversionPrice: (str)
        :rtype column LatestInitialDateOfPut: (str)
        :rtype column LatestDueDateOfPut: (str)
        :rtype column LatestPutPrice: (float)
        :rtype column InitialDateOfEarlyRedemption: (str)
        :rtype column DueDateOfEarlyRedemption: (str)
        :rtype column EarlyRedemptionPrice: (float)
        :rtype column DateOfDelisted: (str)
        :rtype column IssuanceAmount: (float)
        :rtype column OutstandingAmount: (float)
        :rtype column ReferencePrice: (float)
        :rtype column PriceOfUnderlyingStock: (float)
        :rtype column InitialDateOfSuspension: (str)
        :rtype column DueDateOfSuspension: (str)
        :rtype column CouponRate: (float)
        """
        df = self.get_data(
            dataset=Dataset.TaiwanStockConvertibleBondDailyOverview,
            data_id=cb_id,
            start_date=start_date,
            end_date=end_date,
            timeout=timeout,
        )
        return df

    def taiwan_stock_margin_short_sale_suspension(
        self,
        stock_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
        use_async: bool = False,
        stock_id_list: typing.List[str] = None,
    ) -> pd.DataFrame:
        """get 暫停融券賣出表(融券回補日)
        :param stock_id (str): 股票代號("2330")
        :param start_date (str): 開始日期("2018-01-01")
        :param end_date (str): 結束日期("2021-03-06")
        :param timeout (int): timeout seconds, default None

        :return: 暫停融券賣出表(融券回補日) TaiwanStockMarginShortSaleSuspension
        :rtype pd.DataFrame
        :rtype column stock_id: (str)
        :rtype column date: (str)
        :rtype column end_date: (str)
        :rtype column reason: (str)
        """
        df = self.get_data(
            dataset=Dataset.TaiwanStockMarginShortSaleSuspension,
            data_id=stock_id,
            start_date=start_date,
            end_date=end_date,
            timeout=timeout,
            use_async=use_async,
            data_id_list=stock_id_list,
        )
        return df

    def taiwan_stock_trading_daily_report(
        self,
        stock_id: str = "",
        securities_trader_id: str = "",
        stock_id_list: typing.List[str] = None,
        securities_trader_id_list: typing.List[str] = None,
        date: str = "",
        timeout: int = None,
        use_async: bool = False,
    ) -> pd.DataFrame:
        """get 當日卷商分點表
        :param stock_id (str): 股票代號("2330")
        :param securities_trader_id (str): 卷商代號("1020")
        :param date (str): 日期("2018-01-01")
        :param timeout (int): timeout seconds, default None

        :return: 當日卷商分點表 TaiwanStockTradingDailyReport
        :rtype pd.DataFrame
        :rtype column securities_trader (str)
        :rtype column price (float)
        :rtype column buy (int)
        :rtype column sell (int)
        :rtype column securities_trader_id (str)
        :rtype column stock_id (str)
        :rtype column date (str)
        """
        if not stock_id and not stock_id_list:
            stock_id_list = self._get_stock_id_list(date, timeout)

        stock_trading_daily_report = self.get_data(
            dataset=Dataset.TaiwanStockTradingDailyReport,
            data_id=stock_id,
            securities_trader_id=securities_trader_id,
            data_id_list=stock_id_list,
            securities_trader_id_list=securities_trader_id_list,
            start_date=date,
            end_date=date,
            timeout=timeout,
            use_async=use_async,
        )
        return stock_trading_daily_report

    def taiwan_stock_warrant_trading_daily_report(
        self,
        stock_id: str = "",
        securities_trader_id: str = "",
        stock_id_list: typing.List[str] = None,
        # securities_trader_id_list: typing.List[str] = None,
        date: str = "",
        timeout: int = None,
        use_async: bool = False,
    ) -> pd.DataFrame:
        """get 當日權證卷商分點表
        :param stock_id (str): 股票代號("2330")
        :param securities_trader_id (str): 卷商代號("1020")
        :param date (str): 日期("2018-01-01")
        :param timeout (int): timeout seconds, default None

        :return: 當日權證卷商分點表 TaiwanStockWarrantTradingDailyReport
        :rtype pd.DataFrame
        :rtype column securities_trader (str)
        :rtype column price (float)
        :rtype column buy (int)
        :rtype column sell (int)
        :rtype column securities_trader_id (str)
        :rtype column stock_id (str)
        :rtype column date (str)
        """
        stock_trading_daily_report = self.get_data(
            dataset=Dataset.TaiwanStockWarrantTradingDailyReport,
            data_id=stock_id,
            securities_trader_id=securities_trader_id,
            data_id_list=stock_id_list,
            # securities_trader_id_list=securities_trader_id_list,
            start_date=date,
            end_date=date,
            timeout=timeout,
            use_async=use_async,
        )
        return stock_trading_daily_report

    def taiwan_stock_trading_daily_report_secid_agg(
        self,
        stock_id: str = "",
        securities_trader_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
    ) -> pd.DataFrame:
        """get 當日卷商分點統計表
        :param stock_id (str): 股票代號("2330")
        :param securities_trader_id (str): 卷商代號("1020")
        :param start_date (str): 日期("2018-01-01")
        :param end_date (str): 日期("2018-01-02")
        :param timeout (int): timeout seconds, default None

        :return: 當日卷商分點統計表 TaiwanStockTradingDailyReportSecIdAgg
        :rtype pd.DataFrame
        :rtype column securities_trader (str)
        :rtype column securities_trader_id (str)
        :rtype column stock_id (str)
        :rtype column date (str)
        :rtype column buy_volume (int)
        :rtype column sell_volume (int)
        :rtype column buy_price (float)
        :rtype column sell_price (float)
        """
        stock_trading_daily_report_secid_agg = self.get_data(
            dataset=Dataset.TaiwanStockTradingDailyReportSecIdAgg,
            data_id=stock_id,
            securities_trader_id=securities_trader_id,
            start_date=start_date,
            end_date=end_date,
            timeout=timeout,
        )
        return stock_trading_daily_report_secid_agg

    def taiwan_business_indicator(
        self,
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
    ) -> pd.DataFrame:
        """get 台灣每月景氣對策信號表
        :param start_date (str): 日期("2018-01-01")
        :param end_date (str): 日期("2018-01-02")
        :param timeout (int): timeout seconds, default None

        :return: 台灣每月景氣對策信號表 TaiwanBusinessIndicator
        :rtype pd.DataFrame
        :rtype column date (str)
        :rtype column leading (float)
        :rtype column leading_notrend (float)
        :rtype column coincident (float)
        :rtype column coincident_notrend (float)
        :rtype column lagging (float)
        :rtype column lagging_notrend (float)
        :rtype column monitoring (float)
        :rtype column monitoring_color (str)
        """
        taiwan_business_indicator = self.get_data(
            dataset=Dataset.TaiwanBusinessIndicator,
            start_date=start_date,
            end_date=end_date,
            timeout=timeout,
        )
        return taiwan_business_indicator

    def taiwan_stock_disposition_securities_period(
        self,
        stock_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
        use_async: bool = False,
        stock_id_list: typing.List[str] = None,
    ) -> pd.DataFrame:
        """get 公布處置有價證券表
        :param stock_id (str): 股票代號("2330")
        :param start_date (str): 日期("2018-01-01")
        :param end_date (str): 日期("2018-01-02")
        :param timeout (int): timeout seconds, default None

        :return: 公布處置有價證券表 TaiwanStockDispositionSecuritiesPeriod
        :rtype pd.DataFrame
        :rtype column date (str)
        :rtype column stock_id (str)
        :rtype column stock_name (str)
        :rtype column disposition_cnt (int)
        :rtype column condition (str)
        :rtype column measure (str)
        :rtype column period_start (str)
        :rtype column period_end (str)
        """
        stock_disposition_securities_period = self.get_data(
            dataset=Dataset.TaiwanStockDispositionSecuritiesPeriod,
            data_id=stock_id,
            start_date=start_date,
            end_date=end_date,
            timeout=timeout,
            use_async=use_async,
            data_id_list=stock_id_list,
        )
        return stock_disposition_securities_period

    def taiwan_stock_industry_chain(
        self,
        stock_id: str = "",
        timeout: int = None,
    ) -> pd.DataFrame:
        """get 個體公司所屬產業鏈
        :param stock_id (str): 股票代號("2330")
        :param timeout (int): timeout seconds, default None

        :return: 個體公司所屬產業鏈 TaiwanStockIndustryChain
        :rtype pd.DataFrame
        :rtype column stock_id (str)
        :rtype column industry (str)
        :rtype column sub_industry (str)
        """
        stock_industry_chain = self.get_data(
            dataset=Dataset.TaiwanStockIndustryChain,
            stock_id=stock_id,
            timeout=timeout,
        )
        return stock_industry_chain

    def cnn_fear_greed_index(
        self,
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
    ) -> pd.DataFrame:
        """get 恐懼與貪婪指數
        :param start_date (str): 日期("2018-01-01")
        :param end_date (str): 日期("2018-01-02")
        :param timeout (int): timeout seconds, default None

        :return: 恐懼與貪婪指數 CnnFearGreedIndex
        :rtype pd.DataFrame
        :rtype column date (str)
        :rtype column fear_greed (str)
        :rtype column fear_greed_emotion (str)
        """
        cnn_fear_greed_index = self.get_data(
            dataset=Dataset.CnnFearGreedIndex,
            timeout=timeout,
            start_date=start_date,
            end_date=end_date,
        )
        return cnn_fear_greed_index

    def taiwan_stock_every5seconds_index(
        self,
        data_id: str = "",
        date: str = "",
        timeout: int = None,
        use_async: bool = False,
        data_id_list: typing.List[str] = None,
    ) -> pd.DataFrame:
        """get 每5秒指數統計
        :param data_id (str): 產業代號("Automobile")
        :param date (str): 日期("2018-01-01")
        :param timeout (int): timeout seconds, default None

        :return: 每5秒指數統計 TaiwanStockEvery5SecondsIndex
        :rtype pd.DataFrame
        :rtype column date (str)
        :rtype column time (str)
        :rtype column stock_id (str)
        :rtype column price (float)
        """
        taiwan_stock_every5seconds_index = self.get_data(
            dataset=Dataset.TaiwanStockEvery5SecondsIndex,
            data_id=data_id,
            timeout=timeout,
            start_date=date,
            use_async=use_async,
            data_id_list=data_id_list,
        )
        return taiwan_stock_every5seconds_index

    def taiwan_stock_trading_date(
        self,
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
    ) -> pd.DataFrame:
        """get 台灣交易日日期
        :param start_date (str): 日期("2025-01-01")
        :param end_date (str): 日期("2025-02-01")
        :param timeout (int): timeout seconds, default None

        :return: 台灣交易日日期 TaiwanStockTradingDate
        :rtype pd.DataFrame
        :rtype column date (str)
        """
        taiwan_stock_trading_date = self.get_data(
            dataset=Dataset.TaiwanStockTradingDate,
            timeout=timeout,
            start_date=start_date,
            end_date=end_date,
        )
        return taiwan_stock_trading_date

    def taiwan_stock_info_with_warrant_summary(
        self,
        start_date: str = "",
        end_date: str = "",
        stock_id: str = "",
        timeout: int = None,
    ) -> pd.DataFrame:
        """get 台股權證標的對照表
        :param start_date (str): 日期("2025-01-01")
        :param end_date (str): 日期("2026-02-01")
        :param stock_id (str): 權證代號("2330")
        :param timeout (int): timeout seconds, default None

        :return: 台股權證標的對照表 TaiwanStockInfoWithWarrantSummary
        :rtype pd.DataFrame
        :rtype column stock_id (str)
        :rtype column date (str)
        :rtype column close (float)
        :rtype column target_stock_id (str)
        :rtype column target_close (float)
        :rtype column type (str)
        :rtype column fulfillment_method (str)
        :rtype column end_date (str)
        :rtype column fulfillment_start_date (str)
        :rtype column fulfillment_end_date (str)
        :rtype column exercise_ratio (float)
        :rtype column fulfillment_price (float)
        """
        taiwan_stock_info_with_warrant_summary = self.get_data(
            dataset=Dataset.TaiwanStockInfoWithWarrantSummary,
            data_id=stock_id,
            timeout=timeout,
            start_date=start_date,
            end_date=end_date,
        )
        return taiwan_stock_info_with_warrant_summary

    def taiwan_stock_split_price(
        self,
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
    ) -> pd.DataFrame:
        """get 台股分割後參考價
        :param start_date (str): 日期("2025-01-01")
        :param end_date (str): 日期("2026-02-01")
        :param timeout (int): timeout seconds, default None

        :return: 台股分割後參考價 TaiwanStockSplitPrice
        :rtype pd.DataFrame
        :rtype column date (str)
        :rtype column stock_id (str)
        :rtype column type (str)
        :rtype column before_price (float)
        :rtype column after_price (float)
        :rtype column max_price (float)
        :rtype column min_price (float)
        :rtype column open_price (float)
        """
        taiwan_stock_split_price = self.get_data(
            dataset=Dataset.TaiwanStockSplitPrice,
            timeout=timeout,
            start_date=start_date,
            end_date=end_date,
        )
        return taiwan_stock_split_price

    def taiwan_stock_par_value_change(
        self,
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
    ) -> pd.DataFrame:
        """get 台灣股票變更面額恢復買賣參考價格
        :param start_date (str): 日期("2025-01-01")
        :param end_date (str): 日期("2025-02-01")
        :param timeout (int): timeout seconds, default None

        :return: 台灣股票變更面額恢復買賣參考價格 TaiwanStockParValueChange
        :rtype pd.DataFrame
        :rtype column date (str)
        :rtype column stock_id (str)
        :rtype column stock_name (str)
        :rtype column before_close (float)
        :rtype column after_ref_close (float)
        :rtype column after_ref_max (float)
        :rtype column after_ref_min (float)
        :rtype column after_ref_open (float)
        """
        taiwan_stock_par_value_change = self.get_data(
            dataset=Dataset.TaiwanStockParValueChange,
            timeout=timeout,
            start_date=start_date,
            end_date=end_date,
        )
        return taiwan_stock_par_value_change

    def taiwan_stock_suspended(
        self,
        stock_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
    ) -> pd.DataFrame:
        """get 台股暫停交易公告
        :param stock_id (str): 股票代號
        :param start_date (str): 日期("2017-04-01")
        :param end_date (str): 日期("2025-01-01")
        :param timeout (int): timeout seconds, default None

        :return: 台股暫停交易公告 TaiwanStockSuspended
        :rtype pd.DataFrame
        :rtype column date (str)
        :rtype column stock_id (str)
        :rtype column suspension_time (str)
        :rtype column resumption_date (str)
        :rtype column resumption_time (str)
        """
        taiwan_stock_suspended = self.get_data(
            dataset=Dataset.TaiwanStockSuspended,
            data_id=stock_id,
            start_date=start_date,
            end_date=end_date,
            timeout=timeout,
        )
        return taiwan_stock_suspended

    def taiwan_stock_day_trading_suspension(
        self,
        stock_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
    ) -> pd.DataFrame:
        """get 暫停先賣後買當沖預告表
        :param stock_id (str): 股票代號
        :param start_date (str): 日期("2024-12-01")
        :param end_date (str): 日期("2025-01-01")
        :param timeout (int): timeout seconds, default None

        :return: 暫停先賣後買當沖預告表 TaiwanStockDayTradingSuspension
        :rtype pd.DataFrame
        :rtype column stock_id (str)
        :rtype column date (str)
        :rtype column end_date (str)
        :rtype column reason (str)
        """
        taiwan_stock_day_trading_suspension = self.get_data(
            dataset=Dataset.TaiwanStockDayTradingSuspension,
            data_id=stock_id,
            start_date=start_date,
            end_date=end_date,
            timeout=timeout,
        )
        return taiwan_stock_day_trading_suspension

    def _get_stock_id_list(
        self, date: str, timeout: int = None
    ) -> typing.List[str]:
        """A helper function that returns all stock IDs with volume > 0 for specific date.
        :param date (str): 日期("2025-01-01")
        :param timeout (int): timeout seconds, default None

        :return: list[str]
        """
        stock_info = self.taiwan_stock_info(timeout=timeout)
        type_mask = stock_info["type"].isin(["twse", "tpex"])
        industry_category_mask = stock_info["industry_category"].isin(
            ["大盤", "Index", "所有證券"]
        )
        stock_id_mask = stock_info["stock_id"].isin(["TAIEX", "TPEx"])
        stock_info = stock_info[
            type_mask & (~industry_category_mask) & (~stock_id_mask)
        ]
        taiwan_stock_price_df = self.taiwan_stock_daily(start_date=date)
        taiwan_stock_price_df = taiwan_stock_price_df[
            ["stock_id", "Trading_Volume"]
        ]
        taiwan_stock_price_df = taiwan_stock_price_df[
            taiwan_stock_price_df["Trading_Volume"] > 0
        ]
        stock_info = stock_info.merge(
            taiwan_stock_price_df, how="inner", on=["stock_id"]
        )
        return stock_info["stock_id"].unique().tolist()


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
