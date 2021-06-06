import numpy as np
import pandas as pd

from FinMind.data import DataLoader
from FinMind.schema.data import Dataset
from FinMind.strategies.base import Strategy, Trader


class ShortSaleMarginPurchaseRatio(Strategy):
    """
    url: "https://blog.above.tw/2018/08/15/%E7%B1%8C%E7%A2%BC%E9%9D%A2%E7%9A%84%E9%97%9C%E9%8D%B5%E6%8C%87%E6%A8%99%E6%9C%89%E5%93%AA%E4%BA%9B%EF%BC%9F/"
    summary:
        策略概念: 券資比越高代表散戶看空，法人買超股票會上漲，這時候賣可以跟大部分散戶進行相反的操作，反之亦然
        策略規則: 券資比>=30% 且法人買超股票, 賣
                券資比<30% 且法人賣超股票 買
    """

    ShortSaleMarginPurchaseTodayRatioThreshold = 0.3

    def __init__(
        self,
        trader: Trader,
        stock_id: str,
        start_date: str,
        end_date: str,
        data_loader: DataLoader,
    ):
        super().__init__(trader, stock_id, start_date, end_date, data_loader)
        self.TaiwanStockMarginPurchaseShortSale = None
        self.InstitutionalInvestorsBuySell = None

    def load_strategy_data(self):
        self.TaiwanStockMarginPurchaseShortSale = self.data_loader.get_data(
            dataset=Dataset.TaiwanStockMarginPurchaseShortSale,
            data_id=self.stock_id,
            start_date=self.start_date,
            end_date=self.end_date,
        )
        self.InstitutionalInvestorsBuySell = self.data_loader.get_data(
            dataset=Dataset.TaiwanStockInstitutionalInvestorsBuySell,
            data_id=self.stock_id,
            start_date=self.start_date,
            end_date=self.end_date,
        )

    def load_taiwan_stock_margin_purchase_short_sale(self):
        self.TaiwanStockMarginPurchaseShortSale[
            ["ShortSaleTodayBalance", "MarginPurchaseTodayBalance"]
        ] = self.TaiwanStockMarginPurchaseShortSale[
            ["ShortSaleTodayBalance", "MarginPurchaseTodayBalance"]
        ].astype(
            int
        )
        self.TaiwanStockMarginPurchaseShortSale[
            "ShortSaleMarginPurchaseTodayRatio"
        ] = (
            self.TaiwanStockMarginPurchaseShortSale["ShortSaleTodayBalance"]
            / self.TaiwanStockMarginPurchaseShortSale[
                "MarginPurchaseTodayBalance"
            ]
        )

    def load_institutional_investors_buy_sell(self):
        self.InstitutionalInvestorsBuySell[["sell", "buy"]] = (
            self.InstitutionalInvestorsBuySell[["sell", "buy"]]
            .fillna(0)
            .astype(int)
        )
        self.InstitutionalInvestorsBuySell = (
            self.InstitutionalInvestorsBuySell.groupby(
                ["date", "stock_id"], as_index=False
            ).agg({"buy": np.sum, "sell": np.sum})
        )
        self.InstitutionalInvestorsBuySell["diff"] = (
            self.InstitutionalInvestorsBuySell["buy"]
            - self.InstitutionalInvestorsBuySell["sell"]
        )

    def create_trade_sign(self, stock_price: pd.DataFrame) -> pd.DataFrame:
        stock_price = stock_price.sort_values("date")
        self.load_taiwan_stock_margin_purchase_short_sale()
        self.load_institutional_investors_buy_sell()
        stock_price = pd.merge(
            stock_price,
            self.InstitutionalInvestorsBuySell[["stock_id", "date", "diff"]],
            on=["stock_id", "date"],
            how="left",
        ).fillna(0)
        stock_price = pd.merge(
            stock_price,
            self.TaiwanStockMarginPurchaseShortSale[
                ["stock_id", "date", "ShortSaleMarginPurchaseTodayRatio"]
            ],
            on=["stock_id", "date"],
            how="left",
        ).fillna(0)
        stock_price.index = range(len(stock_price))
        stock_price["signal"] = 0
        sell_mask = (
            stock_price["ShortSaleMarginPurchaseTodayRatio"]
            >= self.ShortSaleMarginPurchaseTodayRatioThreshold
        ) & (stock_price["diff"] > 0)
        stock_price.loc[sell_mask, "signal"] = -1
        buy_mask = (
            stock_price["ShortSaleMarginPurchaseTodayRatio"]
            < self.ShortSaleMarginPurchaseTodayRatioThreshold
        ) & (stock_price["diff"] < 0)
        stock_price.loc[buy_mask, "signal"] = 1
        return stock_price
