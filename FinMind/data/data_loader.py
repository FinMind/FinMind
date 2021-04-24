import pandas as pd

from FinMind.data.finmind_api import FinMindApi


class DataLoader(FinMindApi):
    def __init__(self):
        super(DataLoader, self).__init__()

    def taiwan_stock_info(self):
        """
        @return: 台股總覽
        """
        stock_info = self.get_data(dataset="TaiwanStockInfo",)
        return stock_info

    def taiwan_stock_daily(
        self, stock_id: str, start_date: str, end_date: str
    ) -> pd.DataFrame:
        """
        @param stock_id: 股票代號("2330")
        @param start_date: 開始日期("2018-01-01")
        @param end_date: 結束日期("2021-03-06")
        @return: 股價
        """
        stock_price = self.get_data(
            dataset="TaiwanStockPrice",
            data_id=stock_id,
            start_date=start_date,
            end_date=end_date,
        )
        return stock_price

    def taiwan_stock_daily_adj(
        self, stock_id: str, start_date: str, end_date: str
    ) -> pd.DataFrame:
        """
        @param stock_id: 股票代號("2330")
        @param start_date: 開始日期("2018-01-01")
        @param end_date: 結束日期("2021-03-06")
        @return: 還原股價
        """
        stock_price = self.get_data(
            dataset="TaiwanStockPrice",
            data_id=stock_id,
            start_date=start_date,
            end_date=end_date,
        )
        ex_dividend_price = self.get_data(
            dataset="TaiwanStockDividendResult",
            data_id=stock_id,
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
                stock_price[stock_price["date"] == ex_dividend_date][
                    "retroactive_close"
                ].iloc[0]
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
        return stock_price

    def taiwan_stock_tick(self, stock_id: str, date: str) -> pd.DataFrame:
        """
        @param stock_id: 股票代號("2330")
        @param date: 資料日期 ("2021-03-06")
        @return: 當日成交明細
        """
        stock_tick = self.get_data(
            dataset="TaiwanStockPriceTick", data_id=stock_id, start_date=date,
        )
        return stock_tick

    def taiwan_stock_tick_timely(self, stock_id: str) -> pd.DataFrame:
        """
        @param stock_id: 股票代號("2330")
        @return: 最新 100 筆成交資料
        """
        stock_tick = self.get_data(
            dataset="TaiwanStockPriceTick",
            data_id=stock_id,
            streaming_all_data=True,
        )
        return stock_tick

    def taiwan_stock_bid_ask(self, stock_id: str, date: str) -> pd.DataFrame:
        """
        @param stock_id: 股票代號("2330")
        @param date: 資料日期 ("2021-03-06")
        @return: 當日五檔明細
        """
        bid_ask = self.get_data(
            dataset="TaiwanStockPriceBidAsk", data_id=stock_id, start_date=date,
        )
        return bid_ask

    def taiwan_stock_bid_ask_timely(self, stock_id: str) -> pd.DataFrame:
        """
        @param stock_id: 股票代號("2330")
        @return: 當前最佳五檔
        """
        bid_ask = self.get_data(
            dataset="TaiwanStockPriceBidAsk", data_id=stock_id,
        )
        return bid_ask

    def taiwan_stock_book_and_trade(
        self, stock_id: str, date: str
    ) -> pd.DataFrame:
        """
        @param stock_id: 股票代號("2330")
        @param date: 資料日期 ("2021-03-06")
        @return: 當日每五秒委託與成交資料
        """
        stock_book_and_trade = self.get_data(
            dataset="TaiwanStockPriceBidAsk", start_date=date, data_id=stock_id,
        )
        return stock_book_and_trade

    def tse(self, start_date: str, end_date: str):
        """
        @param start_date: 開始日期("2018-01-01")
        @param end_date: 結束日期("2021-03-06")
        @return: 台灣加權指數
        """
        tse = self.get_data(
            dataset="TaiwanVariousIndicators5Seconds",
            start_date=start_date,
            end_date=end_date,
        )
        return tse

    def taiwan_stock_day_trading(
        self, stock_id: str, start_date: str, end_date: str
    ):
        """
        @param stock_id: 股票代號("2330")
        @param start_date: 開始日期("2018-01-01")
        @param end_date: 結束日期("2021-03-06")
        @return: 台灣加權指數
        """
        stock_day_trading = self.get_data(
            dataset="TaiwanStockDayTrading",
            stock_id=stock_id,
            start_date=start_date,
            end_date=end_date,
        )
        return stock_day_trading

    def taiwan_stock_per_pbr(self, stock_id: str, start_date: str):
        """
        @param stock_id: 股票代號("2330")
        @param start_date: 資料起始日期("2018-01-01")
        @return: 股票市盈率PER 市淨率PBR
        """
        stock_per_pbr = self.get_data(
            dataset="TaiwanStockPER", stock_id=stock_id, start_date=start_date,
        )
        return stock_per_pbr

    def taiwan_stock_margin(self, stock_id: str, start_date: str):
        """
        @param stock_id: 股票代號("2330")
        @param start_date: 資料起始日期("2018-01-01")
        @return: 個股融資融券
        """
        stock_margin = self.get_data(
            dataset="TaiwanStockMarginPurchaseShortSale",
            stock_id=stock_id,
            start_date=start_date,
        )
        return stock_margin

    def taiwan_stock_margin_total(self, start_date: str):
        """
        @param start_date: 資料起始日期("2018-01-01")
        @return: 總體融資融券
        """
        stock_margin_total = self.get_data(
            dataset="TaiwanStockTotalMarginPurchaseShortSale",
            start_date=start_date,
        )
        return stock_margin_total

    def taiwan_stock_institutional_investors(
        self, stock_id: str, start_date: str
    ):
        """
        @param stock_id: 股票代號("2330")
        @param start_date: 資料起始日期("2018-01-01")
        @return: 法人買賣超
        """
        stock_institutional_investors = self.get_data(
            dataset="TaiwanStockInstitutionalInvestorsBuySell",
            stock_id=stock_id,
            start_date=start_date,
        )
        return stock_institutional_investors

    def taiwan_stock_institutional_investors_total(self, start_date: str):
        """
        @param start_date: 資料起始日期("2018-01-01")
        @return: 總體法人買賣超
        """
        stock_institutional_investors_total = self.get_data(
            dataset="TaiwanStockTotalInstitutionalInvestors",
            start_date=start_date,
        )
        return stock_institutional_investors_total

    def taiwan_stock_shareholding(self, stock_id: str, start_date: str):
        """
        @param stock_id: 股票代號("2330")
        @param start_date: 資料起始日期("2018-01-01")
        @return: 股東結構表
        """
        stock_shareholding = self.get_data(
            dataset="TaiwanStockShareholding",
            stock_id=stock_id,
            start_date=start_date,
        )
        return stock_shareholding

    def taiwan_stock_shareholding_class(self, stock_id: str, start_date: str):
        """
        @param stock_id: 股票代號("2330")
        @param start_date: 資料起始日期("2018-01-01")
        @return: 股東持股分級
        """
        stock_shareholding_class = self.get_data(
            dataset="TaiwanStockHoldingSharesPer",
            stock_id=stock_id,
            start_date=start_date,
        )
        return stock_shareholding_class

    def taiwan_stock_securities_lending(self, stock_id: str, start_date: str):
        """
        @param stock_id: 股票代號("2330")
        @param start_date: 資料起始日期("2018-01-01")
        @return: 股東持股分級
        """
        stock_securities_lending = self.get_data(
            dataset="TaiwanStockSecuritiesLending",
            stock_id=stock_id,
            start_date=start_date,
        )
        return stock_securities_lending
