## R
###### Arguments

* **dataset** : string.
* **stock_id** : list. USing for stock related dataset.
* **data_id** : list. USing for non stock related dataset, e.g exchange rate, crude oil prices.
* **date** : string. Data time interval is **date** ~ now.( e.g '2019-01-01' )

#### Example

* Load Taiwan Stock info 股票資訊


        library(httr)
        library(jsonlite)
        library('data.table')
        library(dplyr)

        url = 'http://finmindapi.servebeer.com/api/data'
        list_url = 'http://finmindapi.servebeer.com/api/datalist'

        payload<-list( 'dataset' = 'TaiwanStockInfo')

        response = POST(url,body = payload,encode="json")
        data = response %>% content
        data = do.call('cbind',data$data) %>%data.table
        head(data)

* Load Taiwan Stock Price 股價


            payload<-list( 'dataset' = 'TaiwanStockPrice',
                           'stock_id' = '2317',
                           'date'='2019-06-01' )

            response = POST(url,body = payload,encode="json")
            data = response %>% content
            data = do.call('cbind',data$data) %>%data.table
            head(data)

* Load Taiwan Stock Financial Statements 財報


            payload<-list( 'dataset' = 'FinancialStatements',
                           'stock_id' = '2317',
                           'date'='2018-06-01' )

            response = POST(url,body = payload,encode="json")
            data = response %>% content
            data = do.call('cbind',data$data) %>%data.table
            head(data)

* Load Taiwan Stock Stock Dividend 股息股利


            payload<-list( 'dataset' = 'TaiwanStockStockDividend',
                           'stock_id' = '2317',
                           'date'='2019-06-01' )

            response = POST(url,body = payload,encode="json")
            data = response %>% content
            data = do.call('cbind',data$data) %>%data.table
            head(data)

* Load Taiwan Stock Margin Purchase Short Sale 融資融券


            payload<-list( 'dataset' = 'TaiwanStockMarginPurchaseShortSale',
                           'stock_id' = '2317',
                           'date'='2019-06-01' )

            response = POST(url,body = payload,encode="json")
            data = response %>% content
            data = do.call('cbind',data$data) %>%data.table
            head(data)

* Load Taiwan Stock Institutional Investors Buy Sell 個股外資買賣


            payload<-list( 'dataset' = 'InstitutionalInvestorsBuySell',
                           'stock_id' = '2317',
                           'date'='2019-06-01' )

            response = POST(url,body = payload,encode="json")
            data = response %>% content
            data = do.call('cbind',data$data) %>%data.table
            head(data)

* Load Taiwan Stock Share holding 外資持股


            payload<-list( 'dataset' = 'Shareholding',
                           'stock_id' = '2317',
                           'date'='2019-06-01' )

            response = POST(url,body = payload,encode="json")
            data = response %>% content
            data = do.call('cbind',data$data) %>%data.table
            head(data)

* Load Taiwan Stock Balance Sheet 資產負債表


            payload<-list( 'dataset' = 'BalanceSheet',
                           'stock_id' = '2317',
                           'date'='2018-06-01' )

            response = POST(url,body = payload,encode="json")
            data = response %>% content
            data = do.call('cbind',data$data) %>%data.table
            head(data)

* Load Taiwan Stock Holding Shares Per 股權分散表


            payload<-list( 'dataset' = 'TaiwanStockHoldingSharesPer',
                           'stock_id' = '2317',
                           'date'='2019-06-01' )

            response = POST(url,body = payload,encode="json")
            data = response %>% content
            data = do.call('cbind',data$data) %>%data.table
            head(data)

* Load Taiwan Stock Month Revenue 月營收


            payload<-list( 'dataset' = 'TaiwanStockMonthRevenue',
                           'stock_id' = '2317',
                           'date'='2019-01-01' )

            response = POST(url,body = payload,encode="json")
            data = response %>% content
            data = do.call('cbind',data$data) %>%data.table
            head(data)

