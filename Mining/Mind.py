

import pandas as pd
import numpy as np
from FinMind.Data import Load


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
        print('load Stock Price')
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
    #rsv_list = []
    data = pd.DataFrame()
    data['rolling_min'] = sp['min'].rolling(window = days).min()
    data['rolling_max'] = sp['max'].rolling(window = days).max()
    data['close'] = sp['close']
    data['date'] = sp['date']
    rsv = (data['close'] - data['rolling_min'])/(data['rolling_max']-data['rolling_min'])
    rsv = round(rsv,2)*100

    return rsv
  
def BIAS(stock_price,days = 9):
    sp = stock_price
    #rsv_list = []
    data = pd.DataFrame()
    data['mean_close'] = sp['close'].rolling(window = days).mean()
    data['close'] = sp['close']
    data['date'] = sp['date']
    
    bias = (data['close']-data['mean_close'])/data['mean_close']*100
    bias = round(bias,2)   

    return bias
    
def transpose(data):
    select_variable = 'stock_id'
    date = list( np.unique(data['date']) )
    data1 = pd.DataFrame()
    select_var_list = list( np.unique(data[select_variable]) )
    
    for d in date:# d = date[0]
        #data1 = data[]
        for select_var in select_var_list:
            data2 = data.loc[(data['date']==d) & ( data[select_variable] == select_var ),
                             ['type','value']]
            data2.index = data2['type']
            del data2['type']
            data2 = data2.T
            data2.index = range(len(data2))
            data2.columns = list(data2.columns)
            data2['stock_id'] = select_var
            data2['date'] = d
            data1 = data1.append(data2)    
            
    data1.index = range(len(data1))
    return data1




