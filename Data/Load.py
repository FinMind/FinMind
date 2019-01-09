
import os, sys
import importlib
PATH = "/".join( os.path.abspath(__file__).split('/')[:-2])
sys.path.append(PATH)

#---------------------------------------------------------------
def FinData(dataset = '',select = [],date = ''):
    if dataset not in ['TaiwanStockInfo','StockPrice','FinancialStatements',
                     'StockDividend','ExchangeRate','InstitutionalInvestors',
                     'InterestRate','GovernmentBonds','CrudeOilPrices',
                     'EnergyFuturesPrices','GoldPrice']:
        raise(AttributeError, "Hidden attribute")  
    else:
        data = getattr(importlib.import_module("FinMind.Data.{}".format(dataset)), dataset)(
                select = select,date = date)
        return data
#-------------------------------------------------------------------------------------------

def FinDataList(dataset = '',select = [],date = ''):
    if dataset not in ['StockPrice','FinancialStatements',
                     'StockDividend','ExchangeRate','InstitutionalInvestors',
                     'InterestRate','GovernmentBonds',
                     'CrudeOilPrices','EnergyFuturesPrices']:
        raise(AttributeError, "Hidden attribute")  
    else:
        data = getattr(importlib.import_module("FinMind.Data.{}".format(dataset)), 'Load_Data_List')()
        return data




