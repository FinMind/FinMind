
import pandas as pd
import numpy as np
import requests

# class name，必須跟檔案名一致，例如 class KDCROSSOVER，檔名也是 KDCROSSOVER.py
class KDCROSSOVER:
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
        self.stock_price['diff'] = self.stock_price['K'] - self.stock_price['D']
        self.stock_price['signal'] = self.stock_price['diff'].map(lambda x: 1 if x > 0 else -1)
        self.stock_price['signal_shift1'] = self.stock_price['signal'].shift(1)
        self.stock_price = self.stock_price.dropna()

        self.stock_price['signal_shift1'] = self.stock_price['signal_shift1'].astype(int)
        colname = ['date','signal','signal_shift1']
        self.stock_price = self.stock_price[colname]

        self.stock_price = self.stock_price.sort_values('date')
        self.stock_price.index = range(len(self.stock_price))

    def trade(self,date):
        '''
        此區塊，可進行資料處理、做技術指標，寫自己的策略，
        寫你自己的策略, 必須 return : 1 (買) or -1 (賣) or 0 (不操作)
        根據時間date，回傳當下要進行什麼操作 ( 買/賣/不操作 )

        date : 昨天時間
        用昨天的資料，計算技術指標，判斷今天買/賣
        '''
        value = self.stock_price[ self.stock_price['date'] == date ]
        signal = value['signal'].values[0]
        signal_shift1 = value['signal_shift1'].values[0]
        if len(value) == 0:
            return 0

        if signal > 0 and signal_shift1 < 0:
            return 1
        elif signal < 0 and signal_shift1 > 0:
            return -1
        else:
            return 0

def test():

    stock_id = '0056'
    date = '2015-01-01'

    url = 'http://finmindapi.servebeer.com/api/data'
    form_data = {'dataset':'TaiwanStockPrice',
                 'stock_id':stock_id,
                 'date':date}

    res = requests.post(url,verify = True,data = form_data)

    temp = res.json()
    stock_price = pd.DataFrame(temp['data'])

    obj = KDCROSSOVER(
        stock_price=stock_price
    )
    obj.trade('2019-05-07')

test()