
import pandas as pd
import numpy as np
import requests

# class name，必須跟檔案名一致，例如 class INSTITUTIONAL_INVESTORS_FOLLOWER，檔名也是 INSTITUTIONAL_INVESTORS_FOLLOWER.py
class INSTITUTIONAL_INVESTORS_FOLLOWER:
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
        self.url = 'https://www.finlab.tw/%E8%85%A6%E5%8A%9B%E6%BF%80%E7%9B%AA%E7%9A%84%E5%A4%96%E8%B3%87%E7%AD%96%E7%95%A5%EF%BC%81/'
        self.summary = '''策略概念: 法人大量買超會導致股價上漲, 賣超反之
                          策略規則: 三大法人大量買超隔天就賣，大量賣超就買'''
        self.InstitutionalInvestorsBuySell[['sell', 'buy']] = self.InstitutionalInvestorsBuySell[['sell', 'buy']].astype(int)
        self.InstitutionalInvestorsBuySell = self.InstitutionalInvestorsBuySell.groupby(['date', 'stock_id'], as_index=False).agg({'buy':np.sum, 'sell':np.sum})
        self.InstitutionalInvestorsBuySell['diff'] = self.InstitutionalInvestorsBuySell['buy'] - self.InstitutionalInvestorsBuySell['sell']

        self.stock_price = pd.merge(self.stock_price[['stock_id', 'date', 'open', 'close']], self.InstitutionalInvestorsBuySell[['stock_id', 'date', 'diff']], on=['stock_id', 'date'], how='left').fillna(0)
        self.stock_price['signal'] =self.detect_Abnormal_Peak(
            y=self.stock_price['diff'].values, lag=10, threshold=3, influence=0.35)['signals']

    def detect_Abnormal_Peak(self, y, lag, threshold, influence):
        signals = np.zeros(len(y))
        filteredY = np.array(y)
        avgFilter = [0]*len(y)
        stdFilter = [0]*len(y)
        avgFilter[lag - 1] = np.mean(y[0:lag])
        stdFilter[lag - 1] = np.std(y[0:lag])
        for i in range(lag, len(y)):
            if abs(y[i] - avgFilter[i-1]) > threshold * stdFilter [i-1]:
                if y[i] > avgFilter[i-1]:
                    signals[i] = 1
                else:
                    signals[i] = -1

                filteredY[i] = influence * y[i] + (1 - influence) * filteredY[i-1]
                avgFilter[i] = np.mean(filteredY[(i-lag+1):i+1])
                stdFilter[i] = np.std(filteredY[(i-lag+1):i+1])
            else:
                signals[i] = 0
                filteredY[i] = y[i]
                avgFilter[i] = np.mean(filteredY[(i-lag+1):i+1])
                stdFilter[i] = np.std(filteredY[(i-lag+1):i+1])

        return dict(signals = np.asarray(signals),
                    avgFilter = np.asarray(avgFilter),
                    stdFilter = np.asarray(stdFilter))

    def trade(self,date):
        '''
        此區塊，可進行資料處理、做技術指標，寫自己的策略，
        寫你自己的策略, 必須 return : 1 (買) or -1 (賣) or 0 (不操作)
        根據時間date，回傳當下要進行什麼操作 ( 買/賣/不操作 )

        date : 昨天時間
        用昨天的資料，計算技術指標，判斷今天買/賣
        '''
        # example
        value = self.stock_price[self.stock_price['date']==date]
        signal = value['signal'].values
        if len(value) == 0:
            return 0

        if signal == -1:
            return 1 # buy
        elif signal == 1:
            return -1 # sell
        elif signal == 0:
            return 0 # no buy and no sell

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

    form_data = {'dataset':'InstitutionalInvestorsBuySell',
  	   'stock_id':stock_id,
  	   'date':date}
    res = requests.post(
        url,verify = True,
        data = form_data)

    temp = res.json()
    InstitutionalInvestorsBuySell = pd.DataFrame(temp['data'])

    obj = INSTITUTIONAL_INVESTORS_FOLLOWER(
        stock_price=stock_price,
        InstitutionalInvestorsBuySell=InstitutionalInvestorsBuySell
    )
    obj.trade('2019-05-07')

