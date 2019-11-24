
import pandas as pd
import numpy as np
import requests

# class name，必須跟檔案名一致，例如 class BAIS，檔名也是 BAIS.py
class BAIS:
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
        self.url = 'https://bc8800.pixnet.net/blog/post/328645973-%E7%A8%8B%E5%BC%8F%E4%BA%A4%E6%98%93%E4%B9%8B%E7%A0%94%E7%A9%B6%E7%AD%86%E8%A8%98---%E4%B9%96%E9%9B%A2%E7%8E%87'
        self.summary = '''乖離率策略是觀察股價偏離移動平均線(MA線)的程度來決定是否進場
                            負乖離表示股價 低 於過去一段時間平均價，意味著股價相對過去 低 ，所以選擇進場
                            正乖離表示股價 高 於過去一段時間平均價，意味著股價相對過去 高 ，所以選擇出場'''
        self.ma_days = 24
        self.bais_lower = -7
        self.bais_upper = 8
        self.create_feature()# 建立自己的 feature or 技術指標

    def create_feature(self):
        self.stock_price['ma{}'.format(self.ma_days)] = self.stock_price['close'].rolling(window=self.ma_days).mean()
        self.stock_price['bais'] = \
            ((self.stock_price['close'] - self.stock_price['ma{}'.format(self.ma_days)]) \
             / self.stock_price['ma{}'.format(self.ma_days)]) * 100

        self.stock_price = self.stock_price.dropna()
        self.stock_price.index = range(len(self.stock_price))

    def trade(self,date):
        '''
        此區塊，可進行資料處理、做技術指標，寫自己的策略，
        寫你自己的策略, 必須 return : 1 (買) or -1 (賣) or 0 (不操作)
        根據時間date，回傳當下要進行什麼操作 ( 買/賣/不操作 )

        date : 昨天時間
        用昨天的資料，計算技術指標，判斷今天買/賣
        '''
        # example
        value = self.stock_price[ self.stock_price['date'] == date ]
        if len(value) == 0:
            return 0

        bais = value['bais'].values[0]

        if bais < self.bais_lower:
            return 1
        elif bais > self.bais_upper:
            return -1
        else:
            return 0

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

    date = '2019-05-03'
    self = BAIS(stock_price)
    self.trade(date)
    self.trade('2019-05-07')
    self.trade('2019-05-11')


