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
        :rtype column industry_category (str): 產業別
        :rtype column stock_id (str): 股票代碼
        :rtype column stock_name (str): 股票名稱
        :rtype column type (str): 市場別
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
        :rtype column industry_category (str): 產業別
        :rtype column stock_id (str): 股票代碼
        :rtype column stock_name (str): 股票名稱
        :rtype column type (str): 市場別
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
        :rtype column securities_trader_id (str): 券商代碼
        :rtype column securities_trader (str): 券商名稱
        :rtype column date (str): 開業日
        :rtype column address (str): 地址
        :rtype column phone (str): 電話
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
        :rtype column date (str): 日期
        :rtype column stock_id (str): 股票代碼
        :rtype column Trading_Volume (int): 成交量
        :rtype column Trading_money (int): 成交金額
        :rtype column open (float): 開盤價
        :rtype column max (float): 最高價
        :rtype column min (float): 最低價
        :rtype column close (float): 收盤價
        :rtype column spread (float): 漲跌幅
        :rtype column Trading_turnover (float): 交易筆數
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
        :rtype column date (str): 日期
        :rtype column stock_id (str): 股票代碼
        :rtype column deal_price (float): 成交價
        :rtype column volume (int): 成交量
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
        :rtype column date (str): 日期
        :rtype column stock_id (str): 股票代碼
        :rtype column dividend_yield (float): 殖利率
        :rtype column PER (float): 本益比
        :rtype column PBR (float): 股價淨值比
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
        :rtype column Time (str): 時間
        :rtype column TotalBuyOrder (int): 累積委託買進筆數
        :rtype column TotalBuyVolume (int): 累積委託買進數量
        :rtype column TotalSellOrder (int): 累積委託賣出筆數
        :rtype column TotalSellVolume (int): 累積委託賣出數量
        :rtype column TotalDealOrder (int): 累積成交筆數
        :rtype column TotalDealVolume (int): 累積成交數量
        :rtype column TotalDealMoney (int): 累積成交金額
        :rtype column date (str): 日期
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
        :rtype column date (str): 日期
        :rtype column TAIEX (float): 加權指數
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
        :rtype column stock_id (str): 股票代碼
        :rtype column date (str): 日期
        :rtype column BuyAfterSale (str): 可否當沖
        :rtype column Volume (int): 成交量
        :rtype column BuyAmount (int): 買進金額
        :rtype column SellAmount (int): 賣出金額
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
        :rtype column stock_id (str): 股票代碼
        :rtype column date (str): 日期
        :rtype column buy_amount (int): 買進金額
        :rtype column sell_amount (int): 買出金額
        :rtype column buy (int): 買進股數
        :rtype column sell (int): 賣出股數
        :rtype column bank_name (str): 銀行名稱
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
        :rtype column date (str): 日期
        :rtype column stock_id (str): 股票代碼
        :rtype column MarginPurchaseBuy (int): 融資買進
        :rtype column MarginPurchaseCashRepayment (int): 融資現金償還
        :rtype column MarginPurchaseLimit (int): 融資限額
        :rtype column MarginPurchaseSell (int): 融資賣出
        :rtype column MarginPurchaseTodayBalance (int): 融資今日餘額
        :rtype column MarginPurchaseYesterdayBalance (int): 融資昨日餘額
        :rtype column Note (str): 註記
        :rtype column OffsetLoanAndShort (int): 資券互抵
        :rtype column ShortSaleBuy (int): 融券買進
        :rtype column ShortSaleCashRepayment (int): 融券償還
        :rtype column ShortSaleLimit (int): 融券限額
        :rtype column ShortSaleSell (int): 融券賣出
        :rtype column ShortSaleTodayBalance (int): 融券今日餘額
        :rtype column ShortSaleYesterdayBalance (int): 融券昨日餘額
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
        :rtype column TodayBalance (int): 今日餘額
        :rtype column YesBalance (int): 昨日餘額
        :rtype column buy (int): 買進
        :rtype column date (str): 日期
        :rtype column name (str): 種類
        :rtype column Return (int): 現金/券償還
        :rtype column sell (int): 賣出
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
        :rtype column date (str): 日期
        :rtype column stock_id (str): 股票代碼
        :rtype column buy (int): 買進
        :rtype column name (str): 類別
        :rtype column sell (int): 賣出
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
        :rtype column date (str): 日期
        :rtype column buy (int): 買進
        :rtype column name (str): 種類
        :rtype column sell (int): 賣出
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
        :rtype column date (str): 日期
        :rtype column stock_id (str): 股票代碼
        :rtype column stock_name (str): 股票名稱
        :rtype column InternationalCode (str): 國際股票編碼
        :rtype column ForeignInvestmentRemainingShares (int): 外資尚可投資股數
        :rtype column ForeignInvestmentShares (int): 外資持有股數
        :rtype column ForeignInvestmentRemainRatio (float): 外資尚可投資比例
        :rtype column ForeignInvestmentSharesRatio (float): 外資持股比例
        :rtype column ForeignInvestmentUpperLimitRatio (float): 外資投資上限
        :rtype column ChineseInvestmentUpperLimitRatio (float): 陸資投資上限
        :rtype column NumberOfSharesIssued (int): 發行股數
        :rtype column RecentlyDeclareDate (str): 最近一次異動申報日期
        :rtype column note (str): 註
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
        :rtype column date (str): 日期
        :rtype column stock_id (str): 股票代碼
        :rtype column HoldingSharesLevel (str): 持股分級
        :rtype column people (int): 人數
        :rtype column percent (float): 比例
        :rtype column unit (int): 股數
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
        :rtype column date (str): 日期
        :rtype column stock_id (str): 股票代碼
        :rtype column transaction_type (str): 交易方式
        :rtype column volume (int): 成交量
        :rtype column fee_rate (float): 成交費率
        :rtype column close (float): 收盤價
        :rtype column original_return_date (str): 約定還券日期
        :rtype column original_lending_period (int): 約定借券天數
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
        :rtype column stock_id (str): 股票代碼
        :rtype column MarginShortSalesPreviousDayBalance (int): 前日餘額(融券)
        :rtype column MarginShortSalesShortSales (int): 賣出(融券)
        :rtype column MarginShortSalesShortCovering (int): 買進(融券)
        :rtype column MarginShortSalesStockRedemption (int): 現券(融券)
        :rtype column MarginShortSalesCurrentDayBalance (int): 今日餘額(融券)
        :rtype column MarginShortSalesQuota (int): 限額(融券)
        :rtype column SBLShortSalesPreviousDayBalance (int): 前日餘額(借券賣出)
        :rtype column SBLShortSalesShortSales (int): 賣出(借券賣出)
        :rtype column SBLShortSalesReturns (int): 還券(借券賣出)
        :rtype column SBLShortSalesAdjustments (int): 當日調整(借券賣出)
        :rtype column SBLShortSalesCurrentDayBalance (int): 當日餘額(借券賣出)
        :rtype column SBLShortSalesQuota (int): 限額(借券賣出)
        :rtype column SBLShortSalesShortCovering (int): 庫存異動(借券賣出)
        :rtype column date (str): 日期
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
        :rtype column date (str): 日期
        :rtype column stock_id (str): 股票代碼
        :rtype column type (str): 類別
        :rtype column value (float): 數值
        :rtype column origin_name (str): 原始名稱
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
        :rtype column date (str): 日期
        :rtype column stock_id (str): 股票代碼
        :rtype column type (str): 類別
        :rtype column value (float): 數值
        :rtype column origin_name (str): 原始名稱
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
        :rtype column date (str): 日期
        :rtype column stock_id (str): 股票代碼
        :rtype column type (str): 類別
        :rtype column value (float): 數值
        :rtype column origin_name (str): 原始名稱
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
        :rtype column date (str): 權利分派基準日
        :rtype column stock_id (str): 股票代碼
        :rtype column year (str): 股利所屬年度
        :rtype column StockEarningsDistribution (float): 股票股利:盈餘轉增資配股
        :rtype column StockStatutorySurplus (float): 股票股利:法定盈餘公積資本公積轉增資配股
        :rtype column StockExDividendTradingDate (str): 除權交易日
        :rtype column TotalEmployeeStockDividend (float): 員工配股
        :rtype column TotalEmployeeStockDividendAmount (float): 員工配股金額
        :rtype column RatioOfEmployeeStockDividendOfTotal (float): 配股總股數佔盈餘配股總股數之比例
        :rtype column RatioOfEmployeeStockDividend (float): 員工紅利配股率
        :rtype column CashEarningsDistribution (float): 現金股利:盈餘轉增資配股
        :rtype column CashStatutorySurplus (float): 現金股利:法定盈餘公積資本公積轉增資配股
        :rtype column CashExDividendTradingDate (str): 除息交易日
        :rtype column CashDividendPaymentDate (str): 現金股利發放日
        :rtype column TotalEmployeeCashDividend (float): 員工紅利總金額
        :rtype column TotalNumberOfCashCapitalIncrease (float): 現金增資總股數
        :rtype column CashIncreaseSubscriptionRate (float): 現金增資認股比率
        :rtype column CashIncreaseSubscriptionpRrice (float): 現金增資認購價
        :rtype column RemunerationOfDirectorsAndSupervisors (float): 董監酬勞
        :rtype column ParticipateDistributionOfTotalShares (float): 參加分派總股數
        :rtype column AnnouncementDate (str): 公告日期
        :rtype column AnnouncementTime (str): 公告時間
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
        :rtype column date (str): 日期
        :rtype column stock_id (str): 股票代碼
        :rtype column before_price (float): 除權息前收盤價
        :rtype column after_price (float): 除權息後收盤價
        :rtype column stock_and_cache_dividend (float): 權息值
        :rtype column stock_or_cache_dividend (str): 權/息
        :rtype column max_price (float): 漲停價格
        :rtype column min_price (float): 跌停價格
        :rtype column open_price (float): 開盤價
        :rtype column reference_price (float): 減除股利參考價
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
        :rtype column date (str): 日期
        :rtype column stock_id (str): 股票代碼
        :rtype column country (str): 國家
        :rtype column revenue (int): 營收
        :rtype column revenue_month (int): 營收月份
        :rtype column revenue_year (int): 營收年份
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
        :rtype column rank (int): 排名
        :rtype column stock_id (str): 股票代碼
        :rtype column stock_name (str): 股票名稱
        :rtype column weight_per (float): 權重百分比
        :rtype column date (str): 日期
        :rtype column type (str): 上市(twse)/上櫃(tpex)
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
        :rtype column code (str): 代碼
        :rtype column callput (str): 買賣權
        :rtype column date (str): 日期
        :rtype column name (str): 名稱
        :rtype column listing_date (str): 上市日
        :rtype column update_date (str): 更新日期
        :rtype column expire_price (float): 履約價
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
        :rtype column date (str): 日期
        :rtype column Time (str): 時間
        :rtype column Close (List[float]): 成交價
        :rtype column Volume (List[int]): 成交量
        :rtype column futopt_id (str): 期貨選擇權代碼
        :rtype column TickType (int): 成交種類
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
        :rtype column code (str): 商品代碼
        :rtype column type (str): 種類
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
        :rtype column date (str): 日期
        :rtype column future_id (str): 期貨代碼
        :rtype column contract_date (str): 到期月份
        :rtype column open (float): 開盤價
        :rtype column max (float): 最高價
        :rtype column min (float): 最低價
        :rtype column close (float): 收盤價
        :rtype column spread (float): 漲跌幅
        :rtype column spread_per (float): 漲跌幅比例
        :rtype column volume (int): 成交量
        :rtype column settlement_price (float): 結算價
        :rtype column open_interest (int): 未沖銷契約量
        :rtype column trading_session (str): 交易時段
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
        :rtype column date (str): 日期
        :rtype column option_id (str): 選擇權代碼
        :rtype column contract_date (str): 到期月份
        :rtype column strike_price (float): 履約價
        :rtype column call_put (str): 買賣權
        :rtype column open (float): 開盤價
        :rtype column max (float): 最高價
        :rtype column min (float): 最低價
        :rtype column close (float): 收盤價
        :rtype column volume (int): 成交量
        :rtype column settlement_price (float): 結算價
        :rtype column open_interest (int): 未平倉合約
        :rtype column trading_session (str): 交易時段
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
        :rtype column name (str): 商品名稱
        :rtype column contract_type (str): 到期月份
        :rtype column buy_top5_trader_open_interest (float): 買方前五大交易人合計部位數
        :rtype column buy_top5_trader_open_interest_per (float): 買方前五大交易人合計百分比
        :rtype column buy_top10_trader_open_interest (float): 買方前十大交易人合計部位數
        :rtype column buy_top10_trader_open_interest_per (float): 買方前十大交易人合計百分比
        :rtype column sell_top5_trader_open_interest (float): 賣方前五大交易人合計部位數
        :rtype column sell_top5_trader_open_interest_per (float): 賣方前五大交易人合計百分比
        :rtype column sell_top10_trader_open_interest (float): 賣方前十大交易人合計部位數
        :rtype column sell_top10_trader_open_interest_per (float): 賣方前十大交易人合計百分比
        :rtype column market_open_interest (int): 全市場未沖銷部位數
        :rtype column buy_top5_specific_open_interest (float): 買方前五大特定法人合計部位數
        :rtype column buy_top5_specific_open_interest_per (float): 買方前五大特定法人合計百分比
        :rtype column buy_top10_specific_open_interest (float): 買方前十大特定法人合計部位數
        :rtype column buy_top10_specific_open_interest_per (float): 買方前十大特定法人合計百分比
        :rtype column sell_top5_specific_open_interest (float): 賣方前五大特定法人合計部位數
        :rtype column sell_top5_specific_open_interest_per (float): 賣方前五大特定法人合計百分比
        :rtype column sell_top10_specific_open_interest (float): 賣方前十大特定法人合計部位數
        :rtype column sell_top10_specific_open_interest_per (float): 賣方前十大特定法人合計百分比
        :rtype column date (str): 日期
        :rtype column futures_id (str): 期貨代碼
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
        :rtype column contract_type (str): 到期月份
        :rtype column buy_top5_trader_open_interest (float): 買方前五大交易人合計部位數
        :rtype column buy_top5_trader_open_interest_per (float): 買方前五大交易人合計百分比
        :rtype column buy_top10_trader_open_interest (float): 買方前十大交易人合計部位數
        :rtype column buy_top10_trader_open_interest_per (float): 買方前十大交易人合計百分比
        :rtype column sell_top5_trader_open_interest (float): 賣方前五大交易人合計部位數
        :rtype column sell_top5_trader_open_interest_per (float): 賣方前五大交易人合計百分比
        :rtype column sell_top10_trader_open_interest (float): 賣方前十大交易人合計部位數
        :rtype column sell_top10_trader_open_interest_per (float): 賣方前十大交易人合計百分比
        :rtype column market_open_interest (int): 全市場未沖銷部位數
        :rtype column buy_top5_specific_open_interest (float): 買方前五大特定法人合計部位數
        :rtype column buy_top5_specific_open_interest_per (float): 買方前五大特定法人合計百分比
        :rtype column buy_top10_specific_open_interest (float): 買方前十大特定法人合計部位數
        :rtype column buy_top10_specific_open_interest_per (float): 買方前十大特定法人合計百分比
        :rtype column sell_top5_specific_open_interest (float): 賣方前五大特定法人合計部位數
        :rtype column sell_top5_specific_open_interest_per (float): 賣方前五大特定法人合計百分比
        :rtype column sell_top10_specific_open_interest (float): 賣方前十大特定法人合計部位數
        :rtype column sell_top10_specific_open_interest_per (float): 賣方前十大特定法人合計百分比
        :rtype column date (str): 日期
        :rtype column put_call (str): 買賣權
        :rtype column name (str): 商品名稱
        :rtype column option_id (str): 選擇權代碼
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
        :rtype column contract_date (str): 到期月份
        :rtype column date (str): 日期
        :rtype column futures_id (str): 期貨代碼
        :rtype column price (float): 成交價
        :rtype column volume (int): 成交量
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
        :rtype column ExercisePrice (float): 履約價
        :rtype column PutCall (str): 買賣權
        :rtype column contract_date (str): 到期月份
        :rtype column date (str): 日期
        :rtype column option_id (str): 選擇權代碼
        :rtype column price (float): 成交價
        :rtype column volume (int): 成交量
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
        :rtype column name (str): 商品名稱
        :rtype column date (str): 日期
        :rtype column institutional_investors (str): 身分別
        :rtype column long_deal_volume (int): 多方口數
        :rtype column long_deal_amount (int): 多方契約金額
        :rtype column short_deal_volume (int): 空方口數
        :rtype column short_deal_amount (int): 空方契約金額
        :rtype column long_open_interest_balance_volume (int): 多方未平倉口數
        :rtype column long_open_interest_balance_amount (int): 多方未平倉契約金額
        :rtype column short_open_interest_balance_volume (int): 空方未平倉口數
        :rtype column short_open_interest_balance_amount (int): 空方未平倉契約金額
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
        :rtype column name (str): 商品名稱
        :rtype column date (str): 日期
        :rtype column institutional_investors (str): 身分別
        :rtype column long_deal_volume (int): 多方口數
        :rtype column long_deal_amount (int): 多方契約金額
        :rtype column short_deal_volume (int): 空方口數
        :rtype column short_deal_amount (int): 空方契約金額
        :rtype column long_open_interest_balance_volume (int): 多方未平倉口數
        :rtype column long_open_interest_balance_amount (int): 多方未平倉契約金額
        :rtype column short_open_interest_balance_volume (int): 空方未平倉口數
        :rtype column short_open_interest_balance_amount (int): 空方未平倉契約金額
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
        :rtype column name (str): 商品名稱
        :rtype column date (str): 日期
        :rtype column institutional_investors (str): 身分別
        :rtype column long_deal_volume (int): 多方口數
        :rtype column long_deal_amount (int): 多方契約金額
        :rtype column short_deal_volume (int): 空方口數
        :rtype column short_deal_amount (int): 空方契約金額
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
        :rtype column name (str): 商品名稱
        :rtype column date (str): 日期
        :rtype column institutional_investors (str): 身分別
        :rtype column long_deal_volume (int): 多方口數
        :rtype column long_deal_amount (int): 多方契約金額
        :rtype column short_deal_volume (int): 空方口數
        :rtype column short_deal_amount (int): 空方契約金額
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
        :rtype column date (str): 日期
        :rtype column dealer_code (str): 期貨商代碼
        :rtype column dealer_name (str): 期貨商名稱
        :rtype column futures_id (str): 期貨代碼
        :rtype column volume (int): 成交量
        :rtype column is_after_hour (str): 盤後交易
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
        :rtype column date (str): 日期
        :rtype column dealer_code (str): 期貨商代碼
        :rtype column dealer_name (str): 期貨商名稱
        :rtype column option_id (str): 選擇權代碼
        :rtype column volume (int): 成交量
        :rtype column is_after_hour (str): 盤後交易
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

    def taiwan_futures_final_settlement_price(
        self,
        futures_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
        use_async: bool = False,
        futures_id_list: typing.List[str] = None,
    ) -> pd.DataFrame:
        """get 期貨最後結算價
        :param futures_id: 期貨代號("TX")
        :param start_date (str): 起始日期("2024-01-01")
        :param end_date (str): 結束日期("2024-12-31")
        :param timeout (int): timeout seconds, default None

        :return: 期貨最後結算價 TaiwanFuturesFinalSettlementPrice
        :rtype pd.DataFrame
        :rtype column date (str): 到期日
        :rtype column contract_month (str): 契約月份
        :rtype column futures_type (str): 期貨類型
        :rtype column futures_id (str): 期貨代碼
        :rtype column futures_name (str): 期貨名稱
        :rtype column settlement_price (float): 最後結算價
        :rtype column underlying_code (str): 標的證券代號
        :rtype column notional_value (float): 約定標的物價值
        """
        futures_final_settlement_price = self.get_data(
            dataset=Dataset.TaiwanFuturesFinalSettlementPrice,
            data_id=futures_id,
            start_date=start_date,
            end_date=end_date,
            timeout=timeout,
            use_async=use_async,
            data_id_list=futures_id_list,
        )
        return futures_final_settlement_price

    def taiwan_futures_spread_trading(
        self,
        futures_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
        use_async: bool = False,
        futures_id_list: typing.List[str] = None,
    ) -> pd.DataFrame:
        """get 期貨價差行情表
        :param futures_id: 期貨代號("TX")
        :param start_date (str): 起始日期("2024-01-01")
        :param end_date (str): 結束日期("2024-12-31")
        :param timeout (int): timeout seconds, default None

        :return: 期貨價差行情表 TaiwanFuturesSpreadTrading
        :rtype pd.DataFrame
        :rtype column date (str): 日期
        :rtype column futures_id (str): 期貨代碼
        :rtype column contract_date (str): 到期月份
        :rtype column open (float): 開盤價
        :rtype column max (float): 最高價
        :rtype column min (float): 最低價
        :rtype column close (float): 收盤價
        :rtype column best_bid (float): 最佳買價
        :rtype column best_ask (float): 最佳賣價
        :rtype column historical_max (float): 歷史最高價
        :rtype column historical_min (float): 歷史最低價
        :rtype column spread_to_spread_volume (float): 價差對價差成交量
        :rtype column spread_to_single_volume (float): 價差對單式成交量
        :rtype column trading_session (str): 交易時段
        """
        futures_spread_trading = self.get_data(
            dataset=Dataset.TaiwanFuturesSpreadTrading,
            data_id=futures_id,
            start_date=start_date,
            end_date=end_date,
            timeout=timeout,
            use_async=use_async,
            data_id_list=futures_id_list,
        )
        return futures_spread_trading

    def taiwan_option_final_settlement_price(
        self,
        option_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
        use_async: bool = False,
        option_id_list: typing.List[str] = None,
    ) -> pd.DataFrame:
        """get 選擇權最後結算價
        :param option_id: 選擇權代號("TXO")
        :param start_date (str): 起始日期("2024-01-01")
        :param end_date (str): 結束日期("2024-12-31")
        :param timeout (int): timeout seconds, default None

        :return: 選擇權最後結算價 TaiwanOptionFinalSettlementPrice
        :rtype pd.DataFrame
        :rtype column date (str): 到期日
        :rtype column contract_month (str): 契約月份
        :rtype column option_type (str): 選擇權類型
        :rtype column option_id (str): 選擇權代碼
        :rtype column option_name (str): 選擇權名稱
        :rtype column settlement_price (float): 最後結算價
        :rtype column underlying_code (str): 標的證券代號
        :rtype column notional_value (float): 約定標的物價值
        """
        option_final_settlement_price = self.get_data(
            dataset=Dataset.TaiwanOptionFinalSettlementPrice,
            data_id=option_id,
            start_date=start_date,
            end_date=end_date,
            timeout=timeout,
            use_async=use_async,
            data_id_list=option_id_list,
        )
        return option_final_settlement_price

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
        :rtype column date (str): 日期
        :rtype column stock_id (str): 股票代碼
        :rtype column description (str): 描述
        :rtype column link (str): 連結
        :rtype column source (str): 來源
        :rtype column title (str): 標題
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
        :rtype column price (float): 報酬指數
        :rtype column stock_id (str): 指數代碼
        :rtype column date (str): 日期
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
        :rtype column date (str): 日期
        :rtype column stock_id (str): 股票代碼
        :rtype column ClosingPriceonTheLastTradingDay (float): 停止買賣前收盤價格
        :rtype column PostReductionReferencePrice (float): 恢復買賣參考價
        :rtype column LimitUp (float): 漲停價格
        :rtype column LimitDown (float): 跌停價格
        :rtype column OpeningReferencePrice (float): 開盤競價基準
        :rtype column ExrightReferencePrice (float): 除權參考價
        :rtype column ReasonforCapitalReduction (str): 減資原因
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
        :rtype column date (str): 日期
        :rtype column stock_id (str): 股票代碼
        :rtype column market_value (float): 市值
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
        :rtype column date (str): 日期
        :rtype column stock_id (str): 股票代碼
        :rtype column close (float): 股價
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
        :rtype column stock_id (str): 股票代碼
        :rtype column yweek (str): 週日期
        :rtype column max (float): 最高價
        :rtype column min (float): 最低價
        :rtype column trading_volume (int)): 成交量
        :rtype column trading_money (int): 成交金額
        :rtype column trading_turnover (int): 交易筆數
        :rtype column date (str): 日期
        :rtype column close (float): 收盤價
        :rtype column open (float): 開盤價
        :rtype column spread (float): 漲跌幅
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
        :rtype column stock_id (str): 股票代碼
        :rtype column ymonth (str): 月日期
        :rtype column max (float): 最高價
        :rtype column min (float): 最低價
        :rtype column trading_volume (int)): 成交量
        :rtype column trading_money (int): 成交金額
        :rtype column trading_turnover (int): 交易筆數
        :rtype column date (str): 日期
        :rtype column close (float): 收盤價
        :rtype column open (float): 開盤價
        :rtype column spread (float): 漲跌幅
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
        :rtype column date (str): 日期
        :rtype column minute (str): 分
        :rtype column stock_id (str): 股票代碼
        :rtype column open (float): 開盤價
        :rtype column high (float): 最高價
        :rtype column low (float): 最低價
        :rtype column close (float): 收盤價
        :rtype column volume (int): 成交量
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
        :rtype column date (str): 日期
        :rtype column stock_id (str): 股票代碼
        :rtype column stock_name (str): 股票名稱
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
        :rtype column date (str): 日期
        :rtype column TotalExchangeMarginMaintenance (float): 大盤融資維持率
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
        :rtype column date (str): 日期
        :rtype column stock_id (str): 股票代碼
        :rtype column Country (str): 國家
        :rtype column IPOYear (str): IPOYear
        :rtype column MarketCap (str): 市值
        :rtype column Subsector (str): 類別
        :rtype column stock_name (str): 股票名稱
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
        :rtype column date (str): 日期
        :rtype column stock_id (str): 股票代碼
        :rtype column Adj_Close (float): 調整股價
        :rtype column Close (float): 收盤價
        :rtype column High (float): 最高價
        :rtype column Low (float): 最低價
        :rtype column Open (float): 開盤價
        :rtype column Volume (int): 成交量
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
        :rtype column open (float): 開盤價
        :rtype column high (float): 最高價
        :rtype column low (float): 最低價
        :rtype column close (float): 最新成交價
        :rtype column change_price (float): 漲跌
        :rtype column change_rate (float): 漲跌百分比
        :rtype column average_price (float): 平均成交價
        :rtype column volume (int): 成交量
        :rtype column total_volume (int): 累積成交量
        :rtype column amount (int): 交易金額
        :rtype column total_amount (int): 累積交易金額
        :rtype column yesterday_volume (int): 昨日成交量
        :rtype column buy_price (float): 買入價
        :rtype column buy_volume (int): 買入量
        :rtype column sell_price (float): 賣出價
        :rtype column sell_volume (int): 賣出量
        :rtype column volume_ratio (float): 昨日與今日成交量比
        :rtype column date (str): 成交時間
        :rtype column stock_id (str): 股票代碼
        :rtype column TickType (int): 成交種類
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
        :rtype column open (float): 開盤價
        :rtype column high (float): 最高價
        :rtype column low (float): 最低價
        :rtype column close (float): 最新成交價
        :rtype column change_price (float): 漲跌
        :rtype column change_rate (float): 漲跌百分比
        :rtype column average_price (float): 平均成交價
        :rtype column volume (int): 成交量
        :rtype column total_volume (int): 累積成交量
        :rtype column amount (int): 交易金額
        :rtype column total_amount (int): 累積交易金額
        :rtype column yesterday_volume (int): 昨日成交量
        :rtype column buy_price (float): 買入價
        :rtype column buy_volume (int): 買入量
        :rtype column sell_price (float): 賣出價
        :rtype column sell_volume (int): 賣出量
        :rtype column volume_ratio (float): 昨日與今日成交量比
        :rtype column date (str): 成交時間
        :rtype column futures_id (str): 期貨代碼
        :rtype column TickType (int): 成交種類
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
        :rtype column open (float): 開盤價
        :rtype column high (float): 最高價
        :rtype column low (float): 最低價
        :rtype column close (float): 最新成交價
        :rtype column change_price (float): 漲跌
        :rtype column change_rate (float): 漲跌百分比
        :rtype column average_price (float): 平均成交價
        :rtype column volume (int): 成交量
        :rtype column total_volume (int): 累積成交量
        :rtype column amount (int): 交易金額
        :rtype column total_amount (int): 累積交易金額
        :rtype column yesterday_volume (int): 昨日成交量
        :rtype column buy_price (float): 買入價
        :rtype column buy_volume (int): 買入量
        :rtype column sell_price (float): 賣出價
        :rtype column sell_volume (int): 賣出量
        :rtype column volume_ratio (float): 昨日與今日成交量比
        :rtype column date (str): 成交時間
        :rtype column options_id (str): 選擇權代碼
        :rtype column TickType (int): 成交種類
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
        :rtype column cb_id (str): 可轉債代碼
        :rtype column cb_name (str): 可轉債名稱
        :rtype column InitialDateOfConversion (str): 轉換起日
        :rtype column DueDateOfConversion (str): 轉換迄日
        :rtype column IssuanceAmount (int): 原始發行總額
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
        :rtype column cb_id: (str): 可轉債代碼
        :rtype column cb_name: (str): 可轉債名稱
        :rtype column transaction_type: (str): 交易狀態
        :rtype column close: (float): 收盤價
        :rtype column change: (float): 漲跌幅
        :rtype column open: (float): 開盤價
        :rtype column max: (float): 最高價
        :rtype column min: (float): 最低價
        :rtype column no_of_transactions: (int): 交易筆數
        :rtype column unit: (int): 成交量
        :rtype column trading_value: (int): 成交金額
        :rtype column avg_price: (float): 成交均價
        :rtype column next_ref_price: (float): 明日參考價
        :rtype column next_max_limit: (float): 明日漲停價
        :rtype column next_min_limit: (float): 明日跌停價
        :rtype column date: (str): 日期
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
        :rtype column Foreign_Investor_Buy: (int): 外資買入數量
        :rtype column Foreign_Investor_Sell: (int): 外資賣出數量
        :rtype column Foreign_Investor_Overbuy: (int): 外資買超數量
        :rtype column Investment_Trust_Buy: (int): 投信買入數量
        :rtype column Investment_Trust_Sell: (int): 投信賣出數量
        :rtype column Investment_Trust_Overbuy: (int): 投信買超數量
        :rtype column Dealer_self_Buy: (int): 自營商買入數量
        :rtype column Dealer_self_Sell: (int): 自營商賣出數量
        :rtype column Dealer_self_Overbuy: (int): 自營商買超數量
        :rtype column Total_Overbuy: (int): 總買超數量
        :rtype column cb_id: (str): 可轉債代碼
        :rtype column cb_name: (str): 可轉債名稱
        :rtype column date: (str): 日期
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
        :rtype column cb_id: (str): 可轉債代碼
        :rtype column cb_name: (str): 可轉債名稱
        :rtype column date: (str): 日期
        :rtype column InitialDateOfConversion: (str): 轉換起日
        :rtype column DueDateOfConversion: (str): 轉換迄日
        :rtype column InitialDateOfStopConversion: (str): 最近停止轉換起日
        :rtype column DueDateOfStopConversion: (str): 最近停止轉換迄日
        :rtype column ConversionPrice: (float): 轉換價格
        :rtype column NextEffectiveDateOfConversionPrice: (str): 下次轉換價格生效日期
        :rtype column LatestInitialDateOfPut: (str): 最近賣回權起日
        :rtype column LatestDueDateOfPut: (str): 最近賣回權迄日
        :rtype column LatestPutPrice: (float): 最近賣回權價格
        :rtype column InitialDateOfEarlyRedemption: (str): 強制贖回起日
        :rtype column DueDateOfEarlyRedemption: (str): 強制贖回迄日
        :rtype column EarlyRedemptionPrice: (float): 強制贖回價格
        :rtype column DateOfDelisted: (str): 終止櫃檯買賣日
        :rtype column IssuanceAmount: (float): 原始發行總額
        :rtype column OutstandingAmount: (float): 上月底發行餘額
        :rtype column ReferencePrice: (float): 轉債參考價格
        :rtype column PriceOfUnderlyingStock: (float): 轉換標的股票價格
        :rtype column InitialDateOfSuspension: (str): 停止交易起日
        :rtype column DueDateOfSuspension: (str): 停止交易迄日
        :rtype column CouponRate: (float): 票面利率
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
        :rtype column stock_id: (str): 股票代碼
        :rtype column date: (str): 開始日期
        :rtype column end_date: (str): 結束日期
        :rtype column reason: (str): 停券原因
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
        :rtype column securities_trader (str): 券商名稱
        :rtype column price (float): 成交價
        :rtype column buy (int): 買進股數
        :rtype column sell (int): 賣出股數
        :rtype column securities_trader_id (str): 券商代碼
        :rtype column stock_id (str): 股票代碼
        :rtype column date (str): 日期
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
        :rtype column securities_trader (str): 券商名稱
        :rtype column price (float): 成交價
        :rtype column buy (int): 買進股數
        :rtype column sell (int): 賣出股數
        :rtype column securities_trader_id (str): 券商代碼
        :rtype column stock_id (str): 股票代碼
        :rtype column date (str): 日期
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
        :rtype column securities_trader (str): 券商名稱
        :rtype column securities_trader_id (str): 券商代碼
        :rtype column stock_id (str): 股票代碼
        :rtype column date (str): 日期
        :rtype column buy_volume (int): 買進總股數
        :rtype column sell_volume (int): 賣出總股數
        :rtype column buy_price (float): 買進均價
        :rtype column sell_price (float): 賣出均價
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
        :rtype column date (str): 日期
        :rtype column leading (float): 領先指標綜合指數
        :rtype column leading_notrend (float): 領先指標不含趨勢指數
        :rtype column coincident (float): 同時指標綜合指數
        :rtype column coincident_notrend (float): 同時指標不含趨勢指數
        :rtype column lagging (float): 落後指標綜合指數
        :rtype column lagging_notrend (float): 落後指標不含趨勢指數
        :rtype column monitoring (float): 景氣對策信號綜合分數
        :rtype column monitoring_color (str): 景氣對策信號
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
        :rtype column date (str): 公布日期
        :rtype column stock_id (str): 股票代碼
        :rtype column stock_name (str): 股票名稱
        :rtype column disposition_cnt (int): 累計次數
        :rtype column condition (str): 處置條件
        :rtype column measure (str): 處置內容
        :rtype column period_start (str): 處置開始日期
        :rtype column period_end (str): 處置結束日期
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
        :rtype column stock_id (str): 股票代碼
        :rtype column industry (str): 所屬產業
        :rtype column sub_industry (str): 子類別
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
        :rtype column date (str): 日期
        :rtype column fear_greed (str): 恐懼貪婪指數
        :rtype column fear_greed_emotion (str): 恐懼貪婪情緒
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
        :rtype column date (str): 日期
        :rtype column time (str): 時間
        :rtype column stock_id (str): 產業代碼
        :rtype column price (float): 價格
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
        :rtype column date (str): 交易日期
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
        :rtype column stock_id (str): 股票代碼
        :rtype column date (str): 上市日期
        :rtype column close (float): 收盤價
        :rtype column target_stock_id (str): 標的股票代碼
        :rtype column target_close (float): 標的收盤價
        :rtype column type (str): 權證類型
        :rtype column fulfillment_method (str): 履約方式
        :rtype column end_date (str): 最後交易日
        :rtype column fulfillment_start_date (str): 履約開始日
        :rtype column fulfillment_end_date (str): 履約截止日
        :rtype column exercise_ratio (float): 行使比例
        :rtype column fulfillment_price (float): 履約價格
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
        :rtype column date (str): 分割日期
        :rtype column stock_id (str): 股票代碼
        :rtype column type (str): 分割類型
        :rtype column before_price (float): 分割前價格
        :rtype column after_price (float): 分割後價格
        :rtype column max_price (float): 分割後最高價
        :rtype column min_price (float): 分割後最低價
        :rtype column open_price (float): 分割後開盤價
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
        :rtype column date (str): 日期
        :rtype column stock_id (str): 股票代碼
        :rtype column stock_name (str): 股票名稱
        :rtype column before_close (float): 停止買賣前收盤價格
        :rtype column after_ref_close (float): 恢復買賣參考價
        :rtype column after_ref_max (float): 漲停價格
        :rtype column after_ref_min (float): 跌停價格
        :rtype column after_ref_open (float): 開盤競價基準
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
        :rtype column date (str): 暫停交易日期
        :rtype column stock_id (str): 股票代碼
        :rtype column suspension_time (str): 暫停交易時間
        :rtype column resumption_date (str): 恢復交易日期
        :rtype column resumption_time (str): 恢復交易時間
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
        :rtype column stock_id (str): 股票代碼
        :rtype column date (str): 停止先賣後買開始日
        :rtype column end_date (str): 停止先賣後買結束日
        :rtype column reason (str): 原因
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
