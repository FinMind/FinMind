## Python
###### Arguments

* **dataset** : string.
* **stock_id** : list. USing for stock related dataset.
* **data_id** : list. USing for non stock related dataset, e.g exchange rate, crude oil prices.
* **date** : string. Data time interval is **date** ~ now.( e.g '2019-01-01' )

#### Example

* Load Taiwan Stock info

      from FinMind.Data import Load
      import requests
      import pandas as pd
      url = 'http://finmindapi.servebeer.com/api/data'
      list_url = 'http://finmindapi.servebeer.com/api/datalist'


      form_data = {'dataset':'TaiwanStockInfo',
                   'stock_id':'',
                   'date':''}
      res = requests.post(
              url,verify = True,headers = {},
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

* Load Taiwan Stock Price

      form_data = {'dataset':'TaiwanStockPrice',
                   'stock_id':['2330','2317'],
                   'date':'2019-06-01'}
      res = requests.post(
              url,verify = True,headers = {},
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

* Load Taiwan Stock Financial Statements

      form_data = {'dataset':'FinancialStatements',
                   'stock_id':['2330','2317'],
                   'date':'2019-01-01'}
      res = requests.post(
              url,verify = True,headers = {},
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data = Load.transpose(data)
      data.head()

* Load Taiwan Stock Stock Dividend

      form_data = {'dataset':'TaiwanStockStockDividend',
                   'stock_id':['2330','2317'],
                   'date':'2018-01-01'}
      res = requests.post(
              url,verify = True,headers = {},
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()


* Load Taiwan Stock Margin Purchase Short Sale

      form_data = {'dataset':'TaiwanStockMarginPurchaseShortSale',
                   'stock_id':['2330','2317'],
                   'date':'2019-06-01'}
      res = requests.post(
              url,verify = True,headers = {},
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

* Load Taiwan Stock Institutional Investors Buy Sell

      form_data = {'dataset':'InstitutionalInvestorsBuySell',
                   'stock_id':['2330','2317'],
                   'date':'2019-06-01'}
      res = requests.post(
              url,verify = True,headers = {},
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()


* Load Taiwan Stock Share holding

      form_data = {'dataset':'Shareholding',
                   'stock_id':['2330','2317'],
                   'date':'2019-06-01'}
      res = requests.post(
              url,verify = True,headers = {},
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

* Load Taiwan Stock Balance Sheet

      form_data = {'dataset':'BalanceSheet',
                   'stock_id':['2330','2317'],
                   'date':'2019-01-01'}
      res = requests.post(
              url,verify = True,headers = {},
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

* Load Taiwan Stock Holding Shares Per

      form_data = {'dataset':'TaiwanStockHoldingSharesPer',
                   'stock_id':['2330','2317'],
                   'date':'2019-06-01'}
      res = requests.post(
              url,verify = True,headers = {},
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

* Load Taiwan Stock Month Revenue

      form_data = {'dataset':'TaiwanStockMonthRevenue',
                   'stock_id':['2330','2317'],
                   'date':'2019-01-01'}
      res = requests.post(
              url,verify = True,headers = {},
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

* Load US Stock Info

      form_data = {'dataset':'USStockInfo',
                   'stock_id':'',
                   'date':''}
      res = requests.post(
              url,verify = True,headers = {},
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

* Load US Stock Price

      form_data = {'dataset':'USStockPrice',
                   'stock_id':['^GSPC','^DJI'],
                   'date':'2019-06-01'}
      res = requests.post(
              url,verify = True,headers = {},
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

* Load US Stock Financial Statements

      form_data = {'dataset':'FinancialStatements',
                   'stock_id':['AAPL'],
                   'date':'2018-01-01'}
      res = requests.post(
              url,verify = True,headers = {},
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

* Load Japan Stock Info

      form_data = {'dataset':'JapanStockInfo',
                   'stock_id':'',
                   'date':''}
      res = requests.post(
              url,verify = True,headers = {},
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

* Load Japan Stock Price

      form_data = {'dataset':'JapanStockPrice',
                   'stock_id':['1352.T','1376.T'],
                   'date':'2019-06-01'}
      res = requests.post(
              url,verify = True,headers = {},
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

* Load UK Stock Info

      form_data = {'dataset':'UKStockInfo',
                   'stock_id':['2330','2317'],
                   'date':'2019-06-01'}
      res = requests.post(
              url,verify = True,headers = {},
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

* Load UK Stock Price

      form_data = {'dataset':'UKStockPrice',
                   'stock_id':['0TWH.L','0HZU.L'],
                   'date':'2019-06-01'}
      res = requests.post(
              url,verify = True,headers = {},
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

* Load Europe Stock Info

      form_data = {'dataset':'EuropeStockInfo',
                   'stock_id':'',
                   'date':''}
      res = requests.post(
              url,verify = True,headers = {},
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()


* Load Europe Stock Price

      form_data = {'dataset':'EuropeStockPrice',
                   'stock_id':['AB.PA','ABCA.PA'],
                   'date':'2019-06-01'}
      res = requests.post(
              url,verify = True,headers = {},
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

* Load list of Exchange Rate


      form_data = {'dataset':'ExchangeRate',}
      res = requests.post(
              list_url,verify = True,headers = {},
              data = form_data)

      temp = res.json()
      data = temp['data']
      data


* Load Exchange Rate

      form_data = {'dataset':'ExchangeRate',
                   'data_id':['Canda', 'China', 'Euro', 'Japan', 'Taiwan', 'UK'],
                   'date':'2019-06-01'}
      res = requests.post(
              url,verify = True,headers = {},
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

* Load list of Institutional Investors


      form_data = {'dataset':'InstitutionalInvestors'}
      res = requests.post(
              list_url,verify = True,headers = {},
              data = form_data)

      temp = res.json()
      data = temp['data']
      data

* Load Institutional Investors


      form_data = {'dataset':'InstitutionalInvestors',
                   'data_id':['Dealer', 'Dealer_Hedging', 'Foreign_Investor', 'Investment_Trust'],
                   'date':'2019-06-01'}
      res = requests.post(
              url,verify = True,headers = {},
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()


* Load list of Interest Rate

      form_data = {'dataset':'InterestRate'}
      res = requests.post(
              list_url,verify = True,headers = {},
              data = form_data)

      temp = res.json()
      data = temp['data']
      data


* Load Interest Rate

      form_data = {'dataset':'InterestRate',
                   'data_id':['BCB','BOC',],
                   'date':'2019-06-01'}
      res = requests.post(
              url,verify = True,headers = {},
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()


* Load list of Government Bonds

      form_data = {'dataset':'GovernmentBonds'}
      res = requests.post(
              list_url,verify = True,headers = {},
              data = form_data)

      temp = res.json()
      data = temp['data']
      data

* Load Government Bonds


      form_data = {'dataset':'GovernmentBonds',
                   'data_id':['France 9-Month','France 9-Year'],
                   'date':'2019-06-01'}
      res = requests.post(
              url,verify = True,headers = {},
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

* Load list of Crude Oil Prices

      form_data = {'dataset':'CrudeOilPrices'}
      res = requests.post(
              list_url,verify = True,headers = {},
              data = form_data)

      temp = res.json()
      data = temp['data']
      data

* Load Crude Oil Prices

      form_data = {'dataset':'CrudeOilPrices',
                   'data_id':['Brent', 'WTI'],
                   'date':'2019-06-01'}
      res = requests.post(
              url,verify = True,headers = {},
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

* Load list of Raw Material Futures Prices

      form_data = {'dataset':'RawMaterialFuturesPrices'}
      res = requests.post(
              list_url,verify = True,headers = {},
              data = form_data)

      temp = res.json()
      data = temp['data']
      data

* Load Raw Material Futures Prices

      form_data = {'dataset':'RawMaterialFuturesPrices',
                   'data_id':['US Corn Futures','US Soybean Meal Futures',],
                   'date':'2019-06-01'}
      res = requests.post(
              url,verify = True,headers = {},
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()


* Load Gold Price

      form_data = {'dataset':'GoldPrice','date':'2019-06-06'}
      res = requests.post(
              url,verify = True,headers = {},
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

* Load list of Currency Circulation

      form_data = {'dataset':'CurrencyCirculation'}
      res = requests.post(
              list_url,verify = True,headers = {},
              data = form_data)

      temp = res.json()
      data = temp['data']
      data

* Load Currency Circulation


      form_data = {'dataset':'CurrencyCirculation',
                   'data_id':['Europe', 'Taiwan','US'],
                   'date':'2019-06-01'}
      res = requests.post(
              url,verify = True,headers = {},
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()
