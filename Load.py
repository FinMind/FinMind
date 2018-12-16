
import importlib

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
