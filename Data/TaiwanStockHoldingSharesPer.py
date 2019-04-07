
TABLE = 'HoldingSharesPer'
import os, sys
import platform
if 'Windows' in platform.platform():
    PATH = "\\".join( os.path.abspath(__file__).split('\\')[:-1])
else:
    PATH = "/".join( os.path.abspath(__file__).split('/')[:-1])
sys.path.append(PATH)
from BasedClass import Load

class ClassTaiwanStockHoldingSharesPer(Load):
    def __init__(self):
        super(ClassTaiwanStockHoldingSharesPer, self).__init__(TABLE,'stock_id')

def TaiwanStockHoldingSharesPer(select = [],date = ''):
    
    self = ClassTaiwanStockHoldingSharesPer()  
    #stock = select
    if isinstance(select,int): select = str(select)
    
    if isinstance(select,str) or isinstance(select,list):
        return self.load(select,date)
        
    #elif isinstance(select,list):
    #    return self.load_multi(select,date)
    
    else:
        raise(AttributeError, "Hidden attribute")  

