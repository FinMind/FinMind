
TABLE = 'FinancialStatements'

import os, sys
PATH = "/".join( os.path.abspath(__file__).split('/')[:-1])
sys.path.append(PATH)
from BasedClass import Load

class ClassFinancialStatements(Load):
    def __init__(self):
        super(ClassFinancialStatements, self).__init__(TABLE,'stock_id')

def TaiwanFinancialStatements(select = [],date = ''):
    
    self = ClassFinancialStatements()  
    col_name = ['Revenue','CostOfGoodsSold','GrossProfit',
                'OperatingExpenses','OperatingIncome','NonOperatingIncome',
                'NonOperatingExpense', 'PreTaxIncome', 'TAX',
                'IncomeAfterTaxes',  'EPS',
                'stock_id', 'date', 'country']
    
    if isinstance(select,int): select = str(select)
    
    if isinstance(select,str):
        data = self.load(select,date)
        if len(data) == 0:
            return data
        data = data[col_name]
        return data
    elif isinstance(select,list):
        data = self.load_multi(select,date)
        if len(data) == 0:
            return data        
        data = data[col_name]
        return data

    else:
        raise(AttributeError, "Hidden attribute")  
    
