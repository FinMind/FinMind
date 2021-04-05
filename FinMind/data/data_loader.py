import pandas as pd
from FinMind.schema.data import Version
from FinMind.data.finmind_api import FinMindApi


class DataLoader(FinMindApi):
    def __init__(self):
        super(DataLoader, self).__init__()

    def stock_adj_price(
        self, stock_id: str = "", start_date: str = "", end_date: str = "",
    ) -> pd.DataFrame:
        """
        @param stock_id: 股票代號("2330")
        @param start_date: 開始日期("2019-04-01")
        @param end_date: 結束日期("2021-03-06")
        @return: 還原股價
        """
        self.set_api_version(version=Version.V3)
        stock_price = self.get_data(
            dataset="TaiwanStockPrice",
            data_id=stock_id,
            start_date=start_date,
            end_date=end_date,
        )
        self.set_api_version(version=Version.V4)
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
