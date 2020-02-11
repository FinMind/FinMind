
'''
example of loading FinMind api
'''

from FinMind.Data import Load
import requests
import pandas as pd
import datetime

today = str(datetime.datetime.now().date())

url = 'http://finmindapi.servebeer.com/api/data'
list_url = 'http://finmindapi.servebeer.com/api/datalist'
translate_url = 'http://finmindapi.servebeer.com/api/translation'

'''----------------TaiwanStockInfo----------------'''
form_data = {'dataset':'TaiwanStockInfo'}
res = requests.post(
        url,verify = True,
        data = form_data)

temp = res.json()
data = pd.DataFrame(temp['data'])
data.head()

'''----------------Taiwan Stock Dividend Result----------------'''
form_data = {'dataset':'StockDividendResult'}
res = requests.post(
        url,verify = True,
        data = form_data)

temp = res.json()
data = pd.DataFrame(temp['data'])
data.head()

'''----------------TotalMarginPurchaseShortSale----------------'''
form_data = {'dataset':'StockDividendResult',
             'stock_id':'2330',
             'date':today}
res = requests.post(
        url,verify = True,
        data = form_data)

temp = res.json()
data = pd.DataFrame(temp['data'])
data.head()

'''----------------TaiwanStockNews----------------'''
form_data = {'dataset':'TaiwanStockNews',
             'date':today,
             'stock_id':'2317'}
res = requests.post(
        url,verify = True,
        data = form_data)

temp = res.json()
data = pd.DataFrame(temp['data'])
data.head()

'''----------------TaiwanStockPrice----------------'''
form_data = {'dataset':'TaiwanStockPrice',
             'stock_id':'2317',
             'date':today}
res = requests.post(
        url,verify = True,
        data = form_data)

temp = res.json()
data = pd.DataFrame(temp['data'])
data.head()

'''----------------TaiwanStockPriceMinute----------------'''
form_data = {'dataset':'TaiwanStockPriceMinute',
             'stock_id':'2330',
             'date':today}
res = requests.post(
        url,verify = True,
        data = form_data)

temp = res.json()
data = pd.DataFrame(temp['data'])
data.head()

'''----------------FinancialStatements----------------'''
form_data = {'dataset':'FinancialStatements',
             'stock_id':'2317',
             'date':'2019-01-01'}
res = requests.post(
        url,verify = True,
        data = form_data)

temp = res.json()
data = pd.DataFrame(temp['data'])
#data = Load.transpose(data)
#data.head()

'''----------------TaiwanCashFlowsStatement----------------'''
form_data = {'dataset':'TaiwanCashFlowsStatement',
             'stock_id':'2330',
             'date':'2019-06-01'}
res = requests.post(
        url,verify = True,
        data = form_data)

temp = res.json()
data = pd.DataFrame(temp['data'])
data.head()

'''----------------TaiwanStockStockDividend----------------'''
form_data = {'dataset':'StockDividend',
             'stock_id':'2317',
             'date':today}
res = requests.post(
        url,verify = True,
        data = form_data)

temp = res.json()
data = pd.DataFrame(temp['data'])
data.head()

'''----------------TaiwanStockStockDividend----------------'''
form_data = {'dataset':'StockDividend',
             'stock_id':'0050',
             'date':today,
             }
res = requests.post(
        url,verify = True,
        data = form_data)

temp = res.json()
data = pd.DataFrame( temp['data'] )
#data['date'] = data['date'] + '-' + data['period']
#data = data.drop('period',axis = 1)
#data = Load.transpose(data)

'''----------------TaiwanStockMarginPurchaseShortSale----------------'''
form_data = {'dataset':'TaiwanStockMarginPurchaseShortSale',
             'stock_id':'2317',
             'date':'2019-06-01'}
res = requests.post(
        url,verify = True,
        data = form_data)

temp = res.json()
data = pd.DataFrame(temp['data'])
data.head()
'''----------------TotalMarginPurchaseShortSale----------------'''
form_data = {'dataset':'TotalMarginPurchaseShortSale',
             'date':today}
res = requests.post(
        url,verify = True,
        data = form_data)

temp = res.json()
data = pd.DataFrame(temp['data'])
data.head()


'''----------------InstitutionalInvestorsBuySell----------------'''
form_data = {'dataset':'InstitutionalInvestorsBuySell',
             'stock_id':'2317',
             'date':today}
res = requests.post(
        url,verify = True,
        data = form_data)

temp = res.json()
data = pd.DataFrame(temp['data'])
data.head()


'''----------------Shareholding----------------'''
form_data = {'dataset':'Shareholding',
             'stock_id':'2317',
             'date':today}
res = requests.post(
        url,verify = True,
        data = form_data)

temp = res.json()
data = pd.DataFrame(temp['data'])
data.head()

