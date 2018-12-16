
TABLE = 'StockDividend'

from BasedClass import Load

class ClassStockDividend(Load):
    def __init__(self):
        super(ClassStockDividend, self).__init__(TABLE,'stock_id')

def StockDividend(select = [],date = ''):
    
    self = ClassStockDividend()  
    #stock = select
    if isinstance(select,int): select = str(select)
    
    if isinstance(select,str):
        return self.load(select,date)
        
    elif isinstance(select,list):
        return self.load_multi(select,date)
    
    else:
        raise(AttributeError, "Hidden attribute")  
    

def Load_Data_List():
    self = ClassStockDividend()  
    return list( self.get_data_list() )



