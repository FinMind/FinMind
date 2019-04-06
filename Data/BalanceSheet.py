
TABLE = 'BalanceSheet'
import os, sys
import platform
if 'Windows' in platform.platform():
    PATH = "\\".join( os.path.abspath(__file__).split('\\')[:-1])
else:
    PATH = "/".join( os.path.abspath(__file__).split('/')[:-1])
sys.path.append(PATH)
from BasedClass import Load

class ClassBalanceSheet(Load):
    def __init__(self):
        super(ClassBalanceSheet, self).__init__(TABLE,'stock_id')

def BalanceSheet(select = [],date = ''):
    
    self = ClassBalanceSheet()
    #stock = select
    if isinstance(select,int): select = str(select)
    
    if isinstance(select,str):
        data = self.load(select,date)
        
    elif isinstance(select,list):
        data = self.load_multi(select,date)
    
    else:
        raise(AttributeError, "Hidden attribute")  

    #data = self.transpose(data)
    
    return data
