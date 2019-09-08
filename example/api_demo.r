

library(httr) 
library(jsonlite)
library('data.table')
library(dplyr)

url = 'http://finmindapi.servebeer.com/api/data'
list_url = 'http://finmindapi.servebeer.com/api/datalist'

# TaiwanStockInfo
payload<-list( 'dataset' = 'TaiwanStockInfo')

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# TaiwanStockPrice
payload<-list( 'dataset' = 'TaiwanStockPrice', 
               'stock_id' = '2330', 
               'date'='2019-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# FinancialStatements
payload<-list( 'dataset' = 'FinancialStatements', 
               'stock_id' = '2330', 
               'date'='2018-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# TaiwanStockStockDividend
payload<-list( 'dataset' = 'TaiwanStockStockDividend', 
               'stock_id' = '2317', 
               'date'='2019-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# TaiwanStockMarginPurchaseShortSale
payload<-list( 'dataset' = 'TaiwanStockMarginPurchaseShortSale', 
               'stock_id' = '2317', 
               'date'='2019-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# InstitutionalInvestorsBuySell
payload<-list( 'dataset' = 'InstitutionalInvestorsBuySell', 
               'stock_id' = '2317', 
               'date'='2019-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# Shareholding
payload<-list( 'dataset' = 'Shareholding', 
               'stock_id' = '2317', 
               'date'='2019-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# BalanceSheet
payload<-list( 'dataset' = 'BalanceSheet', 
               'stock_id' = '2317', 
               'date'='2018-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# TaiwanStockHoldingSharesPer
payload<-list( 'dataset' = 'TaiwanStockHoldingSharesPer', 
               'stock_id' = '2317', 
               'date'='2019-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# TaiwanStockMonthRevenue
payload<-list( 'dataset' = 'TaiwanStockMonthRevenue', 
               'stock_id' = '2317', 
               'date'='2019-01-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# USStockInfo
payload<-list( 'dataset' = 'USStockInfo')

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# USStockPrice
payload<-list( 'dataset' = 'USStockPrice', 
               'stock_id' = '^GSPC', 
               'date'='2019-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# FinancialStatements
payload<-list( 'dataset' = 'FinancialStatements', 
               'stock_id' = 'AAPL', 
               'date'='2018-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# JapanStockInfo
payload<-list( 'dataset' = 'JapanStockInfo')

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# JapanStockPrice
payload<-list( 'dataset' = 'JapanStockPrice', 
               'stock_id' = '1352.T', 
               'date'='2019-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# UKStockInfo
payload<-list( 'dataset' = 'UKStockInfo')

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# UKStockPrice
payload<-list( 'dataset' = 'UKStockPrice', 
               'stock_id' = '0TWH.L', 
               'date'='2019-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# EuropeStockInfo
payload<-list( 'dataset' = 'EuropeStockInfo')

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# EuropeStockPrice
payload<-list( 'dataset' = 'EuropeStockPrice', 
               'stock_id' = 'AB.PA', 
               'date'='2019-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# ExchangeRate
payload<-list( 'dataset' = 'ExchangeRate')

response = POST(list_url,body =payload,encode="json")
data = response %>% content 
data = do.call('c',data$data)

# EuropeStockInfo
payload<-list( 'dataset' = 'ExchangeRate', 
               'data_id' = 'Taiwan', 
               'date'='2019-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# InstitutionalInvestors
payload<-list( 'dataset' = 'InstitutionalInvestors' )

response = POST(list_url,body =payload,encode="json")
data = response %>% content 
data = do.call('c',data$data)

# InstitutionalInvestors
payload<-list( 'dataset' = 'InstitutionalInvestors', 
               'data_id' = 'Dealer', 
               'date'='2019-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# InterestRate
payload<-list( 'dataset' = 'InterestRate' )

response = POST(list_url,body =payload,encode="json")
data = response %>% content 
data = do.call('c',data$data)

# InterestRate
payload<-list( 'dataset' = 'InterestRate', 
               'data_id' = 'BCB', 
               'date'='2019-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# GovernmentBonds
payload<-list( 'dataset' = 'GovernmentBonds')

response = POST(list_url,body =payload,encode="json")
data = response %>% content 
data = do.call('c',data$data) 

# GovernmentBonds
payload<-list( 'dataset' = 'GovernmentBonds', 
               'data_id' = 'France 9-Year', 
               'date'='2019-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# CrudeOilPrices
payload<-list( 'dataset' = 'CrudeOilPrices' )

response = POST(list_url,body =payload,encode="json")
data = response %>% content 
data = do.call('c',data$data)

# CrudeOilPrices
payload<-list( 'dataset' = 'CrudeOilPrices', 
               'data_id' = 'Brent', 
               'date'='2019-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# RawMaterialFuturesPrices
payload<-list( 'dataset' = 'RawMaterialFuturesPrices')

response = POST(list_url,body =payload,encode="json")
data = response %>% content 
data = do.call('c',data$data)

# RawMaterialFuturesPrices
payload<-list( 'dataset' = 'RawMaterialFuturesPrices', 
               'data_id' = 'Tin Futures', 
               'date'='2019-06-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# GoldPrice
payload<-list( 'dataset' = 'GoldPrice')

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)

# CurrencyCirculation
payload<-list( 'dataset' = 'CurrencyCirculation' )

response = POST(list_url,body =payload,encode="json")
data = response %>% content 
data = do.call('c',data$data)

# CurrencyCirculation
payload<-list( 'dataset' = 'CurrencyCirculation', 
               'data_id' = 'US', 
               'date'='2018-01-01' )

response = POST(url,body =payload,encode="json")
data = response %>% content 
data = do.call('cbind',data$data) %>%data.table
head(data)