'''----------------BalanceSheet----------------'''
form_data = {'dataset':'BalanceSheet',
             'stock_id':'2317',
             'date':'2019-01-01'}
res = requests.post(
        url,verify = True,
        data = form_data)

temp = res.json()
data = pd.DataFrame(temp['data'])
data.head()

'''----------------TaiwanStockHoldingSharesPer----------------'''
form_data = {'dataset':'TaiwanStockHoldingSharesPer',
             'stock_id':'2317',
             'date':today}
res = requests.post(
        url,verify = True,
        data = form_data)

temp = res.json()
data = pd.DataFrame(temp['data'])
data.head()

'''----------------TaiwanStockMonthRevenue----------------'''
form_data = {'dataset':'TaiwanStockMonthRevenue',
             'stock_id':'2317',
             'date':'2019-01-01'}
res = requests.post(
        url,verify = True,
        data = form_data)

temp = res.json()
data = pd.DataFrame(temp['data'])
data.head()

'''----------------TaiwanOption----------------'''
'''
form_data = {'dataset':'TaiwanOption'}
res = requests.post(
	  translate_url,verify = True,
	  data = form_data)
temp = res.json()
data = pd.DataFrame(temp['data'])
data.head()

form_data = {'dataset':'TaiwanOption',
		   'stock_id':'OCO',
		   'date':'2019-09-05',
		   }

res = requests.post(
	  url,verify = True,
	  data = form_data)

temp = res.json()
data = pd.DataFrame(temp['data'])
data.head()
'''
'''----------------TaiwanFutures----------------'''
'''
#load stock_id table, 讀取代碼表，用於輸入以下 stock_id 參數
form_data = {'dataset':'TaiwanFutures'}
res = requests.post(
	  translate_url,verify = True,
	  data = form_data)
temp = res.json()
data = pd.DataFrame(temp['data'])
data.head()

form_data = {'dataset':'TaiwanFutures',
		   'stock_id':'MTX',
		   'date':'2019-09-02',
		   }

res = requests.post(
	  url,verify = True,
	  data = form_data)

temp = res.json()
data = pd.DataFrame(temp['data'])
data.head()
'''
'''----------------USStockInfo----------------'''
form_data = {'dataset':'USStockInfo'}
res = requests.post(
        url,verify = True,
        data = form_data)

temp = res.json()
data = pd.DataFrame(temp['data'])
data.head()

'''----------------USStockPrice----------------'''
form_data = {'dataset':'USStockPrice',
             'stock_id':'^DJI',
             'date':today}
res = requests.post(
        url,verify = True,
        data = form_data)

temp = res.json()
data = pd.DataFrame(temp['data'])
data.head()

'''----------------USStockPriceMinute----------------'''
form_data = {'dataset':'USStockPriceMinute',
             'stock_id':'MTX',
             'date':today}
res = requests.post(
        url,verify = True,
        data = form_data)

temp = res.json()
data = pd.DataFrame(temp['data'])
data.head()

'''----------------FinancialStatements----------------'''
form_data = {'dataset':'FinancialStatements',
             'stock_id':'AAPL',
             'date':'2018-01-01'}
res = requests.post(
        url,verify = True,
        data = form_data)

temp = res.json()
data = pd.DataFrame(temp['data'])
data.head()

'''----------------JapanStockInfo----------------'''
form_data = {'dataset':'JapanStockInfo'}
res = requests.post(
        url,verify = True,
        data = form_data)

temp = res.json()
data = pd.DataFrame(temp['data'])
data.head()

'''----------------JapanStockPrice----------------'''
form_data = {'dataset':'JapanStockPrice',
             'stock_id':'1376.T',
             'date':today}
res = requests.post(
        url,verify = True,
        data = form_data)

temp = res.json()
data = pd.DataFrame(temp['data'])
data.head()

'''----------------UKStockInfo----------------'''
form_data = {'dataset':'UKStockInfo',
             'stock_id':'2317',
             'date':'2019-06-01'}
res = requests.post(
        url,verify = True,
        data = form_data)

temp = res.json()
data = pd.DataFrame(temp['data'])
data.head()

'''----------------UKStockPrice----------------'''
form_data = {'dataset':'UKStockPrice',
             'stock_id':'0HZU.L',
             'date':today}
res = requests.post(
        url,verify = True,
        data = form_data)

temp = res.json()
data = pd.DataFrame(temp['data'])
data.head()

'''----------------EuropeStockInfo----------------'''
form_data = {'dataset':'EuropeStockInfo'}
res = requests.post(
        url,verify = True,
        data = form_data)

temp = res.json()
data = pd.DataFrame(temp['data'])
data.head()
'''----------------EuropeStockPrice----------------'''
form_data = {'dataset':'EuropeStockPrice',
             'stock_id':'ABCA.PA',
             'date':'2019-06-01'}
