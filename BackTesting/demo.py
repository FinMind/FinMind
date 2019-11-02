
import pandas as pd
from random import randint
import requests

class demo:
    def __init__(self,
                 stock_price,
                 **kwargs,):
        
        stock_price = stock_price.sort_values('date')
        
        self.stock_price = stock_price
        self.MarginPurchaseShortSale = kwargs.get("MarginPurchaseShortSale", pd.DataFrame())
        self.InstitutionalInvestorsBuySell = kwargs.get("InstitutionalInvestorsBuySell", pd.DataFrame())
        self.Shareholding = kwargs.get("Shareholding", pd.DataFrame())
        #-------------------------------------------------------------------
    
    def trade(self,date):
        x = randint(1,10)
        x = x%3
        if x == 1:
            return 1
        elif x == 2:
            return -1
        elif x == 0:
            return 0


def test():
    
    url = 'http://finmindapi.servebeer.com/api/data'
    form_data = {'dataset':'TaiwanStockPrice',
                 'stock_id':'2330',
                 'date':'2018-06-01'}
    
    res = requests.post(url,verify = True,data = form_data)
        
    temp = res.json()
    stock_price = pd.DataFrame(temp['data'])

            
    form_data = {'dataset':'TaiwanStockMarginPurchaseShortSale',
    	   'stock_id':'2317',
    	   'date':'2019-06-01'}
    res = requests.post(
          url,verify = True,
          data = form_data)
    
    temp = res.json()
    MarginPurchaseShortSale = pd.DataFrame(temp['data'])

    
    form_data = {'dataset':'InstitutionalInvestorsBuySell',
  	   'stock_id':'2317',
  	   'date':'2019-06-01'}
    res = requests.post(
        url,verify = True,
        data = form_data)

    temp = res.json()
    InstitutionalInvestorsBuySell = pd.DataFrame(temp['data'])


    form_data = {'dataset':'Shareholding',
  	   'stock_id':'2317',
  	   'date':'2019-06-01'}
    res = requests.post(
        url,verify = True,
        data = form_data)

    temp = res.json()
    Shareholding = pd.DataFrame(temp['data'])

    
    self = demo(
            stock_price = stock_price,
            MarginPurchaseShortSale = MarginPurchaseShortSale,
            InstitutionalInvestorsBuySell = InstitutionalInvestorsBuySell,
            Shareholding = Shareholding,)
    
    
    
    
    


