

import pandas as pd
import numpy as np
from FinMind.Data import Load

'''
self = Stock('2330','2019-01-01')
self.StockPrice
self.FinancialStatements
self.ShareHolding
self.InstitutionalInvestors
self.MarginPurchaseShortSale
self.MonthRevenue
self.HoldingSharesPer
self.BalanceSheet
'''
class Stock:
    def __init__(self,stock_id,date):
        self.date = date
        self.country = 'Taiwan'
        if isinstance(stock_id,str):
            self.stock_id = [stock_id]
        elif isinstance(stock_id,list):
            self.stock_id = stock_id
            
        self.StockPrice = pd.DataFrame()
        self.FinancialStatements = pd.DataFrame()
        self.ShareHolding = pd.DataFrame()
        self.InstitutionalInvestors = pd.DataFrame()
        self.MarginPurchaseShortSale = pd.DataFrame()
        self.MonthRevenue = pd.DataFrame()
        self.HoldingSharesPer = pd.DataFrame()
        self.BalanceSheet = pd.DataFrame()

    def init_stock_info(self):
        stock_info = Load.FinData(dataset = '{}StockInfo'.format(self.country))
        if 'industry_category' in stock_info.columns:
            _bool = [ False if x in ['ETF','不動產投資信託證券'] else True 
                         for x in stock_info['industry_category'] ]
            stock_info = stock_info[_bool]
            stock_info.index = range(len(stock_info))
            
        stock_info['country'] = self.country
        colname = ['stock_id','stock_name','country']
        stockinfo = stock_info[colname]
        _bool = [ True if x in self.stock_id else False 
                 for x in stockinfo['stock_id'] ]
        self.stockinfo = stockinfo[_bool]
        
    @property
    def StockPrice(self):
        return self._StockPrice
    
    @StockPrice.setter
    def StockPrice(self,value):
        print('load_stockprice')
        dataset = '{}StockPrice'.format(self.country)
        self._StockPrice = self.load_data(dataset)
        self._StockPrice['country'] = self.country
        return self._StockPrice
    
    @property
    def FinancialStatements(self):
        return self._FinancialStatements
    
    @FinancialStatements.setter
    def FinancialStatements(self,value):
        print('load Financial Statements')
        dataset = 'FinancialStatements'
        self._FinancialStatements = self.load_data(dataset,transpose = True)
        
        return self._FinancialStatements
    
    @property
    def InstitutionalInvestors(self):
        return self._InstitutionalInvestors
    
    @InstitutionalInvestors.setter
    def InstitutionalInvestors(self,value):
        print('load Institutional Investors')
        dataset = 'InstitutionalInvestorsBuySell'
        self._InstitutionalInvestors = self.load_data(dataset)
        
        return self._InstitutionalInvestors
    
    @property
    def MarginPurchaseShortSale(self):
        return self._MarginPurchaseShortSale
    
    @MarginPurchaseShortSale.setter
    def MarginPurchaseShortSale(self,value):
        print('load Taiwan Stock Margin Purchase ShortSale')
        dataset = 'TaiwanStockMarginPurchaseShortSale'
        self._MarginPurchaseShortSale = self.load_data(dataset)
        return self._MarginPurchaseShortSale
    
    @property
    def ShareHolding(self):
        return self._ShareHolding
    
    @ShareHolding.setter
    def ShareHolding(self,value):
        print('load Share holding')
        dataset = 'Shareholding'
        self._ShareHolding = self.load_data(dataset)
        return self._ShareHolding
    
    @property
    def MonthRevenue(self):
        return self._MonthRevenue
    
    @MonthRevenue.setter
    def MonthRevenue(self,value):
        print('load Month Revenue')
        dataset = 'TaiwanStockMonthRevenue'
        self._MonthRevenue = self.load_data(dataset)
        return self._MonthRevenue
    
    @property
    def HoldingSharesPer(self):
        return self._HoldingSharesPer
    
    @HoldingSharesPer.setter
    def HoldingSharesPer(self,value):
        print('load Holding Shares Per')
        dataset = 'TaiwanStockHoldingSharesPer'
        self._HoldingSharesPer = self.load_data(dataset)
        return self._HoldingSharesPer
    
    @property
    def BalanceSheet(self):
        return self._BalanceSheet
    
    @BalanceSheet.setter
    def BalanceSheet(self,value):
        print('load Balance Sheet')
        dataset = 'BalanceSheet'
        self._BalanceSheet = self.load_data(dataset)
        return self._BalanceSheet
    
    def load_data(self,dataset,transpose = False):
        #dataset = 'Shareholding'
        data = Load.FinData(
                dataset = dataset,
                select = self.stock_id,
                date = self.date)      
        
        if len(data) == 0:
            return data
        if transpose:
            data = Load.transpose(data)
        data['stock_id'] = data['stock_id'].astype(str)
        data['date'] = data['date'].astype(str)
        
        return data


def MoveAverage(stock_price,days = 5,variable = 'close'):
    # variable = 'close'
    # days = 5
    return stock_price[variable].rolling(window = days).mean()
    
def RSV(stock_price,days = 9):
    sp = stock_price
    sp = sp[len(sp)-days:]
    sp.index = range(len(sp))
    
    min_price = min(list(sp['min']))
    max_price = max(list(sp['max']))
    close = sp['close'][len(sp)-1]
    
    rsv = (close-min_price)/(max_price-min_price)*100
    rsv = round(rsv,2)
    return rsv
  
def BIAS(stock_price,days = 9):
    sp = stock_price
    sp = sp[len(sp)-9:]
    sp.index = range(len(sp))
    
    close = sp['close'][len(sp)-1]
    mean_close = np.mean(sp['close'])
    bias = (close-mean_close)/mean_close*100
    bias = round(bias,2)   
    return bias