res = requests.post(
        url,verify = True,
        data = form_data)

temp = res.json()
data = pd.DataFrame(temp['data'])
data.head()
'''----------------ExchangeRate----------------'''
form_data = {'dataset':'ExchangeRate',}
res = requests.post(
        list_url,verify = True,
        data = form_data)

temp = res.json()
data = temp['data']
data
'''----------------ExchangeRate----------------'''
form_data = {'dataset':'ExchangeRate',
             'data_id':'Taiwan',
             'date':today}
res = requests.post(
        url,verify = True,
        data = form_data)

temp = res.json()
data = pd.DataFrame(temp['data'])
data.head()

'''----------------InstitutionalInvestors----------------'''
form_data = {'dataset':'InstitutionalInvestors',
             'date':today}
res = requests.post(
        url,verify = True,
        data = form_data)

temp = res.json()
data = pd.DataFrame(temp['data'])
data.head()
'''----------------InterestRate----------------'''
form_data = {'dataset':'InterestRate'}
res = requests.post(
        list_url,verify = True,
        data = form_data)

temp = res.json()
data = temp['data']
data
'''----------------InterestRate----------------'''
form_data = {'dataset':'InterestRate',
             'data_id':'BOC',
             'date':'2019-06-01'}
res = requests.post(
        url,verify = True,
        data = form_data)

temp = res.json()
data = pd.DataFrame(temp['data'])
data.head()
'''----------------GovernmentBonds----------------'''
form_data = {'dataset':'GovernmentBonds'}
res = requests.post(
        list_url,verify = True,
        data = form_data)

temp = res.json()
data = temp['data']
data
'''----------------GovernmentBonds----------------'''
form_data = {'dataset':'GovernmentBonds',
             'data_id':'France 9-Year',
             'date':'2019-06-01'}
res = requests.post(
        url,verify = True,
        data = form_data)

temp = res.json()
data = pd.DataFrame(temp['data'])
data.head()
'''----------------CrudeOilPrices----------------'''
form_data = {'dataset':'CrudeOilPrices'}
res = requests.post(
        list_url,verify = True,
        data = form_data)

temp = res.json()
data = temp['data']
data
'''----------------CrudeOilPrices----------------'''
form_data = {'dataset':'CrudeOilPrices',
             'data_id': 'WTI',
             'date':today}
res = requests.post(
        url,verify = True,
        data = form_data)

temp = res.json()
data = pd.DataFrame(temp['data'])
data.head()
'''----------------RawMaterialFuturesPrices----------------'''
form_data = {'dataset':'RawMaterialFuturesPrices'}
res = requests.post(
        list_url,verify = True,
        data = form_data)

temp = res.json()
data = temp['data']
data
'''----------------RawMaterialFuturesPrices----------------'''
form_data = {'dataset':'RawMaterialFuturesPrices',
             'data_id':'US Soybean Meal Futures',
             'date':'2019-06-01'}
res = requests.post(
        url,verify = True,
        data = form_data)

temp = res.json()
data = pd.DataFrame(temp['data'])
data.head()

'''----------------RawMaterialFuturesPricesMinute----------------'''
form_data = {'dataset':'RawMaterialFuturesPricesMinute',
             'data_id':'London Robusta Coffee Futures',
             'date':'2019-08-01'}
res = requests.post(
        url,verify = True,
        data = form_data)

temp = res.json()
data = pd.DataFrame(temp['data'])
data.head()

'''----------------GoldPrice----------------'''
form_data = {'dataset':'GoldPrice','date':today}
res = requests.post(
        url,verify = True,
        data = form_data)

temp = res.json()
data = pd.DataFrame(temp['data'])
data.head()

'''----------------CurrencyCirculation----------------'''
form_data = {'dataset':'CurrencyCirculation'}
res = requests.post(
        list_url,verify = True,
        data = form_data)

temp = res.json()
data = temp['data']
data
'''----------------CurrencyCirculation----------------'''
form_data = {'dataset':'CurrencyCirculation',
             'data_id': 'Taiwan',
             'date':'2019-06-01'}
res = requests.post(
        url,verify = True,
        data = form_data)

temp = res.json()
data = pd.DataFrame(temp['data'])
data.head()
'''----------------GovernmentBondsYield----------------'''
form_data = {'dataset':'GovernmentBondsYield'}
res = requests.post(
        list_url,verify = True,
        data = form_data)

temp = res.json()
data = temp['data']
data

'''----------------GovernmentBondsYield----------------'''
form_data = {'dataset':'GovernmentBondsYield',
             'data_id':'United States 1-Year',
             'date':'2019-06-01'}
res = requests.post(
        url,verify = True,
        data = form_data)

temp = res.json()
data = pd.DataFrame(temp['data'])
data.head()

