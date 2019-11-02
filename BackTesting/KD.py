
import pandas as pd
import numpy as np
import requests

class KD:
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
        self.min_limit = 20
        self.max_limit = 80
        self.days = 9
        self.create_feature()# 建立自己的 feature or 技術指標
    
    def create_feature(self):
        def RSV(stock_price):
            '''
            if day = 9
            rsv = ( C-L9 )/( H9-L9 ) * 100
            C為第9日的收盤價；L9為9日內的最低價；H9為9日內的最高價
            '''
            min_price = stock_price['min'].rolling(9).min()
            max_price = stock_price['max'].rolling(9).max()
            close = stock_price['close']
            
            rsv = (close-min_price)/(max_price-min_price)*100
            stock_price['rsv'] = rsv
            stock_price = stock_price.dropna()
            
            return stock_price
            
        def calculate_KD(stock_price):
            '''
        　　K值＝2/3×前一日K值+1/3×當日RSV
        　　D值=2/3×前一日D值+1/3×當日K
        　　若無前一日K值與D值，則可以分別用50代替。
            '''
            K_list, D_list = [[50],[50]]
            
            for r in list( stock_price['rsv'] ):
                # r = rsv[1]
                K = K_list[-1]*2/3 + r/3
                D = D_list[-1]*2/3 + K/3
                K_list.append( K )
                D_list.append( D )
            D_list = D_list[1:]
            K_list = K_list[1:]
            
            stock_price['K'] = K_list
            stock_price['D'] = D_list
            
            return stock_price
        
        self.stock_price = RSV(self.stock_price)
        self.stock_price = calculate_KD(self.stock_price)
        
        colname = ['date','K','D']
        self.stock_price = self.stock_price[colname]
        self.stock_price = self.stock_price.sort_values('date')
        self.stock_price.index = range(len(self.stock_price))
    
    def trade(self,date):
        ''' 
        此區塊，可進行資料處理、做技術指標，寫自己的策略，
        寫你自己的策略, 必須 return : 1 (買) or -1 (賣) or 0 (不操作)
        根據時間date，回傳當下要進行什麼操作 ( 買/賣/不操作 )
        '''
        # example
        value = self.stock_price[ self.stock_price['date'] == date ]
        if len(value) == 0:
            return 0
        
        k = value['K'].values[0]
        d = value['D'].values[0]
        
        if k <= self.min_limit and d <= self.min_limit:
            return 1# buy
        elif k >= self.max_limit and d >= self.max_limit:
            return -1# sell
        else:
            return 0# no buy and no sell

def test():

    form_data = {'dataset':'TaiwanStockPrice',
                 'stock_id':'2317',
                 'date':'2019-01-01'}
    url = 'http://finmindapi.servebeer.com/api/data'
    res = requests.post(
            url,verify = True,
            data = form_data)
    
    temp = res.json()
    stock_price = pd.DataFrame(temp['data'])

    self = KD(stock_price)
    self.trade('2019-05-07')
    self.trade('2019-05-11')
    
   