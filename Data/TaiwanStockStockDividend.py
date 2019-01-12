
TABLE = 'TaiwanStockStockDividend'

import os, sys
PATH = "/".join( os.path.abspath(__file__).split('/')[:-1])
sys.path.append(PATH)
from BasedClass import Load


class ClassTaiwanStockStockDividend(Load):
    def __init__(self):
        super(ClassTaiwanStockStockDividend, self).__init__(TABLE,'stock_id')

def TaiwanStockStockDividend(select = [],date = ''):
    
    self = ClassTaiwanStockStockDividend()  
    #stock = select
    if isinstance(select,int): select = str(select)
    
    if isinstance(select,str):
        return self.load(select,date)
        
    elif isinstance(select,list):
        return self.load_multi(select,date)
    
    else:
        raise(AttributeError, "Hidden attribute")  
    
