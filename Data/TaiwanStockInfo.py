

TABLE = 'TaiwanStockInfo'

import pandas as pd
import os, sys
PATH = "/".join( os.path.abspath(__file__).split('/')[:-1])
sys.path.append(PATH)
from BasedClass import execute_sql2

class ClassTaiwanStockInfo:
    def __init__(self):
        pass

    def load_all(self):
        colname = execute_sql2( 'SHOW COLUMNS FROM {}'.format( TABLE ) )
        colname = [ c[0] for c in colname if c[0] not in  ['id','url'] ]     
        
        sql = 'select `{}` from {}'.format( '`,`'.join( colname ) ,TABLE)
        tem = execute_sql2(sql)
        data = pd.DataFrame( list(tem) )
        data.columns = colname
        '''
        sql = 'SHOW TABLES '
        #tem = execute_sql2(sql,TABLE.replace('Info','Price'))
        tem = execute_sql2(sql,'StockPrice')
        stock_id = [ te[0].replace('_TW','') for te in tem ]
        bo = [ True if x in stock_id else False for x in data['stock_id'] ]
        data = data[bo]
        data.index = range(len(data))
        '''
        return data

def TaiwanStockInfo(select = [],date = ''):
    
    self = ClassTaiwanStockInfo()  
    data = self.load_all()
    data = data[ data['status'] == 1 ]
    del data['status']
    del data['date']
        
    return data


