
import pandas as pd
import numpy as np
import requests

# class name，必須跟檔案名一致，例如 class SHORTSALE_MARGINPURCHASE_RATIO，檔名也是 SHORTSALE_MARGINPURCHASE_RATIO.py
class SHORTSALE_MARGINPURCHASE_RATIO:
    def __init__(self,
                 stock_price,
                 ShortSaleMarginPurchaseTodayRatioThreshold=0.3,
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
        self.ShortSaleMarginPurchaseTodayRatioThreshold = ShortSaleMarginPurchaseTodayRatioThreshold

        self.url = 'https://blog.above.tw/2018/08/15/%E7%B1%8C%E7%A2%BC%E9%9D%A2%E7%9A%84%E9%97%9C%E9%8D%B5%E6%8C%87%E6%A8%99%E6%9C%89%E5%93%AA%E4%BA%9B%EF%BC%9F/'
        self.summary = '''策略概念: 券資比越高代表散戶看空，法人買超股票會上漲，這時候賣可以跟大部分散戶進行相反的操作，反之亦然
                          策略規則: 券資比>=30% 且法人買超股票, 賣
                                    券資比<30% 且法人賣超股票 買'''
        self.MarginPurchaseShortSale[['ShortSaleTodayBalance', 'MarginPurchaseTodayBalance']] = self.MarginPurchaseShortSale[['ShortSaleTodayBalance', 'MarginPurchaseTodayBalance']].astype(int)
        self.MarginPurchaseShortSale['ShortSaleMarginPurchaseTodayRatio'] = self.MarginPurchaseShortSale['ShortSaleTodayBalance'] / self.MarginPurchaseShortSale['MarginPurchaseTodayBalance']

        self.InstitutionalInvestorsBuySell[['sell', 'buy']] = self.InstitutionalInvestorsBuySell[['sell', 'buy']].astype(int)
        self.InstitutionalInvestorsBuySell = self.InstitutionalInvestorsBuySell.groupby(['date', 'stock_id'], as_index=False).agg({'buy':np.sum, 'sell':np.sum})
        self.InstitutionalInvestorsBuySell['diff'] = self.InstitutionalInvestorsBuySell['buy'] - self.InstitutionalInvestorsBuySell['sell']

        self.stock_price = pd.merge(self.stock_price[['stock_id', 'date', 'open', 'close']], self.InstitutionalInvestorsBuySell[['stock_id', 'date', 'diff']], on=['stock_id', 'date'], how='left').fillna(0)
        self.stock_price = pd.merge(self.stock_price, self.MarginPurchaseShortSale[['stock_id', 'date', 'ShortSaleMarginPurchaseTodayRatio']], on=['stock_id', 'date'], how='left').fillna(0)

    def trade(self,date):
        '''
        此區塊，可進行資料處理、做技術指標，寫自己的策略，
        寫你自己的策略, 必須 return : 1 (買) or -1 (賣) or 0 (不操作)
        根據時間date，回傳當下要進行什麼操作 ( 買/賣/不操作 )

        date : 昨天時間
        用昨天的資料，計算技術指標，判斷今天買/賣
        '''
        value = self.stock_price[self.stock_price['date']==date]
        ShortSaleMarginPurchaseTodayRatio = value['ShortSaleMarginPurchaseTodayRatio'].values
        diff = value['diff'].values

        if ShortSaleMarginPurchaseTodayRatio>=self.ShortSaleMarginPurchaseTodayRatioThreshold and diff>0:
            return -1
        elif ShortSaleMarginPurchaseTodayRatio<self.ShortSaleMarginPurchaseTodayRatioThreshold and diff<0:
            return 1
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

    form_data = {'dataset':'TaiwanStockMarginPurchaseShortSale',
                'stock_id':stock_id,
                'date':date}
    res = requests.post(
        url,verify = True,
        data = form_data)

    temp = res.json()
    TaiwanStockMarginPurchaseShortSale = pd.DataFrame(temp['data'])

    form_data = {'dataset':'InstitutionalInvestorsBuySell',
                'stock_id':stock_id,
                'date':date}
    res = requests.post(
        url,verify = True,
        data = form_data)

    temp = res.json()
    InstitutionalInvestorsBuySell = pd.DataFrame(temp['data'])

    obj = SHORTSALE_MARGINPURCHASE_RATIO(
        stock_price=stock_price,
        MarginPurchaseShortSale=TaiwanStockMarginPurchaseShortSale,
        InstitutionalInvestorsBuySell=InstitutionalInvestorsBuySell
    )
    obj.trade('2019-05-07')
