

import warnings
warnings.filterwarnings("ignore")
import numpy as np
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import dateutil.relativedelta
import requests
from FinMind.BackTesting import selenium

url = 'http://finmindapi.servebeer.com/api/data'

def get_data(dataset,stock_id,date):
    form_data = {'dataset':'TaiwanStockPrice','stock_id':'2330','date':'2019-06-01'}
    res = requests.post(url,verify = True,data = form_data)
    
    temp = res.json()
    data = pd.DataFrame(temp['data'])
    return data

class BackTest:

    def __init__(self,
                 stock_id,
                 user_funds = 1000000,# 使用者資金
                 tax = 0.005,# 稅
                 fee = 0.005,# 手續費
                 day = None,# 近 n 天
                 month = None,# 近 n 月
                 year = None,# 近 n 年
                 start_date = None,
                 end_date = None
                 ):
        self.stock_id = stock_id

        assert ((year!=None or month!=None or day!=None) != (start_date!=None or end_date!=None)), 'year, month, day 和 start_date, end_date 不要一起使用'
        assert (start_date==None and end_date!=None) is False, '請給定 start_date 或者使用 year, month, day'

        if year or month or day:
            date = datetime.datetime.now().date()
            if day:
                date -= dateutil.relativedelta.relativedelta(days=day)
            if month:
                date -= dateutil.relativedelta.relativedelta(months=month)
            if year:
                date -= dateutil.relativedelta.relativedelta(years=year)
            st_date = date.strftime('%Y-%m-%d')
            en_date = None
        elif start_date and end_date:
            st_date = start_date
            en_date = end_date
        elif start_date:
            st_date = start_date
            en_date = None

        self.st_date = st_date
        self.en_date = en_date

        self.tax = tax
        self.fee = fee
        self.user_funds = user_funds
        self.user_stock = selenium.stock(stock_id,0,0,0).__dict__ # 張數，成本, 現價
        self.load_data()

    def load_data(self):
        
        self.stock_price = get_data(
                'TaiwanStockPrice', self.stock_id, self.st_date)

        
        self.MarginPurchaseShortSale = \
            get_data(
                    'TaiwanStockMarginPurchaseShortSale', 
                    self.stock_id, 
                    self.st_date)
            
        self.InstitutionalInvestorsBuySell = \
            get_data(
                    'InstitutionalInvestorsBuySell', 
                    self.stock_id, 
                    self.st_date)

        self.Shareholding = \
            get_data(
                    'Shareholding', 
                    self.stock_id, 
                    self.st_date)

    def selenium_trade(self,stock_price,volume,trade):

        #volume = 1000
        self.user_funds, self.user_stock = \
            selenium.trade(
                self.user_funds,
                self.user_stock,
                stock_price,
                volume,
                trade,
                self.tax,
                self.fee)

    def init_strategy(self,strategy = ''):
        # class object
        self.strategy = strategy(
                stock_price = self.stock_price,
                MarginPurchaseShortSale = self.MarginPurchaseShortSale,
                InstitutionalInvestorsBuySell = self.InstitutionalInvestorsBuySell,
                Shareholding = self.Shareholding,
                )
        
    def selenium_everyday(self):
        '''
        滾動式，模擬每天狀況，如果達到策略買賣標準，即進行交易
        用前一天的技術指標，判斷是否買賣，並用當天開盤價，作為成交價
        '''
        #UnrealizedProfit = 0
        self.result = pd.DataFrame()
        user_funds = []
        self.stock_price.index = range(len(self.stock_price))
        for i in range(1,len(self.stock_price)):
            # 用前一天的技術指標，判斷是否買賣，並用當天開盤價，作為成交價
            date = self.stock_price.loc[i-1,'date']
            trade = self.strategy.trade(date)
            #------------------------------------------
            stock_price = self.stock_price.loc[i,'open']
            self.user_stock['price'] = stock_price

            volume = 1000 # 預設每次交易 1000 股
            if trade == 1 and (self.user_funds - stock_price*1000 < 0):
                # 如果沒錢了，就不買
                pass
            elif trade == -1 and ( self.user_stock['volume'] - volume < 0 ):
                # 如果沒股票，就不賣
                pass
            else:
                self.selenium_trade(stock_price,volume,trade)

            value = pd.DataFrame.from_dict(
                    self.user_stock,orient = 'index' ).T
            # 紀錄每天資金變化
            user_funds.append(self.user_funds)
            self.result = self.result.append( value )

        self.result['date'] = list( self.stock_price[1:]['date'] )
        self.result['user_funds'] = user_funds
        self.result.index = range(len(self.result))

    def calculate_mean_profit_max_loss(self):

        self.mean_profit = np.mean( self.result['everytime_profit'] )
        self.max_loss = min( self.result['everytime_profit'] )
        self.now_profit = self.result['everytime_profit'].values[-1]

        user_funds = self.result.loc[0,'user_funds']

        self.mean_profit_per = round( self.mean_profit/user_funds*100, 2)
        self.now_profit_per = round( self.now_profit/user_funds*100, 2)
        self.max_loss_per = round( self.max_loss/user_funds*100, 2)

    def cum_profit_plot(self):

        plt.figure(figsize=(12, 8))
        plt.plot(  'UnrealizedProfit',
                 data = self.result, marker = '')
        plt.plot( 'realizedProfit',
                 data = self.result, marker = '')
        plt.plot( 'everytime_profit',
                 data = self.result, marker = '')
        plt.legend(loc=2, prop={'size': 20})


