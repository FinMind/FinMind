
TABLE = 'FinancialStatements'

import os, sys
PATH = "/".join( os.path.abspath(__file__).split('/')[:-1])
sys.path.append(PATH)
from BasedClass import Load

class ClassFinancialStatements(Load):
    def __init__(self):
        super(ClassFinancialStatements, self).__init__(TABLE,'stock_id')

def FinancialStatements(select = [],date = ''):
    
    self = ClassFinancialStatements()  
    #stock = select
    if isinstance(select,int): select = str(select)
    
    if isinstance(select,str):
        return self.load(select,date)
        
    elif isinstance(select,list):
        return self.load_multi(select,date)
    
    else:
        raise(AttributeError, "Hidden attribute")  
    

def Load_Data_List():
    self = ClassFinancialStatements()  
    return list( self.get_data_list() )


