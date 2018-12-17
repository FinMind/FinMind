
import os, sys
import importlib
# __file__ = '/home/linsam/project/master/bitbucket/financialmining/API/Stock.py'
PATH = "/".join( os.path.abspath(__file__).split('/')[:-2])
sys.path.append(PATH)

#---------------------------------------------------------------
def Load(table = '',select = [],date = ''):
    if table not in ['StockInfo','StockPrice','FinancialStatements',
                     'StockDividend','ExchangeRate','InstitutionalInvestors',
                     'InterestRate','GovernmentBonds','CrudeOilPrices',
                     'EnergyFuturesPrices']:
        raise(AttributeError, "Hidden attribute")  
    else:
        data = getattr(importlib.import_module("API.{}".format(table)), table)(
                select = select,date = date)
        return data
#-------------------------------------------------------------------------------------------

def LoadTableList(table = '',select = [],date = ''):
    if table not in ['StockPrice','FinancialStatements',
                     'StockDividend','ExchangeRate','InterestRate',
                     'GovernmentBonds','CrudeOilPrices','EnergyFuturesPrices']:
        raise(AttributeError, "Hidden attribute")  
    else:
        data = getattr(importlib.import_module("API.{}".format(table)), 'Load_Data_List')()
        return data


#---------------------------------------------------------------
def StockInfo(select = [],date = ''):
    data = getattr(importlib.import_module("API.{}".format('StockInfo')), 'StockInfo')(
            select = select,date = date)
    return data

def StockPrice(select = [],date = ''):
    data = getattr(importlib.import_module("API.{}".format('StockPrice')), 'StockPrice')(
            select = select,date = date)
    return data

def FinancialStatements(select = [],date = ''):
    data = getattr(importlib.import_module("API.{}".format('FinancialStatements')), 'FinancialStatements')(
            select = select,date = date)
    return data

def StockDividend(select = [],date = ''):
    data = getattr(importlib.import_module("API.{}".format('StockDividend')), 'StockDividend')(
            select = select,date = date)
    return data

def ExchangeRate(select = [],date = ''):
    data = getattr(importlib.import_module("API.{}".format('ExchangeRate')), 'ExchangeRate')(
            select = select,date = date)
    return data

def InstitutionalInvestors(select = [],date = ''):
    data = getattr(importlib.import_module("API.{}".format('InstitutionalInvestors')), 'InstitutionalInvestors')(
            select = select,date = date)
    return data

def InterestRate(select = [],date = ''):
    data = getattr(importlib.import_module("API.{}".format('InterestRate')), 'InterestRate')(
            select = select,date = date)
    return data

def GovernmentBonds(select = [],date = ''):
    data = getattr(importlib.import_module("API.{}".format('GovernmentBonds')), 'GovernmentBonds')(
            select = select,date = date)
    return data

#---------------------------------------------------------------
def StockPriceList():
    data = getattr(importlib.import_module("API.{}".format('StockPrice')), 'Load_Data_List')()
    return data
    
def FinancialStatementsList():
    data = getattr(importlib.import_module("API.{}".format('FinancialStatements')), 'Load_Data_List')()
    return data


def StockDividendList():
    data = getattr(importlib.import_module("API.{}".format('StockDividend')), 'Load_Data_List')()
    return data

def ExchangeRateList():
    data = getattr(importlib.import_module("API.{}".format('ExchangeRate')), 'Load_Data_List')()
    return data

def InterestRateList():
    data = getattr(importlib.import_module("API.{}".format('InterestRate')), 'Load_Data_List')()
    return data

def GovernmentBondsList():
    data = getattr(importlib.import_module("API.{}".format('GovernmentBonds')), 'Load_Data_List')()
    return data












