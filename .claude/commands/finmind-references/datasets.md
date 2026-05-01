# FinMind Dataset Reference

Complete dataset list with column details, tier requirements, and parameter specifications.

## Table of Contents

- [Taiwan Market - Technical (20 datasets)](#taiwan-market---technical)
- [Taiwan Market - Chip / Institutional (16 datasets)](#taiwan-market---chip--institutional)
- [Taiwan Market - Fundamental (12 datasets)](#taiwan-market---fundamental)
- [Taiwan Market - Derivative (16 datasets)](#taiwan-market---derivative)
- [Taiwan Market - Real-Time (4 datasets, Sponsor)](#taiwan-market---real-time)
- [Taiwan Market - Convertible Bond (4 datasets)](#taiwan-market---convertible-bond)
- [Taiwan Market - Others (3 datasets)](#taiwan-market---others)
- [International Markets (8 datasets)](#international-markets)
- [Global Economic Data (6 datasets)](#global-economic-data)

## Tier Legend

- **Free**: No data_id required
- **Free(w/ data_id)**: Free when querying a specific stock; Backer/Sponsor to query all stocks (omit data_id)
- **Backer**: Requires Backer tier or above
- **Sponsor**: Requires Sponsor tier or above

## Parameter Notes

- `start_date` / `end_date`: Format `YYYY-MM-DD`
- Datasets marked "single day" only accept `start_date` (no end_date range)
- To query all stocks for a date: omit `data_id`, provide only `start_date` (requires Backer/Sponsor)

---

## Taiwan Market - Technical

| Dataset | Description | Tier | Params | Key Columns |
|---------|------------|------|--------|-------------|
| TaiwanStockInfo | 台股總覽 | Free | dataset only | industry_category, stock_id, stock_name, type, date |
| TaiwanStockInfoWithWarrant | 台股總覽含權證 | Free | dataset only | industry_category, stock_id, stock_name, type, date |
| TaiwanStockInfoWithWarrantSummary | 台股權證標的對照表 | Sponsor | data_id, start_date | stock_id, date, close, target_stock_id, target_close, type, exercise_ratio, fulfillment_price |
| TaiwanStockTradingDate | 台股交易日 | Free | dataset only | date |
| TaiwanStockPrice | 股價日成交資訊 | Free(w/ data_id) | data_id, start_date, end_date | date, stock_id, Trading_Volume, Trading_money, open, max, min, close, spread, Trading_turnover |
| TaiwanStockPriceAdj | 還原股價 | Free(w/ data_id) | data_id, start_date, end_date | date, stock_id, Trading_Volume, Trading_money, open, max, min, close, spread, Trading_turnover |
| TaiwanStockPriceTick | 歷史逐筆交易 | Backer | data_id, start_date (single day) | date, stock_id, deal_price, volume, Time, TickType |
| TaiwanStockPER | PER/PBR | Free | data_id, start_date, end_date | date, stock_id, dividend_yield, PER, PBR |
| TaiwanStockStatisticsOfOrderBookAndTrade | 每5秒委託成交統計 | Free | start_date (single day) | Time, TotalBuyOrder, TotalBuyVolume, TotalSellOrder, TotalSellVolume, TotalDealVolume, TotalDealMoney, date |
| TaiwanVariousIndicators5Seconds | 台股加權指數 | Free | start_date (single day) | date, TAIEX |
| TaiwanStockDayTrading | 當沖交易 (2014-01-01~now) | Free(w/ data_id) | data_id, start_date, end_date | stock_id, date, BuyAfterSale, Volume, BuyAmount, SellAmount |
| TaiwanStockTotalReturnIndex | 報酬指數 | Free | data_id(TAIEX/TPEx), start_date, end_date | price, stock_id, date |
| TaiwanStock10Year | 十年線 | Backer | data_id, start_date, end_date | date, stock_id, close |
| TaiwanStockKBar | 分K資料 | Sponsor | data_id, start_date (single day) | date, minute, stock_id, open, high, low, close, volume |
| TaiwanStockWeekPrice | 週K | Backer | data_id, start_date, end_date | stock_id, yweek, max, min, trading_volume, trading_money, date, close, open, spread |
| TaiwanStockMonthPrice | 月K | Backer | data_id, start_date, end_date | stock_id, ymonth, max, min, trading_volume, trading_money, date, close, open, spread |
| TaiwanStockEvery5SecondsIndex | 每5秒指數統計 | Backer | start_date (single day) | date, time, stock_id, price, kind |
| TaiwanStockSuspended | 暫停交易公告 | Backer | start_date, end_date | stock_id, date, suspension_time, resumption_date |
| TaiwanStockDayTradingSuspension | 暫停先賣後買當沖 | Backer | start_date, end_date | stock_id, date, end_date, reason |
| TaiwanStockPriceLimit | 每日漲跌停價 (2000-01-01~now) | Free(w/ data_id) | data_id, start_date | date, stock_id, reference_price, limit_up, limit_down |

## Taiwan Market - Chip / Institutional

| Dataset | Description | Tier | Key Columns |
|---------|------------|------|-------------|
| TaiwanStockMarginPurchaseShortSale | 融資融劵 | Free(w/ data_id) | date, stock_id, MarginPurchaseBuy/Sell/TodayBalance, ShortSaleBuy/Sell/TodayBalance |
| TaiwanStockTotalMarginPurchaseShortSale | 整體市場融資融劵 | Free | TodayBalance, YesBalance, buy, date, name, Return, sell |
| TaiwanStockInstitutionalInvestorsBuySell | 三大法人買賣 | Free(w/ data_id) | date, stock_id, buy, name, sell |
| TaiwanStockTotalInstitutionalInvestors | 整體三大法人 | Free | buy, date, name, sell |
| TaiwanStockShareholding | 外資持股 | Free(w/ data_id) | date, stock_id, ForeignInvestmentShares, ForeignInvestmentSharesRatio |
| TaiwanStockHoldingSharesPer | 股權持股分級 | Backer | date, stock_id, HoldingSharesLevel, people, percent, unit |
| TaiwanStockSecuritiesLending | 借券成交 | Free(w/ data_id) | date, stock_id, transaction_type, volume, fee_rate, close |
| TaiwanStockMarginShortSaleSuspension | 暫停融券賣出 | Free(w/ data_id) | stock_id, date, end_date, reason |
| TaiwanDailyShortSaleBalances | 信用額度總量管制餘額 | Free(w/ data_id) | stock_id, MarginShortSales*, SBLShortSales*, date |
| TaiwanSecuritiesTraderInfo | 證券商資訊 | Free | securities_trader_id, securities_trader, date, address, phone |
| TaiwanStockTradingDailyReport | 分點資料 (special endpoint) | Sponsor | securities_trader, price, buy, sell, securities_trader_id, stock_id, date |
| TaiwanStockWarrantTradingDailyReport | 權證分點資料 (special endpoint) | Sponsor | securities_trader, price, buy, sell, securities_trader_id, stock_id, date |
| TaiwanstockGovernmentBankBuySell | 八大行庫買賣 | Sponsor | date, stock_id, buy_amount, sell_amount, buy, sell, bank_name |
| TaiwanTotalExchangeMarginMaintenance | 大盤融資維持率 | Backer | date, TotalExchangeMarginMaintenance |
| TaiwanStockTradingDailyReportSecIdAgg | 卷商分點統計 (2021-06-30~now, special endpoint) | Sponsor | securities_trader, securities_trader_id, stock_id, date, buy_volume, sell_volume, buy_price, sell_price |
| TaiwanStockDispositionSecuritiesPeriod | 處置有價證券 | Backer | date, stock_id, stock_name, disposition_cnt, condition, measure, period_start, period_end |
| TaiwanStockBlockTrade | 鉅額交易日成交資訊（逐筆，2005-04-04~now） | Sponsor | date, stock_id, trade_type, price, volume, trading_money |
| TaiwanStockLoanCollateralBalance | 借貸款項擔保品餘額表（37 欄位，2006-10-02~now） | Sponsor | date, stock_id, market, Margin*, SecuritiesFirmLoan*, UnrestrictedLoan*, SecuritiesFinanceSecuredLoan*, SettlementMargin* (PreviousDayBalance/Buy/Sell/CashRedemption/Replacement/CurrentDayBalance/NextDayQuota) |

## Taiwan Market - Fundamental

| Dataset | Description | Tier | Key Columns |
|---------|------------|------|-------------|
| TaiwanStockFinancialStatements | 綜合損益表 | Free(w/ data_id) | date, stock_id, type, value, origin_name |
| TaiwanStockBalanceSheet | 資產負債表 | Free(w/ data_id) | date, stock_id, type, value, origin_name |
| TaiwanStockCashFlowsStatement | 現金流量表 | Free(w/ data_id) | date, stock_id, type, value, origin_name |
| TaiwanStockDividend | 股利政策 | Free(w/ data_id) | date, stock_id, CashEarningsDistribution, StockEarningsDistribution, CashExDividendTradingDate |
| TaiwanStockDividendResult | 除權除息結果 | Free(w/ data_id) | date, stock_id, before_price, after_price, stock_and_cache_dividend |
| TaiwanStockMonthRevenue | 月營收 | Free(w/ data_id) | date, stock_id, revenue, revenue_month, revenue_year |
| TaiwanStockCapitalReductionReferencePrice | 減資恢復買賣參考價 | Free | date, stock_id, PostReductionReferencePrice, ReasonforCapitalReduction |
| TaiwanStockMarketValue | 股價市值 | Backer | date, stock_id, market_value |
| TaiwanStockDelisting | 下市櫃 | Free | date, stock_id, stock_name |
| TaiwanStockMarketValueWeight | 市值比重 | Backer | rank, stock_id, stock_name, weight_per, date, type |
| TaiwanStockSplitPrice | 分割後參考價 | Free | date, stock_id, type, before_price, after_price |
| TaiwanStockParValueChange | 變更面額恢復買賣參考價 | Free | date, stock_id, stock_name, before_close, after_ref_close |

## Taiwan Market - Derivative

| Dataset | Description | Tier | Key Columns |
|---------|------------|------|-------------|
| TaiwanFutOptDailyInfo | 期貨選擇權總覽 | Free | code, type, name |
| TaiwanFuturesDaily | 期貨日成交 | Free(w/ data_id) | date, futures_id, contract_date, open, max, min, close, volume, settlement_price, open_interest |
| TaiwanOptionDaily | 選擇權日成交 | Free(w/ data_id) | date, option_id, contract_date, strike_price, call_put, open, max, min, close, volume |
| TaiwanFuturesTick | 期貨交易明細 | Backer | contract_date, date, futures_id, price, volume |
| TaiwanOptionTIck | 選擇權交易明細 | Backer | ExercisePrice, PutCall, contract_date, date, option_id, price, volume |
| TaiwanFuturesInstitutionalInvestors | 期貨三大法人 | Free(w/ data_id) | name, date, institutional_investors, long/short_deal_volume/amount |
| TaiwanOptionInstitutionalInvestors | 選擇權三大法人 | Free(w/ data_id) | name, date, call_put, institutional_investors, long/short_deal_volume/amount |
| TaiwanFuturesInstitutionalInvestorsAfterHours | 期貨夜盤三大法人 | Backer | futures_id, date, institutional_investors, long/short_deal_volume/amount |
| TaiwanOptionInstitutionalInvestorsAfterHours | 選擇權夜盤三大法人 | Backer | option_id, date, call_put, institutional_investors, long/short_deal_volume/amount |
| TaiwanFuturesDealerTradingVolumeDaily | 期貨各卷商每日交易 | Free | date, dealer_code, dealer_name, futures_id, volume |
| TaiwanOptionDealerTradingVolumeDaily | 選擇權各卷商每日交易 | Free | date, dealer_code, dealer_name, option_id, volume |
| TaiwanFuturesOpenInterestLargeTraders | 期貨大額交易人未沖銷 | Backer | name, futures_id, buy/sell_top5/10_trader_open_interest, date |
| TaiwanOptionOpenInterestLargeTraders | 選擇權大額交易人未沖銷 | Backer | name, option_id, put_call, buy/sell_top5/10_trader_open_interest, date |
| TaiwanFuturesSpreadTrading | 期貨價差行情 | Backer | date, futures_id, contract_date, open, max, min, close |
| TaiwanFuturesFinalSettlementPrice | 期貨最後結算價 | Backer | date, contract_month, futures_id, settlement_price |
| TaiwanOptionFinalSettlementPrice | 選擇權最後結算價 | Backer | date, contract_month, option_id, settlement_price |

## Taiwan Market - Real-Time

All real-time datasets require **Sponsor** tier.

| Dataset | Description | Key Columns |
|---------|------------|-------------|
| taiwan_stock_tick_snapshot | 台股即時資訊 | close, high, low, open, volume, total_volume, change_price, change_rate, date, stock_id |
| TaiwanFutOptTickInfo | 期貨選擇權即時總覽 | code, callput, date, name |
| taiwan_futures_snapshot | 期貨即時資訊 | open, high, low, close, volume, total_volume, change_price, change_rate, date, futures_id |
| taiwan_options_snapshot | 選擇權即時資訊 | open, high, low, close, volume, total_volume, change_price, change_rate, date, options_id |

## Taiwan Market - Convertible Bond

All convertible bond datasets require **Backer** or **Sponsor** tier.

| Dataset | Description | Key Columns |
|---------|------------|-------------|
| TaiwanStockConvertibleBondInfo | 可轉債總覽 | cb_id, cb_name, InitialDateOfConversion, DueDateOfConversion |
| TaiwanStockConvertibleBondDaily | 可轉債日成交 | cb_id, cb_name, close, open, max, min, volume, date |
| TaiwanStockConvertibleBondInstitutionalInvestors | 可轉債三大法人 | Foreign/Investment_Trust/Dealer Buy/Sell, cb_id, date |
| TaiwanStockConvertibleBondDailyOverview | 可轉債每日總覽 | cb_id, ConversionPrice, IssuanceAmount, OutstandingAmount, date |

## Taiwan Market - Others

| Dataset | Description | Tier | Key Columns |
|---------|------------|------|-------------|
| TaiwanStockNews | 相關新聞 | Free | date, stock_id, description, link, source, title |
| TaiwanBusinessIndicator | 景氣對策信號 | Backer | date, leading, coincident, lagging, monitoring, monitoring_color |
| TaiwanStockIndustryChain | 產業鏈 | Backer | stock_id, industry, sub_industry, date |

## International Markets

| Dataset | Description | Tier | Key Columns |
|---------|------------|------|-------------|
| USStockInfo | 美股總覽 | Free | date, stock_id, Country, MarketCap, stock_name |
| USStockPrice | 美股股價 daily | Free | date, stock_id, Open, High, Low, Close, Adj_Close, Volume |
| USStockPriceMinute | 美股股價 minute | Backer | date, stock_id, open, high, low, close, volume |
| UKStockInfo | 英股總覽 | Free | date, stock_id, Country, stock_name |
| UKStockPrice | 英股股價 | Free | date, stock_id, Open, High, Low, Close, Adj_Close, Volume |
| EuropeStockInfo | 歐股總覽 | Free | date, stock_id, Market, stock_name |
| EuropeStockPrice | 歐股股價 | Free | date, stock_id, Open, High, Low, Close, Adj_Close, Volume |
| JapanStockInfo | 日股總覽 | Free | date, stock_id, Exchange, Sector, stock_name |
| JapanStockPrice | 日股股價 | Free | date, stock_id, Open, High, Low, Close, Adj_Close, Volume |

## Global Economic Data

| Dataset | Description | Tier | data_id values | Key Columns |
|---------|------------|------|---------------|-------------|
| TaiwanExchangeRate | 外幣匯率 | Free | USD, EUR, JPY, GBP, CNY, HKD, AUD, CAD, CHF, IDR, KRW, MYR, NZD, PHP, SEK, SGD, THB, VND, ZAR | date, currency, cash_buy, cash_sell, spot_buy, spot_sell |
| InterestRate | 央行利率 | Free | FED, BOE, RBA, PBOC, BOC, ECB, RBNZ, RBI, CBR, BCB, BOJ, SNB | country, date, interest_rate |
| GoldPrice | 黃金價格 | Free | — | Price, date |
| CrudeOilPrices | 原油價格 | Free | WTI, Brent | date, name, price |
| GovernmentBondsYield | 美國國債殖利率 | Free | "United States 1-Month" ~ "United States 30-Year" | date, name, value |
| CnnFearGreedIndex | CNN 恐懼貪婪指數 | Backer | — | date, fear_greed, fear_greed_emotion |
