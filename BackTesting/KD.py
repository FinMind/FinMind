

import requests
import pandas as pd
url = 'http://finmindapi.servebeer.com/api/data'

class KD:
    def __init__(self,stock_price,**kwargs,):
        
        self.min_limit = 20
        self.max_limit = 80
        self.days = 9
        stock_price = stock_price.sort_values('date')
        self.stock_price = stock_price
        
        # self.MarginPurchaseShortSale = kwargs.get("MarginPurchaseShortSale", pd.DataFrame())
        # self.InstitutionalInvestorsBuySell = kwargs.get("InstitutionalInvestorsBuySell", pd.DataFrame())
        # self.Shareholding = kwargs.get("Shareholding", pd.DataFrame())
        
        self.create_feature()
        
    def RSV(self):
        '''
        if day = 9
        rsv = ( C-L9 )/( H9-L9 ) * 100
        C為第9日的收盤價；L9為9日內的最低價；H9為9日內的最高價
        '''
        min_price = self.stock_price['min'].rolling(9).min()
        max_price = self.stock_price['max'].rolling(9).max()
        close = self.stock_price['close']
        
        rsv = (close-min_price)/(max_price-min_price)*100
        self.stock_price['rsv'] = rsv
        self.stock_price = self.stock_price.dropna()
        
    def calculate_KD(self):
        '''
    　　K值＝2/3×前一日K值+1/3×當日RSV
    　　D值=2/3×前一日D值+1/3×當日K
    　　若無前一日K值與D值，則可以分別用50代替。
        '''
        K_list, D_list = [[50],[50]]
        
        for r in list( self.stock_price['rsv'] ):
            # r = rsv[1]
            K = K_list[-1]*2/3 + r/3
            D = D_list[-1]*2/3 + K/3
            K_list.append( K )
            D_list.append( D )
        D_list = D_list[1:]
        K_list = K_list[1:]
        
        self.stock_price['K'] = K_list
        self.stock_price['D'] = D_list
    
    def create_feature(self):
        
        self.RSV()
        self.calculate_KD()
        
        colname = ['date','K','D']
        self.stock_price = self.stock_price[colname]
        self.stock_price = self.stock_price.sort_values('date')
        self.stock_price.index = range(len(self.stock_price))
    
    def trade(self,date):
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
    res = requests.post(
            url,verify = True,
            data = form_data)
    
    temp = res.json()
    stock_price = pd.DataFrame(temp['data'])

    self = KD(stock_price)
    self.trade('2019-05-07')
    self.trade('2019-05-11')
    
