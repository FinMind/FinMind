
TABLE = 'InstitutionalInvestorsBuySell'

import os, sys
PATH = "/".join( os.path.abspath(__file__).split('/')[:-1])
sys.path.append(PATH)
from BasedClass import Load

class ClassInstitutionalInvestorsBuySell(Load):
    def __init__(self):
            super(ClassInstitutionalInvestorsBuySell, self).__init__(TABLE,'stock_id')

def InstitutionalInvestorsBuySell(select = [],date = ''):
    
    self = ClassInstitutionalInvestorsBuySell()  
    #stock = select
    if isinstance(select,int): select = str(select)
    
    if isinstance(select,str):
        data = self.load(select,date)
        return data
        
    elif isinstance(select,list):
        data = self.load_multi(select,date)
        return data
    
    else:
        raise(AttributeError, "Hidden attribute")  

def Load_Data_List():
    self = ClassInstitutionalInvestorsBuySell()  
    return list( self.get_data_list() )

