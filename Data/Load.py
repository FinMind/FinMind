
import pandas as pd
import numpy as np
import os, sys
import importlib
import platform
if 'Windows' in platform.platform():
    PATH = "\\".join( os.path.abspath(__file__).split('\\')[:-2])
else:
    PATH = "/".join( os.path.abspath(__file__).split('/')[:-2])
sys.path.append(PATH)

#---------------------------------------------------------------
def FinData(dataset,select='',date='2000-01-01'):# dataset = 'BalanceSheet'
    
        
    if dataset not in ['TaiwanStockInfo','TaiwanStockPrice',
                       'TaiwanStockFinancialStatements','TaiwanStockStockDividend',
                       'TaiwanStockMarginPurchaseShortSale',
                       'TaiwanStockHoldingSharesPer',
                       'BalanceSheet','TaiwanStockMonthRevenue',
                       #-----------------------------------
                       'USStockInfo','USStockPrice',
                       #-----------------------------------
                       'JapanStockInfo','JapanStockPrice',
                       #-----------------------------------
                       'UKStockInfo','UKStockPrice',
                       #-----------------------------------
                       'EuropeStockInfo','EuropeStockPrice',
                       #-----------------------------------
                       'FinancialStatements','InstitutionalInvestorsBuySell',
                       'ExchangeRate','InstitutionalInvestors',
                       'InterestRate','GovernmentBonds','CrudeOilPrices',
                       'EnergyFuturesPrices','GoldPrice','RawMaterialFuturesPrices',
                       #-----------------------------------
                       'CurrencyCirculation','Shareholding']:
        raise(AttributeError, "Hidden attribute")  
    else:
        if select in ['',[]] and dataset in ['ExchangeRate','InstitutionalInvestors',
                       'InterestRate','GovernmentBonds',
                       'CrudeOilPrices','EnergyFuturesPrices','RawMaterialFuturesPrices',
                       'CurrencyCirculation']:
            select = FinDataList(dataset)        
        data = getattr(importlib.import_module("FinMind.Data.{}".format(dataset)), dataset)(
                select = select,date = date)
        return data
#-------------------------------------------------------------------------------------------
def FinDataList(dataset):
    if dataset not in ['ExchangeRate','InstitutionalInvestors',
                       'InterestRate','GovernmentBonds',
                       'CrudeOilPrices','EnergyFuturesPrices',
                       'CurrencyCirculation','RawMaterialFuturesPrices']:
        raise(AttributeError, "Hidden attribute")  
    else:
        data = getattr(importlib.import_module("FinMind.Data.{}".format(dataset)), 'Load_Data_List')()
        return data

# for crawler
def CrawlerStockInfo(dataset = ''):

    data = getattr(importlib.import_module("FinMind.Data.{}".format(dataset)), dataset)(
            status = 'crawler')
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

#-------------------------------------------------------------------------------------------
# stock info
def TaiwanStockInfo():
    dataset = 'TaiwanStockInfo'
    data = getattr(importlib.import_module("FinMind.Data.{}".format(dataset)), dataset)()
    return data
def USStockInfo():
    dataset = 'USStockInfo'
    data = getattr(importlib.import_module("FinMind.Data.{}".format(dataset)), dataset)()
    return data

def JapanStockInfo():
    dataset = 'JapanStockInfo'
    data = getattr(importlib.import_module("FinMind.Data.{}".format(dataset)), dataset)()
    return data

def UKStockInfo():
    dataset = 'UKStockInfo'
    data = getattr(importlib.import_module("FinMind.Data.{}".format(dataset)), dataset)()
    return data

def EuropeStockInfo():
    dataset = 'EuropeStockInfo'
    data = getattr(importlib.import_module("FinMind.Data.{}".format(dataset)), dataset)()
    return data
#-------------------------------------------------------------------------------------------
# list
def ExchangeRateList():
    dataset = 'ExchangeRate'
    data = getattr(importlib.import_module("FinMind.Data.{}".format(dataset)), 'Load_Data_List')()
    return data

def InstitutionalInvestorsList():
    dataset = 'InstitutionalInvestors'
    data = getattr(importlib.import_module("FinMind.Data.{}".format(dataset)), 'Load_Data_List')()
    return data

def InterestRateList():
    dataset = 'InterestRate'
    data = getattr(importlib.import_module("FinMind.Data.{}".format(dataset)), 'Load_Data_List')()
    return data

def GovernmentBondsList():
    dataset = 'GovernmentBonds'
    data = getattr(importlib.import_module("FinMind.Data.{}".format(dataset)), 'Load_Data_List')()
    return data

def EnergyFuturesPricesList():
    dataset = 'EnergyFuturesPrices'
    data = getattr(importlib.import_module("FinMind.Data.{}".format(dataset)), 'Load_Data_List')()
    return data

def CrudeOilPricesList():
    dataset = 'CrudeOilPrices'
    data = getattr(importlib.import_module("FinMind.Data.{}".format(dataset)), 'Load_Data_List')()
    return data

def CurrencyCirculationList():
    dataset = 'CurrencyCirculation'
    data = getattr(importlib.import_module("FinMind.Data.{}".format(dataset)), 'Load_Data_List')()
    return data
#-------------------------------------------------------------------------------------------
# stock price
def TaiwanStockPrice(select = '2330',date = '2018-01-01'):
    dataset = 'TaiwanStockPrice'
    data = getattr(importlib.import_module("FinMind.Data.{}".format(dataset)), dataset)(
                    select = select,date = date)
    return data

