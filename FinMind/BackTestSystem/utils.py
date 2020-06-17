from FinMind.Data.Load import FinData


def get_asset_underlying_type(stock_id: str) -> str:
    TaiwanStockInfo = FinData("TaiwanStockInfo", date="")
    underlying_type = TaiwanStockInfo[TaiwanStockInfo["stock_id"] == stock_id][
        "industry_category"
    ].values[0]
    return underlying_type


def get_underlying_trading_tax(underlying_type: str) -> float:
    mapping = {"ETF": 0.001, "上櫃指數股票型基金(ETF)": 0.001}
    return mapping.get(underlying_type, 0.003)
