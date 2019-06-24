#### R
###### Arguments

* **dataset** : string.
* **stock_id** : list. USing for stock related dataset.
* **data_id** : list. USing for non stock related dataset, e.g exchange rate, crude oil prices.
* **date** : string. Data time interval is **date** ~ now.( e.g '2019-01-01' )

#### Example

* Load Taiwan Stock info


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

* Load Taiwan Stock Price


    payload<-list( 'dataset' = 'TaiwanStockPrice', 
                   'stock_id' = list('2330','2317'), 
                   'date'='2019-06-01' )

    response = POST(url,body = payload,encode="json")
    data = response %>% content 
    data = do.call('cbind',data$data) %>%data.table
    head(data)

* Load Taiwan Stock Financial Statements


    payload<-list( 'dataset' = 'FinancialStatements', 
                   'stock_id' = list('2330','2317'), 
                   'date'='2018-06-01' )

    response = POST(url,body = payload,encode="json")
    data = response %>% content 
    data = do.call('cbind',data$data) %>%data.table
    head(data)

* Load Taiwan Stock Stock Dividend


    payload<-list( 'dataset' = 'TaiwanStockStockDividend', 
                   'stock_id' = list('2330','2317'), 
                   'date'='2019-06-01' )

    response = POST(url,body = payload,encode="json")
    data = response %>% content 
    data = do.call('cbind',data$data) %>%data.table
    head(data)

* Load Taiwan Stock Margin Purchase Short Sale


    payload<-list( 'dataset' = 'TaiwanStockMarginPurchaseShortSale', 
                   'stock_id' = list('2330','2317'), 
                   'date'='2019-06-01' )

    response = POST(url,body = payload,encode="json")
    data = response %>% content 
    data = do.call('cbind',data$data) %>%data.table
    head(data)

* Load Taiwan Stock Institutional Investors Buy Sell


    payload<-list( 'dataset' = 'InstitutionalInvestorsBuySell', 
                   'stock_id' = list('2330','2317'), 
                   'date'='2019-06-01' )

    response = POST(url,body = payload,encode="json")
    data = response %>% content 
    data = do.call('cbind',data$data) %>%data.table
    head(data)

* Load Taiwan Stock Share holding


    payload<-list( 'dataset' = 'Shareholding', 
                   'stock_id' = list('2330','2317'), 
                   'date'='2019-06-01' )

    response = POST(url,body = payload,encode="json")
    data = response %>% content 
    data = do.call('cbind',data$data) %>%data.table
    head(data)

* Load Taiwan Stock Balance Sheet


    payload<-list( 'dataset' = 'BalanceSheet', 
                   'stock_id' = list('2330','2317'), 
                   'date'='2018-06-01' )

    response = POST(url,body = payload,encode="json")
    data = response %>% content 
    data = do.call('cbind',data$data) %>%data.table
    head(data)

* Load Taiwan Stock Holding Shares Per


    payload<-list( 'dataset' = 'TaiwanStockHoldingSharesPer', 
                   'stock_id' = list('2330','2317'), 
                   'date'='2019-06-01' )

    response = POST(url,body = payload,encode="json")
    data = response %>% content 
    data = do.call('cbind',data$data) %>%data.table
    head(data)

* Load Taiwan Stock Month Revenue


    payload<-list( 'dataset' = 'TaiwanStockMonthRevenue', 
                   'stock_id' = list('2330','2317'), 
                   'date'='2019-01-01' )

    response = POST(url,body = payload,encode="json")
    data = response %>% content 
    data = do.call('cbind',data$data) %>%data.table
    head(data)

* Load US Stock Info


    payload<-list( 'dataset' = 'USStockInfo', 
                   'stock_id' = '', 
                   'date'='' )

    response = POST(url,body = payload,encode="json")
    data = response %>% content 
    data = do.call('cbind',data$data) %>%data.table
    head(data)

* Load US Stock Price


    payload<-list( 'dataset' = 'USStockPrice', 
                   'stock_id' = list('^GSPC','^DJI'), 
                   'date'='2019-06-01' )

    response = POST(url,body = payload,encode="json")
    data = response %>% content 
    data = do.call('cbind',data$data) %>%data.table
    head(data)

* Load US Stock Financial Statements


    payload<-list( 'dataset' = 'FinancialStatements', 
                   'stock_id' = list('AAPL'), 
                   'date'='2018-06-01' )

    response = POST(url,body = payload,encode="json")
    data = response %>% content 
    data = do.call('cbind',data$data) %>%data.table
    head(data)

* Load Japan Stock Info


    payload<-list( 'dataset' = 'JapanStockInfo', 
                   'stock_id' = '', 
                   'date'='2019-06-01' )

    response = POST(url,body = payload,encode="json")
    data = response %>% content 
    data = do.call('cbind',data$data) %>%data.table
    head(data)

* Load Japan Stock Price


    payload<-list( 'dataset' = 'JapanStockPrice', 
                   'stock_id' = list('1352.T','1376.T'), 
                   'date'='2019-06-01' )

    response = POST(url,body = payload,encode="json")
    data = response %>% content 
    data = do.call('cbind',data$data) %>%data.table
    head(data)