def USStockPrice(select = 'AAPL',date = '2018-01-01'):
    dataset = 'USStockPrice'
    data = getattr(importlib.import_module("FinMind.Data.{}".format(dataset)), dataset)(
                    select = select,date = date)
    return data

def JapanStockPrice(select = '1377.T',date = '2018-01-01'):
    dataset = 'JapanStockPrice'
    data = getattr(importlib.import_module("FinMind.Data.{}".format(dataset)), dataset)(
                    select = select,date = date)
    return data

def UKStockPrice(select = 'ZIUS.L',date = '2018-01-01'):
    dataset = 'UKStockPrice'
    data = getattr(importlib.import_module("FinMind.Data.{}".format(dataset)), dataset)(
                    select = select,date = date)
    return data

def EuropeStockPrice(select = 'WLN.PA',date = '2018-01-01'):
    dataset = 'EuropeStockPrice'
    data = getattr(importlib.import_module("FinMind.Data.{}".format(dataset)), dataset)(
                    select = select,date = date)
    return data
#-------------------------------------------------------------------------------------------
    
def BalanceSheet(select,date = '',year = '',season = ''):
    dataset = 'BalanceSheet'
    data = getattr(importlib.import_module("FinMind.Data.{}".format(dataset)), dataset)(
                    select = select,date = date,year = year,season = season )
    return data

def FinancialStatements(select,date = '',year = '',season = ''):
    dataset = 'FinancialStatements'
    data = getattr(importlib.import_module("FinMind.Data.{}".format(dataset)), dataset)(
                    select = select,date = date,year = year,season = season )
    return data

def TaiwanStockStockDividend(select,date):
    dataset = 'TaiwanStockStockDividend'
    data = getattr(importlib.import_module("FinMind.Data.{}".format(dataset)), dataset)(
                    select = select,date = date)
    return data

def TaiwanStockMarginPurchaseShortSale(select = '2330',date = '2018-01-01'):
    dataset = 'TaiwanStockMarginPurchaseShortSale'
    data = getattr(importlib.import_module("FinMind.Data.{}".format(dataset)), dataset)(
                    select = select,date = date)
    return data

def TaiwanStockMonthRevenue(select = '2330',date = '2018-01-01'):
    dataset = 'TaiwanStockMonthRevenue'
    data = getattr(importlib.import_module("FinMind.Data.{}".format(dataset)), dataset)(
                    select = select,date = date)
    return data

def InstitutionalInvestorsBuySell(select = '2330',date = '2018-01-01'):
    dataset = 'InstitutionalInvestorsBuySell'
    data = getattr(importlib.import_module("FinMind.Data.{}".format(dataset)), dataset)(
                    select = select,date = date)
    return data

def Shareholding(select = '2330',date = '2018-01-01'):
    dataset = 'Shareholding'
    data = getattr(importlib.import_module("FinMind.Data.{}".format(dataset)), dataset)(
                    select = select,date = date)
    return data

def ExchangeRate(select = 'Canda',date = '2018-01-01'):
    dataset = 'ExchangeRate'
    data = getattr(importlib.import_module("FinMind.Data.{}".format(dataset)), dataset)(
                    select = select,date = date)
    return data

def InstitutionalInvestors(select = 'Dealer',date = '2018-01-01'):
    dataset = 'InstitutionalInvestors'
    data = getattr(importlib.import_module("FinMind.Data.{}".format(dataset)), dataset)(
                    select = select,date = date)
    return data

def InterestRate(select = 'BCB',date = '2018-01-01'):
    dataset = 'InterestRate'
    data = getattr(importlib.import_module("FinMind.Data.{}".format(dataset)), dataset)(
                    select = select,date = date)
    return data

def GovernmentBonds(select = '2330',date = '2018-01-01'):
    dataset = 'GovernmentBonds'
    data = getattr(importlib.import_module("FinMind.Data.{}".format(dataset)), dataset)(
                    select = select,date = date)
    return data

def CrudeOilPrices(select = 'Brent',date = '2018-01-01'):
    dataset = 'CrudeOilPrices'
    data = getattr(importlib.import_module("FinMind.Data.{}".format(dataset)), dataset)(
                    select = select,date = date)
    return data

def EnergyFuturesPrices(select = 'Brent Oil Futures',date = '2018-01-01'):
    dataset = 'EnergyFuturesPrices'
    data = getattr(importlib.import_module("FinMind.Data.{}".format(dataset)), dataset)(
                    select = select,date = date)
    return data

def RawMaterialFuturesPrices(select = 'Brent Oil Futures',date = '2018-01-01'):
    dataset = 'RawMaterialFuturesPrices'
    data = getattr(importlib.import_module("FinMind.Data.{}".format(dataset)), dataset)(
                    select = select,date = date)
    return data

def CurrencyCirculation(select = 'Taiwan',date = '2018-01-01'):
    dataset = 'CurrencyCirculation'
    data = getattr(importlib.import_module("FinMind.Data.{}".format(dataset)), dataset)(
                    select = select,date = date)
    return data

def GoldPrice(date = '2018-01-01'):
    dataset = 'GoldPrice'
    data = getattr(importlib.import_module("FinMind.Data.{}".format(dataset)), dataset)(date = date)
    return data

def TaiwanStockHoldingSharesPer(select = '2330',date = '2018-01-01'):
    dataset = 'TaiwanStockHoldingSharesPer'
    data = getattr(importlib.import_module("FinMind.Data.{}".format(dataset)), dataset)(
                    select = select,date = date)
    return data

