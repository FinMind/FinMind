import numpy as np
import pandas as pd
from ta.momentum import StochasticOscillator

from FinMind.BackTestSystem.BaseClass import Strategy
from FinMind.Data import Load


class ShortSaleMarginPurchaseRatio(Strategy):
    """
    url: "https://blog.above.tw/2018/08/15/%E7%B1%8C%E7%A2%BC%E9%9D%A2%E7%9A%84%E9%97%9C%E9%8D%B5%E6%8C%87%E6%A8%99%E6%9C%89%E5%93%AA%E4%BA%9B%EF%BC%9F/"
    summary:
        策略概念: 券資比越高代表散戶看空，法人買超股票會上漲，這時候賣可以跟大部分散戶進行相反的操作，反之亦然
        策略規則: 券資比>=30% 且法人買超股票, 賣
                券資比<30% 且法人賣超股票 買
    """

    ShortSaleMarginPurchaseTodayRatioThreshold = 0.3

    def init(self, base_data):
        base_data = base_data.sort_values("date")

        stock_id = base_data["stock_id"].unique()
        start_date = base_data["date"].min()
        end_date = base_data["date"].max()

        TaiwanStockMarginPurchaseShortSale = Load.FinData(
            dataset="TaiwanStockMarginPurchaseShortSale",
            select=stock_id,
            date=start_date,
            end_date=end_date,
        )

        TaiwanStockMarginPurchaseShortSale[
            ["ShortSaleTodayBalance", "MarginPurchaseTodayBalance"]
        ] = TaiwanStockMarginPurchaseShortSale[
            ["ShortSaleTodayBalance", "MarginPurchaseTodayBalance"]
        ].astype(
            int
        )
        TaiwanStockMarginPurchaseShortSale[
            "ShortSaleMarginPurchaseTodayRatio"
        ] = (
            TaiwanStockMarginPurchaseShortSale["ShortSaleTodayBalance"]
            / TaiwanStockMarginPurchaseShortSale["MarginPurchaseTodayBalance"]
        )

        InstitutionalInvestorsBuySell = Load.FinData(
            dataset="InstitutionalInvestorsBuySell",
            select=stock_id,
            date=start_date,
            end_date=end_date,
        )

        InstitutionalInvestorsBuySell[["sell", "buy"]] = (
            InstitutionalInvestorsBuySell[["sell", "buy"]].fillna(0).astype(int)
        )
        InstitutionalInvestorsBuySell = InstitutionalInvestorsBuySell.groupby(
            ["date", "stock_id"], as_index=False
        ).agg({"buy": np.sum, "sell": np.sum})
        InstitutionalInvestorsBuySell["diff"] = (
            InstitutionalInvestorsBuySell["buy"]
            - InstitutionalInvestorsBuySell["sell"]
        )
        base_data = pd.merge(
            base_data,
            InstitutionalInvestorsBuySell[["stock_id", "date", "diff"]],
            on=["stock_id", "date"],
            how="left",
        ).fillna(0)
        base_data = pd.merge(
            base_data,
            TaiwanStockMarginPurchaseShortSale[
                ["stock_id", "date", "ShortSaleMarginPurchaseTodayRatio"]
            ],
            on=["stock_id", "date"],
            how="left",
        ).fillna(0)

        base_data.index = range(len(base_data))

        base_data["signal"] = 0
        sell_mask = (
            base_data["ShortSaleMarginPurchaseTodayRatio"]
            >= self.ShortSaleMarginPurchaseTodayRatioThreshold
        ) & (base_data["diff"] > 0)
        base_data.loc[sell_mask, "signal"] = -1
        buy_mask = (
            base_data["ShortSaleMarginPurchaseTodayRatio"]
            < self.ShortSaleMarginPurchaseTodayRatioThreshold
        ) & (base_data["diff"] < 0)
        base_data.loc[buy_mask, "signal"] = 1
        return base_data
