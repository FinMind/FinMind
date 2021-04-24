from pydantic import BaseModel


class FinalStats(BaseModel):
    MeanProfit: float
    MaxLoss: float
    FinalProfit: float
    MeanProfitPer: float
    FinalProfitPer: float
    MaxLossPer: float
    AnnualReturnPer: float
    AnnualSharpRatio: float


class TradeDetail(BaseModel):
    stock_id: str
    date: str
    EverytimeProfit: float
    RealizedProfit: float
    UnrealizedProfit: float
    board_lot: int
    hold_cost: float
    hold_volume: int
    signal: int
    trade_price: float
    trader_fund: float
    EverytimeTotalProfit: float
    CashEarningsDistribution: float
    StockEarningsDistribution: float


class CompareMarketDetail(BaseModel):
    date: str
    CumDailyReturn: float
    CumTaiExDailyReturn: float


class CompareMarketStats(BaseModel):
    AnnualTaiexReturnPer: float
    AnnualReturnPer: float
