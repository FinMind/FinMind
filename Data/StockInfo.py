

TABLE = 'StockInfo'

import pandas as pd
import os, sys
PATH = "/".join( os.path.abspath(__file__).split('/')[:-1])
sys.path.append(PATH)
from BasedClass import execute_sql2

class ClassStockInfo:
    def __init__(self):
        pass

    def load_all(self):
        colname = execute_sql2( 'SHOW COLUMNS FROM {}'.format( TABLE ) )
        colname = [ c[0] for c in colname if c[0] not in  ['id','url'] ]     
        
        sql = 'select `{}` from {}'.format( '`,`'.join( colname ) ,TABLE)
        tem = execute_sql2(sql)
        data = pd.DataFrame( list(tem) )
        data.columns = colname
        return data

def StockInfo(select = [],date = ''):
    
    self = ClassStockInfo()  
    data = self.load_all()
    data = data[ data['status'] == 1 ]
    del data['status']
    del data['date']
        
    return data


