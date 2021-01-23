import typing
from pydantic import BaseModel


class final_stats(BaseModel):
    MeanProfit: float
    MaxLoss: float
    FinalProfit: float
    MeanProfitPer: float
    FinalProfitPer: float
    MaxLossPer: float
    AnnualReturnPer: float
    AnnualSharpRatio: float


class trade_detail(BaseModel):
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

class compare_market_detail(BaseModel):
    date: str
    CumDailyRetrun: float
    CumTaiexDailyRetrun: float

class compare_market_stats(BaseModel):
    AnnualTaiexReturnPer: float
    AnnualReturnPer: float
