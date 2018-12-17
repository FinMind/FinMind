
TABLE = 'GovernmentBonds'

import os, sys
PATH = "/".join( os.path.abspath(__file__).split('/')[:-2])
sys.path.append(PATH)
from API.BasedClass import Load


class ClassGovernmentBonds(Load):
    def __init__(self):
        super(ClassGovernmentBonds, self).__init__(TABLE,'bound_type')


def GovernmentBonds(select = ['Japan 1-Year','Japan 10-Year'],
                    date = '2018-10-10'):
    
    self = ClassGovernmentBonds()  
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
    self = ClassGovernmentBonds()  
    return list( self.get_data_list() )
