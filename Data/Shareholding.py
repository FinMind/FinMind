
'''
NumberOfSharesIssued : 已發行股份數目
ForeignInvestmentMaxShares : 外資 max 投資股票
ForeignInvestmentShares : 外資投資股票
'''

TABLE = 'Shareholding'

import os, sys
import platform
if 'Windows' in platform.platform():
    PATH = "\\".join( os.path.abspath(__file__).split('\\')[:-1])
else:
    PATH = "/".join( os.path.abspath(__file__).split('/')[:-1])
sys.path.append(PATH)
from BasedClass import Load

class ClassShareholding(Load):
    def __init__(self):
        super(ClassShareholding, self).__init__(TABLE,'stock_id')

def Shareholding(select = [],date = ''):
    
    self = ClassShareholding()  
    
    if isinstance(select,int): select = str(select)
    
    if isinstance(select,str):
        data = self.load(select,date)
        if len(data) == 0:
            return data
        #data = data[col_name]
        return data
    elif isinstance(select,list):
        data = self.load_multi(select,date)
        if len(data) == 0:
            return data        
        #data = data[col_name]
        return data

    else:
        raise(AttributeError, "Hidden attribute")  
    
