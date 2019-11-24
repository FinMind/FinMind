
import pandas as pd
import numpy as np
import requests

# class name，必須跟檔案名一致，例如 class MACROSSOVER，檔名也是 MACROSSOVER.py
class MACROSSOVER:
    def __init__(self,
                 stock_price,
                 **kwargs,):
        #-------------------------------------------------------------------
        # 此區塊請勿更動
        stock_price = stock_price.sort_values('date')
        # 股價
        self.stock_price = stock_price.copy()
        # 融資融券
        self.MarginPurchaseShortSale = kwargs.get("MarginPurchaseShortSale", pd.DataFrame())
        # 三大法人買賣
        self.InstitutionalInvestorsBuySell = kwargs.get("InstitutionalInvestorsBuySell", pd.DataFrame())
        # 外資持股
        self.Shareholding = kwargs.get("Shareholding", pd.DataFrame())
        # 此區塊請勿更動
        #-------------------------------------------------------------------
        self.url = 'https://www.cmoney.tw/learn/course/technicalanalysisfast/topic/1811'
        self.summary = '''均線黃金交叉
                          以短線操作來說，當 5日均線 向上突破 20日均線
                          也就是短期的平均買進成本大於長期平均成本
                          代表短期買方的力道較大，市場上大多數人獲利
                          市場易走出「多頭」的趨勢，進而帶動長期均線向上，讓股價上漲機率較大
                          短期線 突破 長期線(黃金交叉)，進場
                          長期線 突破 短期線(死亡交叉)，出場
                          '''
        self.create_feature()

    def create_feature(self):
        self.stock_price['ma10'] = self.stock_price['close'].rolling(window=10).mean()
        self.stock_price['ma30'] = self.stock_price['close'].rolling(window=30).mean()

        self.stock_price['madiff'] = self.stock_price['ma10'] - self.stock_price['ma30']
        self.stock_price['signal'] = self.stock_price['madiff'].map(lambda x: 1 if x > 0 else -1)
        self.stock_price['signal_shift1'] = self.stock_price['signal'].shift(1)
        self.stock_price = self.stock_price.dropna()

        self.stock_price['signal_shift1'] = self.stock_price['signal_shift1'].astype(int)
        colname = ['date','signal','signal_shift1']
        self.stock_price = self.stock_price[colname]
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
        if len(value) == 0:
            return 0

        signal = value['signal'].values[0]
        signal_shift1 = value['signal_shift1'].values[0]

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

    obj = MACROSSOVER(
        stock_price=stock_price
    )
    obj.trade('2019-05-07')
