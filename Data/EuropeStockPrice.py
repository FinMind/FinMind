
TABLE = 'EuropeStockPrice'
import pandas as pd
import os, sys
PATH = "/".join( os.path.abspath(__file__).split('/')[:-1])
sys.path.append(PATH)
from BasedClass import Load,execute_sql2


class ClassEuropeStockPrice(Load):
    def __init__(self):
        super(ClassEuropeStockPrice, self).__init__(TABLE,'stock_id')
    
    def load(self,select = '',date = ''):
        def select_func():# select = 'ALMIL'
            pass
        
        select = '{}.T'.format(select)
        
        colname = execute_sql2( 'SHOW COLUMNS FROM `{}`'.format( select ),database = TABLE )
        colname = [ c[0] for c in colname if c[0] not in  ['id','url'] ]              
        
        sql = 'select `{}` from `{}`'.format( '`,`'.join( colname ) ,select)
        
        if date != '':
            sql = "{} WHERE `date` >= '{}' ".format(sql,date)
           
        data = execute_sql2( sql ,database = TABLE)
        data = pd.DataFrame(list(data))
        if len(data)>0:
            
            data.columns = colname
            
            if self.select_variable in data.columns:
                data = data.sort_values([self.select_variable,'date'])
            else:
                data = data.sort_values('date')
            data.index = range(len(data))
            data['stock_id'] = select
        
        return data
    
    def get_data_list(self):
        tem = execute_sql2( 'SHOW TABLES',database = TABLE )
        return [ te[0] for te in tem ]
        
def EuropeStockPrice(select = [],date = ''):
    
    self = ClassEuropeStockPrice()  
    #stock = select
    if isinstance(select,int): select = str(select)
    
    if isinstance(select,str):
        return self.load(select,date)
        
    elif isinstance(select,list):
        return self.load_multi(select,date)
    
    else:
        raise(AttributeError, "Hidden attribute")  

