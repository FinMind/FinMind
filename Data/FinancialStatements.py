
TABLE = 'FinancialStatements2'
import os, sys
import platform
if 'Windows' in platform.platform():
    PATH = "\\".join( os.path.abspath(__file__).split('\\')[:-1])
else:
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
    
    if isinstance(select,str) or isinstance(select,list):
        data = self.load(select,date)
        
    #elif isinstance(select,list):
    #    data = self.load_multi(select,date)
    
    else:
        raise(AttributeError, "Hidden attribute")  
    
    #data = self.transpose(data)
    
    return data
    
    
