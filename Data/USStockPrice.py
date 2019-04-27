
TABLE = 'USStockPrice'
DATABASE = 'FinancialData'

import pandas as pd
import os, sys
import platform
if 'Windows' in platform.platform():
    PATH = "\\".join( os.path.abspath(__file__).split('\\')[:-1])
else:
    PATH = "/".join( os.path.abspath(__file__).split('/')[:-1])
sys.path.append(PATH)
from BasedClass import Load,query


class ClassUSStockPrice(Load):
    def __init__(self):
        super(ClassUSStockPrice, self).__init__(TABLE,'stock_id')
        
    def load(self,select = '',date = ''):
        
        colname = query( 'SHOW COLUMNS FROM `{}`'.format( TABLE ),database = DATABASE )
        colname = [ c[0] for c in colname if c[0] not in  ['id','url'] ]              

        if isinstance(select,list) == False:
            select = [select]
        select = "','".join(select)

        sql = 'select `{}` from `{}`'.format( '`,`'.join( colname ) ,TABLE)
        sql = "{} WHERE `stock_id` IN ('{}') ".format(sql,select)
        if date != '':
            sql = "{} AND `date` >= '{}' ".format(sql,date)
           
        data = query( sql ,database = DATABASE)
        data = pd.DataFrame(list(data))
        if len(data)>0:
            
            data.columns = colname
            
            if self.select_variable in data.columns:
                data = data.sort_values([self.select_variable,'date'])
            else:
                data = data.sort_values('date')
            data.index = range(len(data))

        return data
    
    def get_data_list(self):
        tem = query( 'SHOW TABLES',database = DATABASE )
        return [ te[0] for te in tem ]
        
def USStockPrice(select = [],date = ''):
    
    self = ClassUSStockPrice()  
    #stock = select
    if isinstance(select,int): select = str(select)
    
    if isinstance(select,str) or isinstance(select,list):
        return self.load(select,date)
    else:
        raise(AttributeError, "Hidden attribute")  
