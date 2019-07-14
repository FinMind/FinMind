
import pandas as pd
import numpy as np
import requests
#---------------------------------------------------------------
def FinData(
        dataset,select = '',date = '2000-01-01',
        url = 'http://finmindapi.servebeer.com/api/data'):# dataset = 'BalanceSheet'

    parameter = {'dataset':dataset,
                 'stock_id':select,
                 'date':date}
    res = requests.post(
            url,verify = True,headers = {},
            json = parameter)
        
    data = res.json()
    if data['status'] == 200:
        data = pd.DataFrame( data['data'] )
    
    return data
#-------------------------------------------------------------------------------------------
def FinDataList(
        dataset,
        list_url = 'http://finmindapi.servebeer.com/api/datalist'):# dataset = 'BalanceSheet'

    parameter = {'dataset':dataset}
    res = requests.post(
            list_url,verify = True,headers = {},
            json = parameter)
        
    data = res.json()
    if data['status'] == 200:
        data = data['data']
        
    return data

# for crawler
def CrawlerStockInfo(dataset = ''):

    data = FinData(dataset)
    return data
#-------------------------------------------------------------------------------------------
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
