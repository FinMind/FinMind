

library(httr) 
library(jsonlite)
library('data.table')
library(dplyr)

url = 'http://192.168.25.140/api/data'
list_url = 'http://192.168.25.140/api/datalist'
#url = 'http://finmindapi.servebeer.com/api/data'

# TaiwanStockInfo
payload<-list( 'dataset' = 'TaiwanStockInfo', 
               'stock_id' = '', 
               'date'='' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# TaiwanStockPrice
payload<-list( 'dataset' = 'TaiwanStockPrice', 
               'stock_id' = list('2330','2317'), 
               'date'='2019-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# FinancialStatements
payload<-list( 'dataset' = 'FinancialStatements', 
               'stock_id' = list('2330','2317'), 
               'date'='2018-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# TaiwanStockStockDividend
payload<-list( 'dataset' = 'TaiwanStockStockDividend', 
               'stock_id' = list('2330','2317'), 
               'date'='2019-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# TaiwanStockMarginPurchaseShortSale
payload<-list( 'dataset' = 'TaiwanStockMarginPurchaseShortSale', 
               'stock_id' = list('2330','2317'), 
               'date'='2019-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# InstitutionalInvestorsBuySell
payload<-list( 'dataset' = 'InstitutionalInvestorsBuySell', 
               'stock_id' = list('2330','2317'), 
               'date'='2019-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# Shareholding
payload<-list( 'dataset' = 'Shareholding', 
               'stock_id' = list('2330','2317'), 
               'date'='2019-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# BalanceSheet
payload<-list( 'dataset' = 'BalanceSheet', 
               'stock_id' = list('2330','2317'), 
               'date'='2018-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# TaiwanStockHoldingSharesPer
payload<-list( 'dataset' = 'TaiwanStockHoldingSharesPer', 
               'stock_id' = list('2330','2317'), 
               'date'='2019-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# TaiwanStockMonthRevenue
payload<-list( 'dataset' = 'TaiwanStockMonthRevenue', 
               'stock_id' = list('2330','2317'), 
               'date'='2019-01-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# USStockInfo
payload<-list( 'dataset' = 'USStockInfo', 
               'stock_id' = '', 
               'date'='' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# USStockPrice
payload<-list( 'dataset' = 'USStockPrice', 
               'stock_id' = list('^GSPC','^DJI'), 
               'date'='2019-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# FinancialStatements
payload<-list( 'dataset' = 'FinancialStatements', 
               'stock_id' = list('AAPL'), 
               'date'='2018-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# JapanStockInfo
payload<-list( 'dataset' = 'JapanStockInfo', 
               'stock_id' = '', 
               'date'='2019-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# JapanStockPrice
payload<-list( 'dataset' = 'JapanStockPrice', 
               'stock_id' = list('1352.T','1376.T'), 
               'date'='2019-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# UKStockInfo
payload<-list( 'dataset' = 'UKStockInfo', 
               'stock_id' = '', 
               'date'='2019-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# UKStockPrice
payload<-list( 'dataset' = 'UKStockPrice', 
               'stock_id' = list('0TWH.L','0HZU.L'), 
               'date'='2019-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# EuropeStockInfo
payload<-list( 'dataset' = 'EuropeStockInfo', 
               'stock_id' = '', 
               'date'='2019-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# EuropeStockPrice
payload<-list( 'dataset' = 'EuropeStockPrice', 
               'stock_id' = list('AB.PA','ABCA.PA'), 
               'date'='2019-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# EuropeStockInfo
payload<-list( 'dataset' = 'EuropeStockInfo', 
               'stock_id' = list(), 
               'date'='2019-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# ExchangeRate
payload<-list( 'dataset' = 'ExchangeRate', 
               'stock_id' = list(), 
               'date'='2019-06-01' )

response = POST(list_url,body =payload,encode="json")
data = response %>% content 
data = do.call('c',data$data)

# EuropeStockInfo
payload<-list( 'dataset' = 'ExchangeRate', 
               'stock_id' = list('Canda', 'China', 'Euro', 'Japan', 'Taiwan', 'UK'), 
               'date'='2019-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# InstitutionalInvestors
payload<-list( 'dataset' = 'InstitutionalInvestors', 
               'stock_id' = '', 
               'date'='2019-06-01' )

response = POST(list_url,body =payload,encode="json")
data = response %>% content 
data = do.call('c',data$data)

# InstitutionalInvestors
payload<-list( 'dataset' = 'InstitutionalInvestors', 
               'stock_id' = list('Dealer'), 
               'date'='2019-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# InterestRate
payload<-list( 'dataset' = 'InterestRate', 
               'stock_id' = '', 
               'date'='2019-06-01' )

response = POST(list_url,body =payload,encode="json")
data = response %>% content 
data = do.call('c',data$data)

# InterestRate
payload<-list( 'dataset' = 'InterestRate', 
               'stock_id' = list('BCB','BOC'), 
               'date'='2019-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# GovernmentBonds
payload<-list( 'dataset' = 'GovernmentBonds', 
               'stock_id' = '', 
               'date'='2019-06-01' )

response = POST(list_url,body =payload,encode="json")
data = response %>% content 
data = do.call('c',data$data) 

# GovernmentBonds
payload<-list( 'dataset' = 'GovernmentBonds', 
               'stock_id' = list('France 9-Month','France 9-Year'), 
               'date'='2019-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# CrudeOilPrices
payload<-list( 'dataset' = 'CrudeOilPrices', 
               'stock_id' = '', 
               'date'='2019-06-01' )

response = POST(list_url,body =payload,encode="json")
data = response %>% content 
data = do.call('c',data$data)

# CrudeOilPrices
payload<-list( 'dataset' = 'CrudeOilPrices', 
               'stock_id' = list('Brent', 'WTI'), 
               'date'='2019-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# RawMaterialFuturesPrices
payload<-list( 'dataset' = 'RawMaterialFuturesPrices', 
               'stock_id' = '', 
               'date'='2019-06-01' )

response = POST(list_url,body =payload,encode="json")
data = response %>% content 
data = do.call('c',data$data)

# RawMaterialFuturesPrices
payload<-list( 'dataset' = 'RawMaterialFuturesPrices', 
               'stock_id' = list('US Wheat Futures', 'Tin Futures'), 
               'date'='2019-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# GoldPrice
payload<-list( 'dataset' = 'GoldPrice', 
               'stock_id' = '', 
               'date'='2019-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# CurrencyCirculation
payload<-list( 'dataset' = 'CurrencyCirculation', 
               'stock_id' = '', 
               'date'='2019-06-01' )

response = POST(list_url,body =payload,encode="json")
data = response %>% content 
data = do.call('c',data$data)

# CurrencyCirculation
payload<-list( 'dataset' = 'CurrencyCirculation', 
               'stock_id' = list('US'), 
               'date'='2018-01-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)







