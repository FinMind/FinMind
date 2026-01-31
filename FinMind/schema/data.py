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
    TaiwanStockTotalReturnIndex = "TaiwanStockTotalReturnIndex"
    USStockPrice = "USStockPrice"
    TaiwanStockDividendResult = "TaiwanStockDividendResult"
    TaiwanStockInfo = "TaiwanStockInfo"
    TaiwanStockInfoWithWarrant = "TaiwanStockInfoWithWarrant"
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
    TaiwanFuturesInstitutionalInvestors = "TaiwanFuturesInstitutionalInvestors"
    TaiwanOptionInstitutionalInvestors = "TaiwanOptionInstitutionalInvestors"
    TaiwanFuturesInstitutionalInvestorsAfterHours = (
        "TaiwanFuturesInstitutionalInvestorsAfterHours"
    )
    TaiwanOptionInstitutionalInvestorsAfterHours = (
        "TaiwanOptionInstitutionalInvestorsAfterHours"
    )
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
    TaiwanStockCapitalReductionReferencePrice = (
        "TaiwanStockCapitalReductionReferencePrice"
    )
    TaiwanStockGovernmentBankBuySell = "TaiwanStockGovernmentBankBuySell"
    TaiwanSecuritiesTraderInfo = "TaiwanSecuritiesTraderInfo"
    TaiwanStockMarketValue = "TaiwanStockMarketValue"
    TaiwanStock10Year = "TaiwanStock10Year"
    TaiwanStockTickSnapshot = "taiwan_stock_tick_snapshot"
    TaiwanFuturesSnapshot = "taiwan_futures_snapshot"
    TaiwanOptionsSnapshot = "taiwan_options_snapshot"
    TaiwanStockPriceAdj = "TaiwanStockPriceAdj"
    TaiwanStockKBar = "TaiwanStockKBar"
    TaiwanStockDelisting = "TaiwanStockDelisting"
    TaiwanStockConvertibleBondInfo = "TaiwanStockConvertibleBondInfo"
    TaiwanStockConvertibleBondDaily = "TaiwanStockConvertibleBondDaily"
    TaiwanStockConvertibleBondInstitutionalInvestors = (
        "TaiwanStockConvertibleBondInstitutionalInvestors"
    )
    TaiwanStockConvertibleBondDailyOverview = (
        "TaiwanStockConvertibleBondDailyOverview"
    )
    TaiwanStockMarginShortSaleSuspension = (
        "TaiwanStockMarginShortSaleSuspension"
    )
    TaiwanTotalExchangeMarginMaintenance = (
        "TaiwanTotalExchangeMarginMaintenance"
    )
    TaiwanStockWeekPrice = "TaiwanStockWeekPrice"
    TaiwanStockMonthPrice = "TaiwanStockMonthPrice"
    TaiwanStockTradingDailyReportSecIdAgg = (
        "TaiwanStockTradingDailyReportSecIdAgg"
    )
    TaiwanStockTradingDailyReport = "TaiwanStockTradingDailyReport"
    TaiwanStockWarrantTradingDailyReport = (
        "TaiwanStockWarrantTradingDailyReport"
    )
    TaiwanOptionOpenInterestLargeTraders = (
        "TaiwanOptionOpenInterestLargeTraders"
    )
    TaiwanFuturesOpenInterestLargeTraders = (
        "TaiwanFuturesOpenInterestLargeTraders"
    )
    TaiwanStockMarketValueWeight = "TaiwanStockMarketValueWeight"
    TaiwanBusinessIndicator = "TaiwanBusinessIndicator"
    TaiwanStockDispositionSecuritiesPeriod = (
        "TaiwanStockDispositionSecuritiesPeriod"
    )
    TaiwanStockIndustryChain = "TaiwanStockIndustryChain"
    TaiwanStockTradingDate = "TaiwanStockTradingDate"
    TaiwanStockInfoWithWarrantSummary = "TaiwanStockInfoWithWarrantSummary"
    TaiwanStockSplitPrice = "TaiwanStockSplitPrice"
    TaiwanStockParValueChange = "TaiwanStockParValueChange"
    TaiwanStockSuspended = "TaiwanStockSuspended"
    TaiwanStockDayTradingSuspension = "TaiwanStockDayTradingSuspension"


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
