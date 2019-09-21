## Python
###### Arguments

* **dataset** : string.
* **stock_id** : list. USing for stock related dataset.
* **data_id** : list. USing for non stock related dataset, e.g exchange rate, crude oil prices.
* **date** : string. Data time interval is **date** ~ now.( e.g '2019-01-01' )

#### Example

      from FinMind.Data import Load
      import requests
      import pandas as pd
      url = 'http://finmindapi.servebeer.com/api/data'
      list_url = 'http://finmindapi.servebeer.com/api/datalist'
      translate_url = 'http://finmindapi.servebeer.com/api/translation'

* Load Taiwan Stock info 股票資訊

      form_data = {'dataset':'TaiwanStockInfo'}
      res = requests.post(
              url,verify = True,
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

* Load Taiwan Stock Price 股價

      form_data = {'dataset':'TaiwanStockPrice',
                   'stock_id':'2330',
                   'date':'2019-06-01'}
      res = requests.post(
              url,verify = True,
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

* Load Taiwan Stock Financial Statements 財報

      form_data = {'dataset':'FinancialStatements',
                   'stock_id':'2330',
                   'date':'2019-01-01'}
      res = requests.post(
              url,verify = True,
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data = Load.transpose(data)
      data.head()

* Load Taiwan Stock Stock Dividend 股息股利

      form_data = {'dataset':'TaiwanStockStockDividend',
                   'stock_id':'2317',
                   'date':'2018-01-01'}
      res = requests.post(
              url,verify = True,
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()


* Load Taiwan Stock Margin Purchase Short Sale 融資融券

      form_data = {'dataset':'TaiwanStockMarginPurchaseShortSale',
                   'stock_id':'2317',
                   'date':'2019-06-01'}
      res = requests.post(
              url,verify = True,
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

* Load Taiwan Stock Institutional Investors Buy Sell 個股外資買賣

      form_data = {'dataset':'InstitutionalInvestorsBuySell',
                   'stock_id':'2317',
                   'date':'2019-06-01'}
      res = requests.post(
              url,verify = True,
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()


* Load Taiwan Stock Share holding 外資持股

      form_data = {'dataset':'Shareholding',
                   'stock_id':'2317',
                   'date':'2019-06-01'}
      res = requests.post(
              url,verify = True,
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

* Load Taiwan Stock Balance Sheet 資產負債表

      form_data = {'dataset':'BalanceSheet',
                   'stock_id':'2317',
                   'date':'2019-01-01'}
      res = requests.post(
              url,verify = True,
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

* Load Taiwan Stock Holding Shares Per 股權分散表

      form_data = {'dataset':'TaiwanStockHoldingSharesPer',
                   'stock_id':'2317',
                   'date':'2019-06-01'}
      res = requests.post(
              url,verify = True,
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

* Load Taiwan Stock Month Revenue 月營收

      form_data = {'dataset':'TaiwanStockMonthRevenue',
                   'stock_id':'2317',
                   'date':'2019-01-01'}
      res = requests.post(
              url,verify = True,
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

* Load Taiwan Option 台股選擇權，

        #load stock_id table, 讀取代碼表，用於輸入以下 stock_id 參數
		form_data = {'dataset':'TaiwanOption'}
		res = requests.post(
			  translate_url,verify = True,
			  data = form_data)
		temp = res.json()
		data = pd.DataFrame(temp['data'])
		data.head()

		parameter = {'dataset':'TaiwanOption',
				   'stock_id':'OCO',
				   'date':'2019-09-05',
				   }

		res = requests.post(
			  url,verify = True,
			  data = form_data)

		temp = res.json()
		data = pd.DataFrame(temp['data'])
		data.head()

* Load Taiwan Futures 台股期貨明細，由於資料過多，只會回傳 date 當天 data，如要長期資料，請用 loop call api

      #load stock_id table, 讀取代碼表，用於輸入以下 stock_id 參數
      form_data = {'dataset':'TaiwanFutures'}
      res = requests.post(
            translate_url,verify = True,
            data = form_data)
      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

      parameter = {'dataset':'TaiwanFutures',
                 'stock_id':'MTX',
                 'date':'2019-09-02',
                 }

      res = requests.post(
            url,verify = True,
            data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

* Load US Stock Info 美股股票資訊

      form_data = {'dataset':'USStockInfo'}
      res = requests.post(
              url,verify = True,
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

* Load US Stock Price 美股股價

      form_data = {'dataset':'USStockPrice',
                   'stock_id':'^GSPC',
                   'date':'2019-06-01'}
      res = requests.post(
              url,verify = True,
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

* Load US Stock Financial Statements 財報

      form_data = {'dataset':'FinancialStatements',
                   'stock_id':'AAPL',
                   'date':'2018-01-01'}
      res = requests.post(
              url,verify = True,
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

* Load Japan Stock Info 日股股票資訊

      form_data = {'dataset':'JapanStockInfo'}
      res = requests.post(
              url,verify = True,
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

* Load Japan Stock Price 日股股價

      form_data = {'dataset':'JapanStockPrice',
                   'stock_id':'1376.T',
                   'date':'2019-06-01'}
      res = requests.post(
              url,verify = True,
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

* Load UK Stock Info 英股股票資訊

      form_data = {'dataset':'UKStockInfo',
                   'stock_id':'2317',
                   'date':'2019-06-01'}
      res = requests.post(
              url,verify = True,
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

* Load UK Stock Price 英股股價

      form_data = {'dataset':'UKStockPrice',
                   'stock_id':'0TWH.L',
                   'date':'2019-06-01'}
      res = requests.post(
              url,verify = True,
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

* Load Europe Stock Info  歐股股票資訊

      form_data = {'dataset':'EuropeStockInfo'}
      res = requests.post(
              url,verify = True,
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()


* Load Europe Stock Price 歐股股價

      form_data = {'dataset':'EuropeStockPrice',
                   'stock_id':'ABCA.PA',
                   'date':'2019-06-01'}
      res = requests.post(
              url,verify = True,
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

* Load list of Exchange Rate 匯率列表


      form_data = {'dataset':'ExchangeRate'}
      res = requests.post(
              list_url,verify = True,
              data = form_data)

      temp = res.json()
      data = temp['data']
      data


* Load Exchange Rate 匯率

      form_data = {'dataset':'ExchangeRate',
                   'data_id':'Taiwan',
                   'date':'2019-06-01'}
      res = requests.post(
              url,verify = True,
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

* Load list of Institutional Investors 外資列表


      form_data = {'dataset':'InstitutionalInvestors'}
      res = requests.post(
              list_url,verify = True,
              data = form_data)

      temp = res.json()
      data = temp['data']
      data

* Load Institutional Investors 整體外資買賣


      form_data = {'dataset':'InstitutionalInvestors',
                   'data_id':'Dealer_Hedging',
                   'date':'2019-06-01'}
      res = requests.post(
              url,verify = True,
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()


* Load list of Interest Rate 各國利率列表

      form_data = {'dataset':'InterestRate'}
      res = requests.post(
              list_url,verify = True,
              data = form_data)

      temp = res.json()
      data = temp['data']
      data


* Load Interest Rate 利率

      form_data = {'dataset':'InterestRate',
                   'data_id':'BOC',
                   'date':'2019-06-01'}
      res = requests.post(
              url,verify = True,
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()


* Load list of Government Bonds 政府債券列表

      form_data = {'dataset':'GovernmentBonds'}
      res = requests.post(
              list_url,verify = True,
              data = form_data)

      temp = res.json()
      data = temp['data']
      data

* Load Government Bonds 政府債券


      form_data = {'dataset':'GovernmentBonds',
                   'data_id':'France 9-Year',
                   'date':'2019-06-01'}
      res = requests.post(
              url,verify = True,
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

* Load list of Crude Oil Prices 油價列表

      form_data = {'dataset':'CrudeOilPrices'}
      res = requests.post(
              list_url,verify = True,
              data = form_data)

      temp = res.json()
      data = temp['data']
      data

* Load Crude Oil Prices 油價

      form_data = {'dataset':'CrudeOilPrices',
                   'data_id': 'WTI',
                   'date':'2019-06-01'}
      res = requests.post(
              url,verify = True,
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

* Load list of Raw Material Futures Prices 原物料期貨列表

      form_data = {'dataset':'RawMaterialFuturesPrices'}
      res = requests.post(
              list_url,verify = True,
              data = form_data)

      temp = res.json()
      data = temp['data']
      data

* Load Raw Material Futures Prices 原物料期貨

      form_data = {'dataset':'RawMaterialFuturesPrices',
                   'data_id':'US Soybean Meal Futures',
                   'date':'2019-06-01'}
      res = requests.post(
              url,verify = True,
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()


* Load Gold Price 金價

      form_data = {'dataset':'GoldPrice','date':'2019-06-06'}
      res = requests.post(
              url,verify = True,
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

* Load list of Currency Circulation

      form_data = {'dataset':'CurrencyCirculation'}
      res = requests.post(
              list_url,verify = True,
              data = form_data)

      temp = res.json()
      data = temp['data']
      data

* Load Currency Circulation


      form_data = {'dataset':'CurrencyCirculation',
                   'data_id':'Taiwan',
                   'date':'2019-06-01'}
      res = requests.post(
              url,verify = True,
              data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

* Load list of Government Bonds Yield 政府債券殖利率列表

      form_data = {'dataset':'GovernmentBondsYield'}
      res = requests.post(
            list_url,verify = True,
            data = form_data)

      temp = res.json()
      data = temp['data']
      data

* Load Government Bonds Yield 政府債券殖利率

      form_data = {'dataset':'GovernmentBondsYield',
                  'data_id':'United States 1-Year',
                  'date':'2019-06-01'}
      res = requests.post(
            url,verify = True,
            data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

* Load Taiwan Cash Flows Statement 台灣現金流量表

      form_data = {'dataset':'TaiwanCashFlowsStatement',
                  'stock_id':'2330',
                  'date':'2019-06-01'}
      res = requests.post(
            url,verify = True,
            data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()

* Load Taiwan Stock Price Minute 台灣每分鐘股價

      form_data = {'dataset':'TaiwanStockPriceMinute',
                  'stock_id':'2330',
                  'date':'2019-06-01'}
      res = requests.post(
            url,verify = True,
            data = form_data)

      temp = res.json()
      data = pd.DataFrame(temp['data'])
      data.head()