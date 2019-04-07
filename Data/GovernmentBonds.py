
TABLE = 'GovernmentBonds'

import os, sys
import platform
if 'Windows' in platform.platform():
    PATH = "\\".join( os.path.abspath(__file__).split('\\')[:-1])
else:
    PATH = "/".join( os.path.abspath(__file__).split('/')[:-1])
sys.path.append(PATH)
from BasedClass import Load


class ClassGovernmentBonds(Load):
    def __init__(self):
        super(ClassGovernmentBonds, self).__init__(TABLE,'bound_type')


def GovernmentBonds(select = ['Japan 1-Year','Japan 10-Year'],
                    date = '2018-10-10'):
    
    self = ClassGovernmentBonds()  
    #stock = select
    if isinstance(select,int): select = str(select)
    
    if isinstance(select,str) or isinstance(select,list):
        return self.load(select,date)
        
    #elif isinstance(select,list):
    #    return self.load_multi(select,date)
        
    else:
        raise(AttributeError, "Hidden attribute")  

def Load_Data_List():
    self = ClassGovernmentBonds()  
    return list( self.get_data_list() )
