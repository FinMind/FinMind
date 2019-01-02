
import os, sys
import importlib
PATH = "/".join( os.path.abspath(__file__).split('/')[:-2])
sys.path.append(PATH)

#---------------------------------------------------------------
def FinData(table = '',select = [],date = ''):
    if table not in ['StockInfo','StockPrice','FinancialStatements',
                     'StockDividend','ExchangeRate','InstitutionalInvestors',
                     'InterestRate','GovernmentBonds','CrudeOilPrices',
                     'EnergyFuturesPrices']:
        raise(AttributeError, "Hidden attribute")  
    else:
        data = getattr(importlib.import_module("FinMind.Data.{}".format(table)), table)(
                select = select,date = date)
        return data
#-------------------------------------------------------------------------------------------

def FinDataList(table = '',select = [],date = ''):
    if table not in ['StockPrice','FinancialStatements',
                     'StockDividend','ExchangeRate','InterestRate',
                     'GovernmentBonds','CrudeOilPrices','EnergyFuturesPrices']:
        raise(AttributeError, "Hidden attribute")  
    else:
        data = getattr(importlib.import_module("FinMind.Data.{}".format(table)), 'Load_Data_List')()
        return data




