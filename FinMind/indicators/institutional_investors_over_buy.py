import numpy as np
import pandas as pd

from FinMind.schema.data import Dataset


def _taiwan_stock_institutional_investors_buy_sell_group_by(
    taiwan_stock_institutional_investors_buy_sell: pd.DataFrame,
) -> pd.DataFrame:
    taiwan_stock_institutional_investors_buy_sell[["sell", "buy"]] = (
        taiwan_stock_institutional_investors_buy_sell[["sell", "buy"]]
        .fillna(0)
        .astype(int)
    )
    taiwan_stock_institutional_investors_buy_sell = (
        taiwan_stock_institutional_investors_buy_sell.groupby(
            ["date", "stock_id"], as_index=False
        ).agg({"buy": np.sum, "sell": np.sum})
    )
    taiwan_stock_institutional_investors_buy_sell[
        "InstitutionalInvestorsOverBuy"
    ] = (
        taiwan_stock_institutional_investors_buy_sell["buy"]
        - taiwan_stock_institutional_investors_buy_sell["sell"]
    )
    return taiwan_stock_institutional_investors_buy_sell


def add_institutional_investors_over_buy_indicators(
    stock_price: pd.DataFrame, additional_dataset_obj, **kwargs
) -> pd.DataFrame:
    """
    url: "https://blog.above.tw/2018/08/15/%E7%B1%8C%E7%A2%BC%E9%9D%A2%E7%9A%84%E9%97%9C%E9%8D%B5%E6%8C%87%E6%A8%99%E6%9C%89%E5%93%AA%E4%BA%9B%EF%BC%9F/"
    summary:
        策略概念:法人買超股票會上漲, 反之亦然
        策略規則: 法人買超, 買
                法人賣超, 賣
    """
    stock_price = stock_price.sort_values("date")
    taiwan_stock_institutional_investors_buy_sell = getattr(
        additional_dataset_obj, Dataset.TaiwanStockInstitutionalInvestorsBuySell
    )
    taiwan_stock_institutional_investors_buy_sell = (
        _taiwan_stock_institutional_investors_buy_sell_group_by(
            taiwan_stock_institutional_investors_buy_sell
        )
    )
    stock_price = pd.merge(
        stock_price,
        taiwan_stock_institutional_investors_buy_sell[
            ["stock_id", "date", "InstitutionalInvestorsOverBuy"]
        ],
        on=["stock_id", "date"],
        how="left",
    ).fillna(0)
    return stock_price