* Load UK Stock Info


    payload<-list( 'dataset' = 'UKStockInfo', 
                   'stock_id' = '', 
                   'date'='2019-06-01' )

    response = POST(url,body = payload,encode="json")
    data = response %>% content 
    data = do.call('cbind',data$data) %>%data.table
    head(data)

* Load UK Stock Price


    payload<-list( 'dataset' = 'UKStockPrice', 
                   'stock_id' = list('0TWH.L','0HZU.L'), 
                   'date'='2019-06-01' )

    response = POST(url,body = payload,encode="json")
    data = response %>% content 
    data = do.call('cbind',data$data) %>%data.table
    head(data)

* Load Europe Stock Info


    payload<-list( 'dataset' = 'EuropeStockInfo', 
                   'stock_id' = '', 
                   'date'='2019-06-01' )

    response = POST(url,body = payload,encode="json")
    data = response %>% content 
    data = do.call('cbind',data$data) %>%data.table
    head(data)

* Load Europe Stock Price


    payload<-list( 'dataset' = 'EuropeStockPrice', 
                   'stock_id' = list('AB.PA','ABCA.PA'), 
                   'date'='2019-06-01' )

    response = POST(url,body = payload,encode="json")
    data = response %>% content 
    data = do.call('cbind',data$data) %>%data.table
    head(data)

* Load list of Exchange Rate


    payload<-list( 'dataset' = 'ExchangeRate' )

    response = POST(list_url,body = payload,encode="json")
    data = response %>% content 
    data = do.call('c',data$data)

* Load Exchange Rate


    payload<-list( 'dataset' = 'ExchangeRate', 
                   'data_id' = list('Canda', 'China', 'Euro', 'Japan', 'Taiwan', 'UK'), 
                   'date'='2019-06-01' )

    response = POST(url,body = payload,encode="json")
    data = response %>% content 
    data = do.call('cbind',data$data) %>%data.table
    head(data)

* Load lsit of Institutional Investors


    payload<-list( 'dataset' = 'InstitutionalInvestors')

    response = POST(list_url,body = payload,encode="json")
    data = response %>% content 
    data = do.call('c',data$data)

* Load Institutional Investors


    payload<-list( 'dataset' = 'InstitutionalInvestors', 
                   'data_id' = list('Dealer'), 
                   'date'='2019-06-01' )

    response = POST(url,body = payload,encode="json")
    data = response %>% content 
    data = do.call('cbind',data$data) %>%data.table
    head(data)

* Load lsit of Interest Rate


    payload<-list( 'dataset' = 'InterestRate',  )

    response = POST(list_url,body = payload,encode="json")
    data = response %>% content 
    data = do.call('c',data$data)

* Load Interest Rate


    payload<-list( 'dataset' = 'InterestRate', 
                   'data_id' = list('BCB','BOC'), 
                   'date'='2019-06-01' )

    response = POST(url,body = payload,encode="json")
    data = response %>% content 
    data = do.call('cbind',data$data) %>%data.table
    head(data)

* Load lsit of Government Bonds


    payload<-list( 'dataset' = 'GovernmentBonds' )

    response = POST(list_url,body = payload,encode="json")
    data = response %>% content 
    data = do.call('c',data$data) 

* Load Government Bonds


    payload<-list( 'dataset' = 'GovernmentBonds', 
                   'data_id' = list('France 9-Month','France 9-Year'), 
                   'date'='2019-06-01' )

    response = POST(url,body = payload,encode="json")
    data = response %>% content 
    data = do.call('cbind',data$data) %>%data.table
    head(data)

* Load lsit of Crude Oil Prices


    payload<-list( 'dataset' = 'CrudeOilPrices' )

    response = POST(list_url,body = payload,encode="json")
    data = response %>% content 
    data = do.call('c',data$data)

* Load Crude Oil Prices


    payload<-list( 'dataset' = 'CrudeOilPrices', 
                   'data_id' = list('Brent', 'WTI'), 
                   'date'='2019-06-01' )

    response = POST(url,body = payload,encode="json")
    data = response %>% content 
    data = do.call('cbind',data$data) %>%data.table
    head(data)

* Load list of Raw Material Futures Prices


    payload<-list( 'dataset' = 'RawMaterialFuturesPrices' )

    response = POST(list_url,body = payload,encode="json")
    data = response %>% content 
    data = do.call('c',data$data)

* Load Raw Material Futures Prices


    payload<-list( 'dataset' = 'RawMaterialFuturesPrices', 
                   'data_id' = list('US Wheat Futures', 'Tin Futures'), 
                   'date'='2019-06-01' )

    response = POST(url,body = payload,encode="json")
    data = response %>% content 
    data = do.call('cbind',data$data) %>%data.table
    head(data)

* Load Gold Price


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
                   'stock_id' = list('US'), 
                   'date'='2018-01-01' )

    response = POST(url,body = payload,encode="json")
    data = response %>% content 
    data = do.call('cbind',data$data) %>%data.table
    head(data)


