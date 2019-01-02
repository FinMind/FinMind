
import os, sys
import importlib
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
        data = getattr(importlib.import_module("FinMind.API.{}".format(table)), table)(
                select = select,date = date)
        return data
#-------------------------------------------------------------------------------------------

def LoadTableList(table = '',select = [],date = ''):
    if table not in ['StockPrice','FinancialStatements',
                     'StockDividend','ExchangeRate','InterestRate',
                     'GovernmentBonds','CrudeOilPrices','EnergyFuturesPrices']:
        raise(AttributeError, "Hidden attribute")  
    else:
        data = getattr(importlib.import_module("FinMind.API.{}".format(table)), 'Load_Data_List')()
        return data




