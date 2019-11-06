

import pandas as pd
import numpy as np
import requests
from FinMind.Data import Load

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


