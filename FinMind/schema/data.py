from enum import Enum


class Dataset(str, Enum):
    TaiwanStockBalanceSheet = "TaiwanStockBalanceSheet"
    TaiwanStockFinancialStatements = "TaiwanStockFinancialStatements"
    TaiwanStockInstitutionalInvestorsBuySell = (
        "TaiwanStockInstitutionalInvestorsBuySell"
    )
    TaiwanStockTotalInstitutionalInvestors = (
        "TaiwanStockTotalInstitutionalInvestors"
    )
    TaiwanStockShareholding = "TaiwanStockShareholding"
    TaiwanStockPER = "TaiwanStockPER"
    TaiwanStockPrice = "TaiwanStockPrice"
    TaiwanStockCashFlowsStatement = "TaiwanStockCashFlowsStatement"
    TaiwanStockMonthRevenue = "TaiwanStockMonthRevenue"
    TaiwanStockMarginPurchaseShortSale = "TaiwanStockMarginPurchaseShortSale"
    TaiwanDailyShortSaleBalances = "TaiwanDailyShortSaleBalances"
    CrudeOilPrices = "CrudeOilPrices"
    CnnFearGreedIndex = "CnnFearGreedIndex"
    TaiwanExchangeRate = "TaiwanExchangeRate"
    ExchangeRate = "ExchangeRate"
    TaiwanStockPriceTick = "TaiwanStockPriceTick"
    TaiwanFuturesTick = "TaiwanFuturesTick"
    TaiwanOptionTick = "TaiwanOptionTick"
    TaiwanStockPriceBidAsk = "TaiwanStockPriceBidAsk"
    TaiwanFuturesDaily = "TaiwanFuturesDaily"
    TaiwanOptionDaily = "TaiwanOptionDaily"
    TaiwanStockNews = "TaiwanStockNews"
    USStockPrice = "USStockPrice"
    TaiwanStockDividendResult = "TaiwanStockDividendResult"
    TaiwanStockInfo = "TaiwanStockInfo"
    TaiwanStockSecuritiesLending = "TaiwanStockSecuritiesLending"
    TaiwanFutOptTickInfo = "TaiwanFutOptTickInfo"
    TaiwanFutOptDailyInfo = "TaiwanFutOptDailyInfo"
    TaiwanStockHoldingSharesPer = "TaiwanStockHoldingSharesPer"
    TaiwanStockDividend = "TaiwanStockDividend"
    TaiwanStockTotalMarginPurchaseShortSale = (
        "TaiwanStockTotalMarginPurchaseShortSale"
    )
    EuropeStockInfo = "EuropeStockInfo"
    JapanStockInfo = "JapanStockInfo"
    GoldPrice = "GoldPrice"
    InterestRate = "InterestRate"
    USStockInfo = "USStockInfo"
    UKStockInfo = "UKStockInfo"
    TaiwanStockStatisticsOfOrderBookAndTrade = (
        "TaiwanStockStatisticsOfOrderBookAndTrade"
    )
    TaiwanFutOptTick = "TaiwanFutOptTick"
    TaiwanVariousIndicators5Seconds = "TaiwanVariousIndicators5Seconds"
    TaiwanFutOptInstitutionalInvestors = "TaiwanFutOptInstitutionalInvestors"
    TaiwanFuturesDealerTradingVolumeDaily = (
        "TaiwanFuturesDealerTradingVolumeDaily"
    )
    TaiwanOptionDealerTradingVolumeDaily = (
        "TaiwanOptionDealerTradingVolumeDaily"
    )
    GovernmentBondsYield = "GovernmentBondsYield"
    USStockPriceMinute = "USStockPriceMinute"
    TaiwanStockDayTrading = "TaiwanStockDayTrading"
    TaiwanStockEvery5SecondsIndex = "TaiwanStockEvery5SecondsIndex"


class Version(str, Enum):
    V4 = "v4"
    V3 = "v3"


class DataList(str, Enum):
    CrudeOilPrices = "CrudeOilPrices"
    CurrencyCirculation = "CurrencyCirculation"
    ExchangeRate = "ExchangeRate"
    GovernmentBondsYield = "GovernmentBondsYield"
    GovernmentBonds = "GovernmentBonds"
    InterestRate = "InterestRate"
    TaiwanExchangeRate = "TaiwanExchangeRate"


class Translation(str, Enum):
    TaiwanStockBalanceSheet = "TaiwanStockBalanceSheet"
    TaiwanStockFinancialStatements = "TaiwanStockFinancialStatements"
    TaiwanStockInstitutionalInvestorsBuySell = (
        "TaiwanStockInstitutionalInvestorsBuySell"
    )
    RawMaterialFuturesPrices = "RawMaterialFuturesPrices"
    TaiwanStockShareholding = "TaiwanStockShareholding"
    TaiwanStockDividend = "TaiwanStockDividend"
    TaiwanStockCashFlowsStatement = "TaiwanStockCashFlowsStatement"
    TaiwanFutures = "TaiwanFutures"
    TaiwanOption = "TaiwanOption"
    TaiwanStockTotalMarginPurchaseShortSale = (
        "TaiwanStockTotalMarginPurchaseShortSale"
    )
    TaiwanStockMarginPurchaseShortSale = "TaiwanStockMarginPurchaseShortSale"
    USStockPrice = "USStockPrice"