* Load US Stock Info 美股股票資訊


            payload<-list( 'dataset' = 'USStockInfo' )

            response = POST(url,body = payload,encode="json")
            data = response %>% content
            data = do.call('cbind',data$data) %>%data.table
            head(data)

* Load US Stock Price 美股股價


            payload<-list( 'dataset' = 'USStockPrice',
                           'stock_id' = '^GSPC',
                           'date'='2019-06-01' )

            response = POST(url,body = payload,encode="json")
            data = response %>% content
            data = do.call('cbind',data$data) %>%data.table
            head(data)

* Load US Stock Financial Statements 財報


            payload<-list( 'dataset' = 'FinancialStatements',
                           'stock_id' = 'AAPL',
                           'date'='2018-06-01' )

            response = POST(url,body = payload,encode="json")
            data = response %>% content
            data = do.call('cbind',data$data) %>%data.table
            head(data)

* Load Japan Stock Info 日股股票資訊


            payload<-list( 'dataset' = 'JapanStockInfo')

            response = POST(url,body = payload,encode="json")
            data = response %>% content
            data = do.call('cbind',data$data) %>%data.table
            head(data)

* Load Japan Stock Price 日股股價


            payload<-list( 'dataset' = 'JapanStockPrice',
                           'stock_id' = '1376.T',
                           'date'='2019-06-01' )

            response = POST(url,body = payload,encode="json")
            data = response %>% content
            data = do.call('cbind',data$data) %>%data.table
            head(data)

* Load UK Stock Info 英股股票資訊


            payload<-list( 'dataset' = 'UKStockInfo' )

            response = POST(url,body = payload,encode="json")
            data = response %>% content
            data = do.call('cbind',data$data) %>%data.table
            head(data)

* Load UK Stock Price 英股股價


            payload<-list( 'dataset' = 'UKStockPrice',
                           'stock_id' = '0TWH.L',
                           'date'='2019-06-01' )

            response = POST(url,body = payload,encode="json")
            data = response %>% content
            data = do.call('cbind',data$data) %>%data.table
            head(data)

* Load Europe Stock Info 歐股股票資訊


            payload<-list( 'dataset' = 'EuropeStockInfo')

            response = POST(url,body = payload,encode="json")
            data = response %>% content
            data = do.call('cbind',data$data) %>%data.table
            head(data)

* Load Europe Stock Price 歐股股價


            payload<-list( 'dataset' = 'EuropeStockPrice',
                           'stock_id' = 'ABCA.PA',
                           'date'='2019-06-01' )

            response = POST(url,body = payload,encode="json")
            data = response %>% content
            data = do.call('cbind',data$data) %>%data.table
            head(data)

* Load list of Exchange Rate 匯率列表


            payload<-list( 'dataset' = 'ExchangeRate' )

            response = POST(list_url,body = payload,encode="json")
            data = response %>% content
            data = do.call('c',data$data)

* Load Exchange Rate 匯率


            payload<-list( 'dataset' = 'ExchangeRate',
                           'data_id' = 'Taiwan',
                           'date'='2019-06-01' )

            response = POST(url,body = payload,encode="json")
            data = response %>% content
            data = do.call('cbind',data$data) %>%data.table
            head(data)

* Load lsit of Institutional Investors 外資列表


            payload<-list( 'dataset' = 'InstitutionalInvestors')

            response = POST(list_url,body = payload,encode="json")
            data = response %>% content
            data = do.call('c',data$data)

* Load Institutional Investors 整體外資買賣


            payload<-list( 'dataset' = 'InstitutionalInvestors',
                           'data_id' = 'Dealer',
                           'date'='2019-06-01' )

            response = POST(url,body = payload,encode="json")
            data = response %>% content
            data = do.call('cbind',data$data) %>%data.table
            head(data)

* Load list of Interest Rate 各國利率列表


            payload<-list( 'dataset' = 'InterestRate' )

            response = POST(list_url,body = payload,encode="json")
            data = response %>% content
            data = do.call('c',data$data)

