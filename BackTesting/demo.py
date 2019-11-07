
import pandas as pd
import numpy as np
import requests

# class name，必須跟檔案名一致，例如 class demo，檔名也是 demo.py
class demo:
    def __init__(self,
                 stock_price,
                 **kwargs,):
        #-------------------------------------------------------------------    
        # 此區塊請勿更動
        stock_price = stock_price.sort_values('date')
        # 股價
        self.stock_price = stock_price
        # 融資融券
        self.MarginPurchaseShortSale = kwargs.get("MarginPurchaseShortSale", pd.DataFrame())
        # 三大法人買賣
        self.InstitutionalInvestorsBuySell = kwargs.get("InstitutionalInvestorsBuySell", pd.DataFrame())
        # 外資持股
        self.Shareholding = kwargs.get("Shareholding", pd.DataFrame())
        # 此區塊請勿更動
        #-------------------------------------------------------------------
    
    def trade(self,date):
        ''' 
        此區塊，可進行資料處理、做技術指標，寫自己的策略，
        寫你自己的策略, 必須 return : 1 (買) or -1 (賣) or 0 (不操作)
        根據時間date，回傳當下要進行什麼操作 ( 買/賣/不操作 )
        '''
        # example
        from random import randint
        
        x = randint(1,10)
        x = x%3
        if x == 1:
            return 1
        elif x == 2:
            return -1
        elif x == 0:
            return 0


def test():
    '''
    測試
    '''
    stock_id = '2330'
    date = '2018-01-01'
    
    url = 'http://finmindapi.servebeer.com/api/data'
    form_data = {'dataset':'TaiwanStockPrice',
                 'stock_id':stock_id,
                 'date':date}
    
    res = requests.post(url,verify = True,data = form_data)
        
    temp = res.json()
    stock_price = pd.DataFrame(temp['data'])

            
    form_data = {'dataset':'TaiwanStockMarginPurchaseShortSale',
    	   'stock_id':stock_id,
    	   'date':date}
    res = requests.post(
          url,verify = True,
          data = form_data)
    
    temp = res.json()
    MarginPurchaseShortSale = pd.DataFrame(temp['data'])

    
    form_data = {'dataset':'InstitutionalInvestorsBuySell',
  	   'stock_id':stock_id,
  	   'date':date}
    res = requests.post(
        url,verify = True,
        data = form_data)

    temp = res.json()
    InstitutionalInvestorsBuySell = pd.DataFrame(temp['data'])


    form_data = {'dataset':'Shareholding',
  	   'stock_id':stock_id,
  	   'date':date}
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
    
    self.trade('2019-05-03')
    self.trade('2019-05-05')
    
    


