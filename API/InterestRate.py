
TABLE = 'InterestRate'
from BasedClass import Load

class ClassInterestRate(Load):
    def __init__(self):
        super(ClassInterestRate, self).__init__(TABLE,'country')

def InterestRate(select = [],date = ''):
    
    self = ClassInterestRate()  
    #stock = select
    if isinstance(select,int): select = str(select)
    
    if isinstance(select,str):
        return self.load(select,date)
        
    elif isinstance(select,list):
        return self.load_multi(select,date)
    
    else:
        raise(AttributeError, "Hidden attribute")  
    

def Load_Data_List():
    self = ClassInterestRate()  
    return list( self.get_data_list() )