* Load Interest Rate 利率


            payload<-list( 'dataset' = 'InterestRate',
                           'data_id' = 'BOC',
                           'date'='2019-06-01' )

            response = POST(url,body = payload,encode="json")
            data = response %>% content
            data = do.call('cbind',data$data) %>%data.table
            head(data)

* Load lsit of Government Bonds 政府債券列表


            payload<-list( 'dataset' = 'GovernmentBonds' )

            response = POST(list_url,body = payload,encode="json")
            data = response %>% content
            data = do.call('c',data$data)

* Load Government Bonds 政府債券


            payload<-list( 'dataset' = 'GovernmentBonds',
                           'data_id' = 'France 9-Year',
                           'date'='2019-06-01' )

            response = POST(url,body = payload,encode="json")
            data = response %>% content
            data = do.call('cbind',data$data) %>%data.table
            head(data)

* Load lsit of Crude Oil Prices 油價列表


            payload<-list( 'dataset' = 'CrudeOilPrices' )

            response = POST(list_url,body = payload,encode="json")
            data = response %>% content
            data = do.call('c',data$data)

* Load Crude Oil Prices 油價


            payload<-list( 'dataset' = 'CrudeOilPrices',
                           'data_id' = 'WTI',
                           'date'='2019-06-01' )

            response = POST(url,body = payload,encode="json")
            data = response %>% content
            data = do.call('cbind',data$data) %>%data.table
            head(data)

* Load list of Raw Material Futures Prices 原物料期貨列表


            payload<-list( 'dataset' = 'RawMaterialFuturesPrices' )

            response = POST(list_url,body = payload,encode="json")
            data = response %>% content
            data = do.call('c',data$data)

* Load Raw Material Futures Prices 原物料期貨


            payload<-list( 'dataset' = 'RawMaterialFuturesPrices',
                           'data_id' = 'Tin Futures',
                           'date'='2019-06-01' )

            response = POST(url,body = payload,encode="json")
            data = response %>% content
            data = do.call('cbind',data$data) %>%data.table
            head(data)

* Load Gold Price 金價


            payload<-list( 'dataset' = 'GoldPrice', 'date'='2019-06-01' )

            response = POST(url,body = payload,encode="json")
            data = response %>% content
            data = do.call('cbind',data$data) %>%data.table
            head(data)

* Load list of Currency Circulation


            payload<-list( 'dataset' = 'CurrencyCirculation' )

            response = POST(list_url,body = payload,encode="json")
            data = response %>% content
            data = do.call('c',data$data)

* Load Currency Circulation


            payload<-list( 'dataset' = 'CurrencyCirculation',
                           'data_id' = 'US',
                           'date'='2018-01-01' )

            response = POST(url,body = payload,encode="json")
            data = response %>% content
            data = do.call('cbind',data$data) %>%data.table
            head(data)

* Load lsit of Government Bonds Yield 政府債券殖利率列表


            payload<-list( 'dataset' = 'GovernmentBondsYield' )

            response = POST(list_url,body = payload,encode="json")
            data = response %>% content
            data = do.call('c',data$data)

* Load Government Bonds Yield 政府債券殖利率


            payload<-list( 'dataset' = 'GovernmentBondsYield',
                           'data_id' = 'United States 1-Year',
                           'date'='2019-06-01' )

            response = POST(url,body = payload,encode="json")
            data = response %>% content
            data = do.call('cbind',data$data) %>%data.table
            head(data)

* Load Taiwan Cash Flows Statement 台灣現金流量表


             payload<-list( 'dataset' = 'TaiwanCashFlowsStatement',
                            'stock_id' = '2330',
                            'date'='2019-06-01' )

            response = POST(url,body = payload,encode="json")
            data = response %>% content
            data = do.call('cbind',data$data) %>%data.table
            head(data)

* Load Taiwan Stock Price Minute 台灣每分鐘股價


             payload<-list( 'dataset' = 'TaiwanStockPriceMinute',
                            'stock_id' = '2330',
                            'date'='2019-06-01' )

            response = POST(url,body = payload,encode="json")
            data = response %>% content
            data = do.call('cbind',data$data) %>%data.table
            head(data)