import numpy as np
import pandas as pd

from FinMind.schema.data import Dataset


def _create_short_sale_margin_purchase_today_ratio(
    taiwan_stock_margin_purchase_shortSale: pd.DataFrame,
) -> pd.DataFrame:
    taiwan_stock_margin_purchase_shortSale[
        ["ShortSaleTodayBalance", "MarginPurchaseTodayBalance"]
    ] = taiwan_stock_margin_purchase_shortSale[
        ["ShortSaleTodayBalance", "MarginPurchaseTodayBalance"]
    ].astype(
        int
    )
    taiwan_stock_margin_purchase_shortSale["ShortSaleMarginPurchaseRatio"] = (
        taiwan_stock_margin_purchase_shortSale["ShortSaleTodayBalance"]
        / taiwan_stock_margin_purchase_shortSale["MarginPurchaseTodayBalance"]
    )
    return taiwan_stock_margin_purchase_shortSale


def add_short_sale_margin_purchase_ratio_indicators(
    stock_price: pd.DataFrame, additional_dataset_obj, **kwargs
) -> pd.DataFrame:
    """
    url: "https://blog.above.tw/2018/08/15/%E7%B1%8C%E7%A2%BC%E9%9D%A2%E7%9A%84%E9%97%9C%E9%8D%B5%E6%8C%87%E6%A8%99%E6%9C%89%E5%93%AA%E4%BA%9B%EF%BC%9F/"
    summary:
        策略概念: 券資比越高代表散戶看空，這時候賣可以跟大部分散戶進行相反的操作，反之亦然
        策略規則: 券資比>=30%, 賣
                券資比<30%, 買
    """
    stock_price = stock_price.sort_values("date")
    taiwan_stock_margin_purchase_shortSale = getattr(
        additional_dataset_obj, Dataset.TaiwanStockMarginPurchaseShortSale
    )
    taiwan_stock_margin_purchase_shortSale = (
        _create_short_sale_margin_purchase_today_ratio(
            taiwan_stock_margin_purchase_shortSale
        )
    )
    stock_price = pd.merge(
        stock_price,
        taiwan_stock_margin_purchase_shortSale[
            ["stock_id", "date", "ShortSaleMarginPurchaseRatio"]
        ],
        on=["stock_id", "date"],
        how="left",
    ).fillna(0)
    return stock_price
